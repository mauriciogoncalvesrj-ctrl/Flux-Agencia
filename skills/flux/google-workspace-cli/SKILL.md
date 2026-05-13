---
name: google-workspace-cli
title: Google Workspace CLI (gog) Setup
description: Install and configure the gog CLI for Google Workspace access (Gmail, Calendar, Drive, Sheets, Docs, Contacts, Ads, Analytics, etc.) on a headless Linux server/agent environment.
trigger: When the user needs to install gog, configure Google Workspace OAuth, or set up Google API access from Hermes/VPS for Gmail, Drive, Calendar, Sheets, Docs, Contacts, Ads, Analytics, Search Console, or Meet.
---

# Google Workspace CLI (gog) Setup

## Purpose
Install the `gog` binary and configure OAuth so Hermes can programmatically access Google Workspace services from a headless VPS.

## Prerequisites
- Linux server with internet access
- A Google Cloud project with OAuth 2.0 credentials (desktop/installed app type)
- The `client_secret.json` file downloaded from Google Cloud Console

## Step-by-Step

### 1. Find the correct release

⚠️ **Pitfall**: The GitHub repo is `openclaw/gogcli`, not `steipete/gog`.
The `steipete/gog` repo is private/archived. Releases are published under the `openclaw` organization.

```bash
# List latest release assets
curl -sL -A "Mozilla/5.0" \
  "https://api.github.com/repos/openclaw/gogcli/releases/latest" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); [print(a['name'], a['browser_download_url']) for a in d.get('assets', [])]"
```

### 2. Download and install

```bash
cd /tmp
VERSION="0.16.0"  # update as needed
ARCH="linux_amd64"
TARBALL="gogcli_${VERSION}_${ARCH}.tar.gz"

# Download
curl -sLO "https://github.com/openclaw/gogcli/releases/download/v${VERSION}/${TARBALL}"

# Verify checksum (optional but recommended)
curl -sLO "https://github.com/openclaw/gogcli/releases/download/v${VERSION}/checksums.txt"
sha256sum -c checksums.txt 2>/dev/null | grep "${TARBALL}"

# Extract and install
tar -xzf "${TARBALL}"
mkdir -p ~/.local/bin
mv gog ~/.local/bin/gog
chmod +x ~/.local/bin/gog

# Ensure PATH
if ! grep -q '\.local/bin' ~/.bashrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
fi
source ~/.bashrc
which gog && gog --version
```

### 3. Configure OAuth credentials

Place the `client_secret.json` (from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0 Client ID → Download JSON) into the gog config directory:

```bash
mkdir -p ~/.config/gogcli
cp /path/to/client_secret.json ~/.config/gogcli/client_secret.json
gog auth credentials set ~/.config/gogcli/client_secret.json --json
```

Expected output: `{"client": "default", "saved": true}`.

### 4. Headless OAuth authorization (server-friendly flow)

Since Hermes runs headless, use the `--remote` flow instead of opening a local browser.

**Step 1 — generate the auth URL:**
```bash
gog auth add "USER_EMAIL" \
  --remote --step 1 \
  --services gmail,calendar,drive,docs,slides,sheets,contacts,tasks,people,forms,meet,analytics,searchconsole,ads,youtube \
  --json
```

This prints a URL. The user must open it in their browser, authenticate, and then copy the **final redirect URL** from the browser address bar after Google redirects back.

**Step 2 — exchange the redirect URL for a token:**
```bash
gog auth add "USER_EMAIL" \
  --remote --step 2 \
  --auth-url "PASTE_REDIRECT_URL_HERE" \
  --services gmail,calendar,drive,docs,slides,sheets,contacts,tasks,people,forms,meet,analytics,searchconsole,ads,youtube \
  --json
```

### 5. Verify

```bash
gog auth list --json
gog auth status --json
gog me --json          # profile info (People API)
```

### 6. Cleanup

```bash
rm -f /tmp/gogcli_*.tar.gz /tmp/checksums.txt /tmp/CHANGELOG.md /tmp/LICENSE /tmp/README.md
```

## Google Cloud Console prerequisites

Before the OAuth flow works, ensure the Google Cloud project has these APIs enabled:

- Gmail API
- Calendar API
- Drive API
- Docs API
- Sheets API
- Slides API
- People API
- Contacts API
- Tasks API
- Forms API
- Meet REST API
- Analytics Admin API + Analytics Data API
- Search Console API
- Google Ads API
- YouTube Data API v3

Also verify the OAuth consent screen is configured (published or in testing with the user's email added as a test user).

## Safety flags for agent use

- `--gmail-no-send` — block send operations entirely
- `--no-input` — fail instead of prompting (CI-safe)
- `-n, --dry-run` — preview changes without executing
- `--readonly` — use read-only scopes where available

## Key config paths

| Path | Purpose |
|------|---------|
| `~/.config/gogcli/config.json` | General config |
| `~/.config/gogcli/credentials.json` | Stored OAuth client secrets |
| `~/.config/gogcli/keyring/` | Encrypted refresh tokens |

## Common commands

```bash
# Gmail
gog gmail search 'newer_than:7d' --max 10 --json
gog gmail send --to a@b.com --subject "Hi" --body "Hello" --account USER_EMAIL

# Calendar
gog calendar events primary --from 2026-05-12T00:00:00Z --to 2026-05-19T00:00:00Z --json

# Drive
gog drive search "query" --max 10 --json
gog drive upload /path/to/file.pdf --account USER_EMAIL

# Sheets
gog sheets get SHEET_ID "Sheet1!A1:D10" --json
gog sheets update SHEET_ID "Sheet1!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED

# Docs
gog docs export DOC_ID --format txt --out /tmp/doc.txt

# Contacts
gog contacts list --max 20 --json
```

## Pitfalls

1. **Wrong repo name**: `steipete/gog` on GitHub is private; releases live at `openclaw/gogcli`.
2. **Missing PATH**: `~/.local/bin` must be in PATH before commands will work in new shells.
3. **OAuth consent screen**: If the project is in "Testing" mode, only added test users can authenticate. Add the user's email under OAuth consent screen → Test users.
4. **Redirect URI mismatch**: The `client_secret.json` must have `http://localhost` in `redirect_uris` for the default manual flow; the `--remote` flow is required on headless servers.
5. **Keyring backend**: If the server has no keyring daemon, `gog` falls back to file-based storage in `~/.config/gogcli/keyring/`. This is normal for VPS environments.
6. **Scope breadth**: Requesting `all` services grants very broad access. Prefer explicit comma-separated `--services` lists for least privilege.

## References
- `references/gog-discovery.md` — how the correct repo and release assets were identified
- `references/google-apis-list.md` — full list of APIs and scopes supported by gog
- `references/headless-oauth-flow.md` — step-by-step headless OAuth workflow for VPS environments
- Homepage: https://gogcli.sh/
- ClawHub page: https://clawhub.ai/steipete/gog
