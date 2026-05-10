# GitHub PAT: Classic vs Fine-Grained

Reference for diagnosing "git push 403" with `github_pat_*` tokens.

## Quick Identification

| Prefix | Type | Default write? |
|--------|------|----------------|
| `ghp_*` | Classic PAT | Yes (with `repo` scope) |
| `github_pat_*` | Fine-grained PAT | **NO** (must explicitly grant per permission) |

## Fine-Grained PAT Triage

When a user provides a `github_pat_*` token and `git push` returns 403:

### Step 1: Check if token can read
```bash
curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/user
# Should return user JSON
```

### Step 2: Check repo permissions from API
```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO" | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin).get('permissions',{}), indent=2))"
```

If `push: true` appears but push still fails → token has metadata permission but not **Contents: Write**. The `permissions` object reflects user permissions, not token permissions.

### Step 3: Test write via API
```bash
# Try creating a file via the Contents API
curl -s -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/$OWNER/$REPO/contents/test.txt" \
  -d '{"message":"test","content":"dGVzdA=="}'
```

HTTP 403 "Resource not accessible by personal access token" → token lacks **Contents: Read and write**.

### Fix for user
Direct them to: https://github.com/settings/tokens?type=beta
1. Click the token
2. Under "Repository permissions" → find "Contents"
3. Change from "Read" to **"Read and write"**
4. Click "Update token"

No token regeneration needed — permissions are updated in-place.

## Classic PAT Triage

If `ghp_*` token fails:
1. Check `X-OAuth-Scopes` header: `curl -sI -H "Authorization: Bearer $TOKEN" https://api.github.com/user | grep X-OAuth-Scopes`
2. Must include `repo` for push access
3. Classic PATs cannot be edited — must regenerate

## Container-Specific: Token in Remote URL

When credential store (`~/.git-credentials`) doesn't work due to Docker HOME path mismatches:
```bash
git remote set-url origin "https://$USERNAME:$TOKEN@github.com/$OWNER/$REPO.git"
```
This is reliable for cron scripts and automated backups where credential files may not persist.
