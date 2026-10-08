# Hosting the Windows agent on S3: a customer installs with one command

Goal: a customer opens an **Administrator PowerShell**, pastes **one line**, and the agent is downloaded,
checked and installed. Everything below is in `probe/windows/hosting/`.

> **Status.** The scripts and the tests are done and run on a real Windows runner against a local web
> server. The CloudFormation template is checked for structure only. **Nothing has been deployed to
> AWS yet** (this repository has no AWS access): you run the setup in section 3 once. Section 9 lists
> exactly what is and is not proven.

Related: [operator guide](../probe/WINDOWS_AGENT_INSTALL.md) · [reference](../probe/WINDOWS_AGENT_REFERENCE.md) ·
[ADR-0005](../adr/0005-windows-agent-delivery.md) (D14) · [pipeline](../planning/2026-10-07-windows-agent-pipeline.md).

## 1. What the customer does

```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm https://DOWNLOADS/windows/get.ps1))) -Version 2.2.2 -Sha256 <64 hex> -Token vet_XXXXXXXX
```

(or the `curl.exe` form in section 6). That is all. The command already contains the version, the
package's SHA-256 and the one-time token, because **you** generate it (section 5).

## 2. How it works

```
  you (once per release)                         AWS                                 customer
  ----------------------                         ---                                 --------
  GitHub: build the package  ->  artifact
  publish-to-s3.sh  --------->  S3 (private) <--- CloudFront (HTTPS only) <----- get.ps1  -> download zip
                                  windows/get.ps1                                         -> check SHA-256 against the command
                                  windows/latest.json                                     -> unpack in an admin-only folder
                                  windows/2.2.2/vedha-agent-win.zip                       -> run install.ps1 -> agent online
                                  windows/2.2.2/vedha-agent-win.zip.sha256                -> delete the downloaded files
                                  windows/2.2.2/release.json
```

Why it is built this way:

| Choice | Reason |
|---|---|
| **The hash travels with the command, not the bucket.** `get.ps1` refuses to run without `-Sha256` and `-Version` | If the bucket (or the network path, or a proxy) were tampered with, the downloaded zip would not match the hash you gave the customer, and nothing is installed. The bucket does not have to be trusted |
| **It must be run from an Administrator PowerShell; it never raises its own rights** | A script that re-launches itself as administrator from a folder any user can write to is an easy privilege-escalation target. Opening the elevated prompt yourself means the whole command runs once, with no second prompt, and the unpacked files sit in a folder only SYSTEM and Administrators can touch |
| **The command runs the script in memory** (`[scriptblock]::Create(irm ...)`) rather than saving it first | No file to swap between download and run |
| **Private bucket, read only through CloudFront**, HTTPS only, versions never overwritten | Nothing is publicly listable; a published version cannot silently change |
| **Nothing secret is stored.** The zip holds the compiled agent, the manager address and hashes | The install token is never in the bucket |
| Downloads from PowerShell or curl carry no "downloaded from the internet" mark | SmartScreen's file warning does not apply to them (the build is still unsigned: see section 8) |

## 3. One-time AWS setup (about 15 minutes)

You need the AWS CLI configured for the account (an admin for this first step) and this repository.

**3.1 Choose the address.** Start with the default CloudFront name (`dxxxxxxxx.cloudfront.net`): no
DNS and no certificate, and it works immediately. A name like `downloads.vedhasec.com` looks better but
needs a certificate and a DNS record, and **a young domain can be blocked by customers' web filters**
(see STATUS.md: the categorisation task). You can add a custom name later without changing anything
you published (just publish again with the new `--base-url`).

**3.2 Deploy the stack.** From the repository root:

```bash
aws cloudformation deploy \
  --stack-name vedha-agent-downloads \
  --template-file probe/windows/hosting/cloudformation.yaml \
  --capabilities CAPABILITY_IAM \
  --region ap-south-1 \
  --parameter-overrides PriceClass=PriceClass_200
```

`PriceClass_200` includes Asia (India); `PriceClass_100` (the default) is only the US, Canada and Europe.
The bucket's region is your choice; CloudFront is global.

**3.3 Read the outputs.**

```bash
aws cloudformation describe-stacks --stack-name vedha-agent-downloads --region ap-south-1 \
  --query 'Stacks[0].Outputs[].[OutputKey,OutputValue]' --output table
```

Note `BucketName`, `DistributionId` and `DownloadBaseUrl` (for example `https://d1234abcd.cloudfront.net/windows`).
These are the three values the publish script needs.

**3.4 (Optional) your own domain.**
1. In **us-east-1** (a CloudFront rule, whatever region the stack is in) request an ACM certificate for
   `downloads.example.com` with DNS validation and add the validation record it asks for.
2. Redeploy the stack with `--parameter-overrides DomainName=downloads.example.com CertificateArn=arn:aws:acm:us-east-1:...`.
3. At your DNS provider create `downloads.example.com` as a CNAME to the `DistributionDomain` output.
4. Use `https://downloads.example.com/windows` as `--base-url` from now on.

**3.5 Who may publish.** The stack creates a `PublisherPolicy` (output `PublisherPolicyArn`): it can write
only under `windows/` in this bucket and invalidate this one distribution. Attach it to the IAM user or
role that will run the publish script, rather than using an administrator every time.

## 4. Publish a release (every time you ship a new agent)

1. **Build.** GitHub -> Actions -> *vedha-agent-windows-build* -> Run workflow (keep `manager_url`). Wait for green.
2. **Download the artifact** `vedha-agent-windows` and unzip it. It holds three files:
   `vedha-agent-win.zip`, `vedha-agent-win.zip.sha256`, `vedha-agent-win.release.json`.
3. **Publish** (macOS or Linux, with `aws` and `python3`):

```bash
probe/windows/hosting/publish-to-s3.sh \
  --bucket          <BucketName> \
  --distribution-id <DistributionId> \
  --base-url        <DownloadBaseUrl> \
  --zip     vedha-agent-win.zip \
  --release vedha-agent-win.release.json
# add  --dry-run  first to see exactly what it would do without calling AWS
# add  --profile NAME --region REGION  if you use named AWS profiles
```

What it does: checks the zip against its release file; refuses to overwrite a version that is already
published (bump `AGENT_VERSION` and rebuild instead, or `--force` if you really mean it); uploads the
version folder, then `get.ps1` (with your download address filled in), then `latest.json` last;
invalidates the CloudFront copies of `get.ps1` and `latest.json`; and prints the commands for the customer.

4. **Try it** on a clean Windows machine you control before sending anything to a customer (section 5, with a test token).

## 5. Hand a customer their command

1. Create a one-time install token ([operator guide, section 2](../probe/WINDOWS_AGENT_INSTALL.md#2-create-the-customers-install-token)).
2. Take the command the publish script printed and replace `<TOKEN>` with it. The version and hash are already filled in.
3. Send the command to the customer **by a different channel** from anything else about the engagement
   (chat or phone, not the same email that explains the project), and tell them to run it in an
   **Administrator** PowerShell (right-click Start -> *Terminal (Admin)* or *Windows PowerShell (Admin)*).
4. Options to add to the end of the command when needed: `-Proxy http://proxy:3128`, `-Scope 10.0.5.0/24`,
   `-Name HQ-scanner`, `-CaBundle C:\certs\root.pem`. Anything else (for example `-SkipPreflight`) is passed
   straight to the installer; see the [reference](../probe/WINDOWS_AGENT_REFERENCE.md#7-the-installer).

## 6. The two command forms

**PowerShell** (works on every supported Windows):

```
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm https://DOWNLOADS/windows/get.ps1))) -Version 2.2.2 -Sha256 <64 hex> -Token <TOKEN>
```

The first statement makes older Windows PowerShell use TLS 1.2, which CloudFront requires.

**Command Prompt with `curl.exe`** (Windows 10 1803 / Server 2019 or newer; older servers use the form above):

```
curl.exe -fsSL https://DOWNLOADS/windows/get.ps1 -o "%SystemRoot%\Temp\vedha-get.ps1" && powershell -NoProfile -ExecutionPolicy Bypass -File "%SystemRoot%\Temp\vedha-get.ps1" -Version 2.2.2 -Sha256 <64 hex> -Token <TOKEN>
```

This saves the script to disk first. `C:\Windows\Temp` is used because a standard user cannot modify an
administrator's file there.

**Read it first (recommended for customers with endpoint protection).** A command that downloads text and
runs it from memory is exactly what malware does, so some security products **flag or block that pattern
whatever the script is**. Give such customers this instead:

```
curl.exe -fsSL https://DOWNLOADS/windows/get.ps1 -o get.ps1
notepad get.ps1                    # read it; it is about 250 lines and changes no security setting
powershell -NoProfile -ExecutionPolicy Bypass -File .\get.ps1 -Version 2.2.2 -Sha256 <64 hex> -Token <TOKEN>
```

or the original route: send them the zip and `install.cmd -Token ...` ([operator guide](../probe/WINDOWS_AGENT_INSTALL.md)).

## 7. Operating it

| Task | How |
|---|---|
| Roll back to the previous version | Upload that version's `release.json` as `latest.json`: `aws s3 cp s3://BUCKET/windows/2.2.1/release.json s3://BUCKET/windows/latest.json --cache-control "no-cache, max-age=0" --content-type application/json`, then invalidate `/windows/latest.json`. Commands you already handed out carry their own version and hash, so they keep working |
| Withdraw a bad version | `aws s3 rm s3://BUCKET/windows/2.2.2/ --recursive`; commands that name it then stop working ("Could not download") |
| See what is published | `aws s3 ls s3://BUCKET/windows/ --recursive` |
| A customer lost their command | Make a new token and give the same command with the new token. The old token is single-use and expires |
| Cost | A pay-per-use bucket and CDN; the main cost is data transfer, about the package size (about 30 MB) per install. See the AWS pricing pages for current rates |
| Remove everything | Empty the bucket, then delete the stack (the bucket is set to be **retained**, so deleting the stack does not delete your packages) |

## 8. Honest limits

- **The build is not code-signed.** S3 does not change that. SmartScreen and some endpoint products may still warn or block.
- **`latest.json` is only a convenience** (`-TrustHostedHash`, for tests and internal use). Customer commands should always pin the hash.
- **One package, one manager.** The manager address is baked into the zip, so a different manager needs its own build and its own prefix (`--prefix`).
- A web filter can block a young custom domain or `cloudfront.net`; the fallback is the zip route.
- This route does not use the manager at all. A manager-served download with an update path is a later step ([pipeline L1, L2](../planning/2026-10-07-windows-agent-pipeline.md)).

## 9. What is proven, and what is not

| | |
|---|---|
| Proven (tests in this repo) | The publish script against a fake `aws` (41 Python tests: order, cache headers, hash fill-in, immutability, refusal cases, dry run); `get.ps1`'s checks and its full download, hash check and unpack against a local web server, under PowerShell 7 and Windows PowerShell 5.1 (51 tests); on a real Windows runner, the **hosted install end to end** (wrong hash refused and nothing installed; one command installs; removed again) |
| Checked structurally only | The CloudFormation template (private bucket, blocked public access, CloudFront-only read, HTTPS-only, signed origin requests, least-privilege publisher). It has **not** been deployed, and `aws cloudformation validate-template` has not been run |
| Not tried | A real S3 + CloudFront deployment; the CloudFront default certificate and TLS behaviour from an old Windows; a customer's proxy or TLS inspection with this download; endpoint-protection reaction to the in-memory command; invalidation timing |

Do a first full run yourself (sections 3-5, with a test token on a clean VM) and tell Claude what breaks.

## 10. Troubleshooting

| What the customer sees | Meaning | Fix |
|---|---|---|
| `Open PowerShell as Administrator ...` | not elevated | open an elevated prompt and run the same command |
| `This command needs the package's SHA-256` / `needs the package version` | the command was cut short | copy the whole command again |
| `Could not download ... 403` | the bucket policy or CloudFront origin access is not in place, or the version was withdrawn | check the stack deployed; `aws s3 ls` the key |
| `Could not download ... 404` | wrong version in the command, or not published yet | publish it, or fix the command |
| `Could not download ...` (timeout, TLS) | firewall, proxy or TLS inspection on the download address | allow the address, add `-Proxy`, or use the zip route |
| `The downloaded package does not match the SHA-256 in your command` | the file was altered or truncated, or the command is for another build | **do not use it**; check the command's version and hash match the published release; republish if needed |
| `Could not create SSL/TLS secure channel` | an old Windows PowerShell without TLS 1.2 | use the PowerShell form, whose first statement turns TLS 1.2 on |
| The command is blocked or the window closes at once | endpoint protection blocked the in-memory download | use the "read it first" form or the zip route, and give their security team `ALLOWLIST.txt` |
| Anything after the download (checks, connection) | the normal installer | see the [operator guide, section 5](../probe/WINDOWS_AGENT_INSTALL.md#5-when-something-is-wrong) |
