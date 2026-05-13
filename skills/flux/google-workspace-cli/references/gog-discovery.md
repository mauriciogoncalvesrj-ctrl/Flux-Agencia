# gog CLI Discovery Notes

## The repo confusion
- ClawHub page says `steipete/gog` → GitHub repo `steipete/gog` is **private/unreachable** (404 on releases API)
- The actual releases are published under **`openclaw/gogcli`**
- The `steipete/gog` repo may be the source or an older private fork, but the public distribution channel is `openclaw/gogcli`

## Finding the correct release

```bash
# This works
curl -sL -A "Mozilla/5.0" \
  "https://api.github.com/repos/openclaw/gogcli/releases/latest" | \
  python3 -m json.tool
```

Assets pattern:
- `gogcli_X.Y.Z_linux_amd64.tar.gz`
- `gogcli_X.Y.Z_linux_arm64.tar.gz`
- `gogcli_X.Y.Z_darwin_amd64.tar.gz`
- `gogcli_X.Y.Z_darwin_arm64.tar.gz`
- `gogcli_X.Y.Z_windows_amd64.zip`
- `checksums.txt`

## Contents of the tarball
```
CHANGELOG.md
LICENSE
README.md
gog
```

Only `gog` is needed; the binary is self-contained Go (~31MB).

## Version as of this session
- v0.16.0 (280eea7) — May 10, 2026
- SHA256: `46c8ffa71a4e425e6885b926f1c67be7899f444c9e254ae8da9c46ea297a6bda`
