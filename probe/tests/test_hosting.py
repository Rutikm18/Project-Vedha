"""The S3 hosting kit for the Windows agent (probe/windows/hosting/).

`publish-to-s3.sh` is exercised end to end against a fake `aws` command that records what it was
asked to do; `get.ps1` is checked for the properties that matter for safety (it is exercised for
real, against a local web server, by hosting/tests/Test-Get.ps1 on the Windows runner); the
CloudFormation template is checked structurally (it has not been deployed by these tests).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

import pytest

PROBE = Path(__file__).resolve().parent.parent
HOSTING = PROBE / "windows" / "hosting"
PUBLISH = HOSTING / "publish-to-s3.sh"
GET = HOSTING / "get.ps1"

needs_bash = pytest.mark.skipif(sys.platform == "win32", reason="the publish script is bash (macOS / Linux)")


# ── a fake `aws` that records its calls and copies uploaded files aside ─────────────────────────

FAKE_AWS = r"""#!/usr/bin/env bash
echo "$*" >> "$FAKE_AWS_LOG"
if [ "$1 $2" = "s3api head-object" ]; then
  [ "${FAKE_AWS_EXISTS:-0}" = "1" ] && exit 0 || exit 254
fi
if [ "$1 $2" = "s3 cp" ]; then
  # aws s3 cp SRC s3://bucket/key ...  -> keep a copy of SRC named after the key
  key="${4#s3://*/}"
  mkdir -p "$FAKE_AWS_STORE/$(dirname "$key")"
  cp "$3" "$FAKE_AWS_STORE/$key"
fi
exit 0
"""


@pytest.fixture()
def kit(tmp_path):
    shim = tmp_path / "shim"
    shim.mkdir()
    aws = shim / "aws"
    aws.write_text(FAKE_AWS, encoding="utf-8")
    aws.chmod(aws.stat().st_mode | stat.S_IEXEC)
    zip_path = tmp_path / "vedha-agent-win.zip"
    zip_path.write_bytes(b"PK-not-really-a-zip-but-bytes-are-bytes" * 50)
    sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    release = tmp_path / "vedha-agent-win.release.json"
    release.write_text(json.dumps({
        "schema": 1, "version": "2.2.2", "package_version": "1.0.380", "manager": "https://api.example.com",
        "zip": "2.2.2/vedha-agent-win.zip", "sha256": sha, "exe_sha256": "e" * 64,
        "size": zip_path.stat().st_size, "built_at": "2026-10-08T00:00:00Z",
    }), encoding="utf-8")
    log, store = tmp_path / "aws.log", tmp_path / "store"
    store.mkdir()
    env = dict(os.environ, PATH=f"{shim}{os.pathsep}{os.environ['PATH']}",
               FAKE_AWS_LOG=str(log), FAKE_AWS_STORE=str(store))
    return {"zip": zip_path, "release": release, "sha": sha, "log": log, "store": store, "env": env, "shim": shim}


def publish(kit, *extra, base_url="https://downloads.example.com/windows", env=None):
    args = ["bash", str(PUBLISH), "--bucket", "my-bucket", "--zip", str(kit["zip"]),
            "--release", str(kit["release"]), "--base-url", base_url, *extra]
    return subprocess.run(args, capture_output=True, text=True, env=env or kit["env"], timeout=60)


def calls(kit):
    return kit["log"].read_text(encoding="utf-8").splitlines() if kit["log"].exists() else []


@needs_bash
class TestPublishScript:
    def test_uploads_in_a_safe_order_and_prints_the_commands(self, kit):
        r = publish(kit, "--distribution-id", "E123ABC")
        assert r.returncode == 0, r.stderr + r.stdout
        uploads = [c for c in calls(kit) if c.startswith("s3 cp")]
        keys = [re.search(r"s3://my-bucket/(\S+)", c).group(1) for c in uploads]
        assert keys == [
            "windows/2.2.2/vedha-agent-win.zip",
            "windows/2.2.2/vedha-agent-win.zip.sha256",
            "windows/2.2.2/release.json",
            "windows/get.ps1",
            "windows/latest.json",          # last: nobody is pointed at a file that is not there yet
        ]
        assert any(c.startswith("cloudfront create-invalidation --distribution-id E123ABC --paths /windows/get.ps1 /windows/latest.json") for c in calls(kit))
        out = r.stdout
        assert f"-Version 2.2.2 -Sha256 {kit['sha']} -Token <TOKEN>" in out
        assert "irm https://downloads.example.com/windows/get.ps1" in out
        assert 'curl.exe -fsSL https://downloads.example.com/windows/get.ps1' in out
        assert "Tls12" in out and "ADMINISTRATOR" in out

    def test_cache_headers(self, kit):
        publish(kit)
        by_key = {re.search(r"s3://my-bucket/(\S+)", c).group(1): c for c in calls(kit) if c.startswith("s3 cp")}
        assert "immutable" in by_key["windows/2.2.2/vedha-agent-win.zip"]
        assert "--content-type application/zip" in by_key["windows/2.2.2/vedha-agent-win.zip"]
        assert "no-cache" in by_key["windows/get.ps1"] and "no-cache" in by_key["windows/latest.json"]

    def test_the_published_script_has_the_download_address_filled_in(self, kit):
        publish(kit)
        script = (kit["store"] / "windows" / "get.ps1").read_text(encoding="utf-8")
        assert "[string]$BaseUrl = 'https://downloads.example.com/windows'" in script
        assert "__VEDHA_DOWNLOAD_BASE__" not in script.split("param(")[1].split(")")[0]
        # the source file in the repo keeps its placeholder
        assert "__VEDHA_DOWNLOAD_BASE__" in GET.read_text(encoding="utf-8")

    def test_the_sidecar_hash_file_matches(self, kit):
        publish(kit)
        side = (kit["store"] / "windows" / "2.2.2" / "vedha-agent-win.zip.sha256").read_text(encoding="utf-8")
        assert side.split()[0] == kit["sha"]

    def test_no_latest(self, kit):
        r = publish(kit, "--no-latest", "--distribution-id", "E1")
        assert r.returncode == 0
        assert not any("latest.json" in c and c.startswith("s3 cp") for c in calls(kit))
        assert any(c.endswith("--paths /windows/get.ps1") for c in calls(kit))

    def test_a_published_version_is_not_overwritten(self, kit):
        env = dict(kit["env"], FAKE_AWS_EXISTS="1")
        r = publish(kit, env=env)
        assert r.returncode != 0 and "already published" in r.stderr
        assert not any(c.startswith("s3 cp") for c in calls(kit))

    def test_force_replaces_it(self, kit):
        env = dict(kit["env"], FAKE_AWS_EXISTS="1")
        r = publish(kit, "--force", env=env)
        assert r.returncode == 0 and "WARNING" in r.stdout
        assert any(c.startswith("s3 cp") for c in calls(kit))

    def test_a_zip_that_is_not_the_one_in_the_release_file_is_refused_before_any_aws_call(self, kit):
        kit["zip"].write_bytes(kit["zip"].read_bytes() + b"x")
        r = publish(kit)
        assert r.returncode != 0 and ("SHA-256" in r.stderr or "size" in r.stderr)
        assert calls(kit) == []

    def test_dry_run_calls_nothing_and_needs_no_aws(self, kit):
        env = dict(kit["env"], PATH=os.environ["PATH"])        # no shim: `aws` may not even exist
        r = publish(kit, "--dry-run", env=env)
        assert r.returncode == 0, r.stderr
        assert "[dry run]" in r.stdout and calls(kit) == []

    @pytest.mark.parametrize("base_url", ["http://downloads.example.com/windows", "downloads.example.com", "https://x.example.com/a b"])
    def test_a_bad_base_url_is_refused(self, kit, base_url):
        r = publish(kit, base_url=base_url)
        assert r.returncode != 0 and calls(kit) == []

    @pytest.mark.parametrize("prefix", ["../x", "/abs", "a b", ""])
    def test_a_bad_prefix_is_refused(self, kit, prefix):
        r = publish(kit, "--prefix", prefix)
        assert r.returncode != 0 and calls(kit) == []

    def test_missing_options_are_named(self, kit):
        r = subprocess.run(["bash", str(PUBLISH), "--zip", str(kit["zip"])], capture_output=True, text=True, env=kit["env"], timeout=30)
        assert r.returncode != 0 and "--bucket" in r.stderr

    def test_profile_and_region_reach_every_aws_call(self, kit):
        publish(kit, "--profile", "vedha", "--region", "ap-south-1", "--distribution-id", "E1")
        assert calls(kit) and all(c.startswith("--profile vedha --region ap-south-1 ") for c in calls(kit))


# ── get.ps1: the safety properties ─────────────────────────────────────────────────────────────────

class TestBootstrapScript:
    text = GET.read_text(encoding="utf-8")

    def test_ascii_only(self):
        # Windows PowerShell 5.1 reads a BOM-less file as the ANSI code page, so non-ASCII text can corrupt it
        assert self.text.isascii()

    def test_it_refuses_to_run_without_administrator_rights_instead_of_raising_its_own(self):
        assert "Test-GetIsAdmin" in self.text and "Open PowerShell as Administrator" in self.text
        assert "RunAs" not in self.text

    def test_it_requires_a_pinned_hash_and_a_version_by_default(self):
        assert "needs the package's SHA-256" in self.text and "needs the package version" in self.text

    def test_it_verifies_before_unpacking_and_never_through_cmd(self):
        assert self.text.index("Get-GetSha256 $zipPath") < self.text.index("ExtractToDirectory")
        code = "\n".join(l for l in self.text.splitlines() if not l.lstrip().startswith("#"))
        assert "cmd.exe" not in code.lower() and "install.cmd" not in code.lower()

    def test_the_unpack_folder_is_locked_to_system_and_administrators_by_sid(self):
        assert "*S-1-5-18" in self.text and "*S-1-5-32-544" in self.text

    def test_http_is_only_for_this_computer(self):
        assert "127\\.0\\.0\\.1|localhost" in self.text

    @pytest.mark.parametrize("forbidden", [
        "Add-MpPreference", "Set-MpPreference", "Set-ExecutionPolicy", "netsh", "New-NetFirewallRule",
        "Import-Certificate", "certutil", "Invoke-Expression", "iex ", "DownloadString",
    ])
    def test_it_never_touches_security_settings_or_evals_downloaded_text(self, forbidden):
        # (comments and messages may mention these words; code must not call them)
        code = "\n".join(l for l in self.text.splitlines() if not l.lstrip().startswith("#"))
        assert forbidden not in code

    def test_the_build_checks_it_on_windows(self):
        workflow = (PROBE.parent / ".github" / "workflows" / "agent-windows-build.yml").read_text(encoding="utf-8")
        for needle in ("windows\\hosting\\get.ps1", "Test-Get.ps1", "vedha-agent-win.release.json"):
            assert needle in workflow, needle

    def test_packaging_writes_the_release_file(self):
        text = (PROBE / "windows" / "package-zip.ps1").read_text(encoding="utf-8")
        for needle in ("release.json", "AGENT_VERSION", "exe_sha256", "$zipHash"):
            assert needle in text, needle


# ── the CloudFormation template ──────────────────────────────────────────────────────────────────────

yaml = pytest.importorskip("yaml")


def load_template():
    class Loader(yaml.SafeLoader):
        pass

    def any_tag(loader, suffix, node):
        if isinstance(node, yaml.ScalarNode):
            value = loader.construct_scalar(node)
        elif isinstance(node, yaml.SequenceNode):
            value = loader.construct_sequence(node, deep=True)
        else:
            value = loader.construct_mapping(node, deep=True)
        return {f"!{suffix}": value}

    Loader.add_multi_constructor("!", any_tag)
    return yaml.load((HOSTING / "cloudformation.yaml").read_text(encoding="utf-8"), Loader=Loader)


class TestCloudFormation:
    t = load_template()
    r = t["Resources"]

    def test_the_bucket_is_private_encrypted_and_versioned(self):
        props = self.r["Bucket"]["Properties"]
        assert all(props["PublicAccessBlockConfiguration"].values()) and len(props["PublicAccessBlockConfiguration"]) == 4
        assert props["BucketEncryption"]["ServerSideEncryptionConfiguration"][0]["ServerSideEncryptionByDefault"]["SSEAlgorithm"] == "AES256"
        assert props["VersioningConfiguration"]["Status"] == "Enabled"
        assert self.r["Bucket"]["DeletionPolicy"] == "Retain"          # deleting the stack must not delete the packages

    def test_only_cloudfront_may_read_and_plain_http_is_denied(self):
        statements = self.r["BucketPolicy"]["Properties"]["PolicyDocument"]["Statement"]
        allow = next(s for s in statements if s["Effect"] == "Allow")
        assert allow["Principal"] == {"Service": "cloudfront.amazonaws.com"} and allow["Action"] == "s3:GetObject"
        assert "AWS:SourceArn" in allow["Condition"]["StringEquals"]
        deny = next(s for s in statements if s["Effect"] == "Deny")
        assert deny["Condition"]["Bool"]["aws:SecureTransport"] == "false"

    def test_cloudfront_signs_its_requests_and_redirects_to_https(self):
        oac = self.r["OriginAccessControl"]["Properties"]["OriginAccessControlConfig"]
        assert oac["SigningBehavior"] == "always" and oac["SigningProtocol"] == "sigv4" and oac["OriginAccessControlOriginType"] == "s3"
        cfg = self.r["Distribution"]["Properties"]["DistributionConfig"]
        behavior = cfg["DefaultCacheBehavior"]
        assert behavior["ViewerProtocolPolicy"] == "redirect-to-https" and behavior["AllowedMethods"] == ["GET", "HEAD"]
        assert cfg["Origins"][0]["S3OriginConfig"] == {"OriginAccessIdentity": ""}
        # a custom domain must not weaken TLS
        cert = cfg["ViewerCertificate"]["!If"][1]
        assert cert["MinimumProtocolVersion"] == "TLSv1.2_2021"

    def test_the_publisher_can_only_write_the_windows_prefix(self):
        statements = self.r["PublisherPolicy"]["Properties"]["PolicyDocument"]["Statement"]
        write = next(s for s in statements if s["Sid"] == "WriteWindowsPrefix")
        assert write["Resource"] == {"!Sub": "${Bucket.Arn}/windows/*"}
        assert set(write["Action"]) == {"s3:PutObject", "s3:GetObject"}
        everything = json.dumps(statements)
        assert "s3:*" not in everything and "DeleteObject" not in everything

    def test_the_outputs_feed_the_publish_script(self):
        assert {"BucketName", "DistributionId", "DistributionDomain", "DownloadBaseUrl", "PublisherPolicyArn"} <= set(self.t["Outputs"])
        assert "https://" in json.dumps(self.t["Outputs"]["DownloadBaseUrl"]) and "/windows" in json.dumps(self.t["Outputs"]["DownloadBaseUrl"])
