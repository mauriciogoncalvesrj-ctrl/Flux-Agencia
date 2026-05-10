# Paperclip Auth Debugging — Session 2026-05-09

## Problem

User (Mauricio/Flux) could not log into Paperclip at `https://paperclip.somosflux.com.br/auth?next=%2F`. Error: "invalid username or password".

## Root Cause (Dual Issue)

### Issue 1: Origin Blocked (403 Invalid origin)

Better Auth was rejecting requests from `https://paperclip.somosflux.com.br` because the trusted origin was derived from `PAPERCLIP_PUBLIC_URL=http://paperclip-tjjz.srv1651876.hstgr.cloud` (the Hostinger auto-generated URL).

**Log evidence:**
```
ERROR [Better Auth]: Invalid origin: https://paperclip.somosflux.com.br
POST /api/auth/sign-in/email 403
```

The 403 (not 401) is the key indicator — the request is blocked before credential validation even happens.

### Issue 2: Wrong Password (401)

Even when bypassing the origin check by testing directly via Docker network with a trusted origin, the credentials from env vars (`ADMIN_PASSWORD=VsSjU3rW5ST`) returned 401. The password had likely been changed or the bootstrap used different values.

## Environment at Time of Debugging

```json
{
  "PAPERCLIP_DEPLOYMENT_MODE": "authenticated",
  "PAPERCLIP_PUBLIC_URL": "http://paperclip-tjjz.srv1651876.hstgr.cloud",
  "PAPERCLIP_ALLOWED_HOSTNAMES": "srv1651876.hstgr.cloud,2.24.85.2:57186",
  "ADMIN_EMAIL": "mauriciogoncalvesrj@gmail.com",
  "ADMIN_PASSWORD": "VsSjU3rW5ST"
}
```

Config.json `auth.publicBaseUrl` was correctly set to `https://paperclip.somosflux.com.br` but was being IGNORED because the env var `PAPERCLIP_PUBLIC_URL` takes precedence in `resolveBaseUrl()`.

## Database Investigation

### User table
```json
[{"id":"jH0DEnVL2ZbjwSrpyI589vlFzRGJPr2e","name":"Mauricio Flux","email":"mauriciogoncalvesrj@gmail.com"}]
```

### Account table (Better Auth credentials)
```
id: nB0Hw6MEJg9wH7lHyv0iya2ecQUwK0b0
account_id: jH0DEnVL2ZbjwSrpyI589vlFzRGJPr2e
provider_id: credential
user_id: jH0DEnVL2ZbjwSrpyI589vlFzRGJPr2e
password: a40c35e2dd58b951bd5e6246cab2afc5:39c0c8b4a3a30ee90... (scrypt hash)
```

## Password Reset

1. Located Better Auth's `hashPassword` function at:
   `/usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/crypto/password.mjs`

2. Hash algorithm: scrypt with N=16384, r=16, p=1, dkLen=64

3. Generated new hash for password `Flux2026!` and updated the `account` table directly

4. Verified login works via localhost:
   ```bash
   curl -s -X POST "http://localhost:3100/api/auth/sign-in/email" \
     -H "Content-Type: application/json" \
     -H "Origin: http://localhost:3100" \
     -d '{"email":"mauriciogoncalvesrj@gmail.com","password":"Flux2026!"}'
   # Response: {"redirect":false,"token":"...","user":{...}}
   ```

## resolveBaseUrl() Function Logic

Discovered by reading the bundled dist file at line 9364:

```js
function resolveBaseUrl(configPath, explicitBaseUrl) {
  if (explicitBaseUrl) return explicitBaseUrl...
  const fromEnv = process.env.PAPERCLIP_PUBLIC_URL 
    ?? process.env.PAPERCLIP_AUTH_PUBLIC_BASE_URL 
    ?? process.env.BETTER_AUTH_URL 
    ?? process.env.BETTER_AUTH_BASE_URL;
  if (fromEnv?.trim()) return fromEnv.trim()...
  const config = readConfig(configPath);
  if (config?.auth.baseUrlMode === "explicit" && config.auth.publicBaseUrl) {
    return config.auth.publicBaseUrl...
  }
  // fallback: construct from host:port
}
```

**Key finding:** env vars are checked BEFORE config.json. Setting `auth.publicBaseUrl` in config.json has no effect when `PAPERCLIP_PUBLIC_URL` env var is set.

## Runtime Config Construction (line 10680-10730)

```js
allowedHostnamesFromEnv = PAPERCLIP_ALLOWED_HOSTNAMES.split(",")
hostnameFromPublicUrl = new URL(publicUrl).hostname
allowedHostnames = [...allowedHostnamesFromEnv, hostnameFromPublicUrl]
```

Config.json's `server.allowedHostnames` array is NOT read at runtime — only during `paperclipai onboard` bootstrap.

## Trusted Origins for Better Auth (line 11282-11335)

```js
publicUrl = PAPERCLIP_PUBLIC_URL ?? ... ?? config?.auth?.publicBaseUrl ?? ""
trustedOriginsDefault = new URL(publicUrl).origin
BETTER_AUTH_TRUSTED_ORIGINS = process.env.BETTER_AUTH_TRUSTED_ORIGINS ?? trustedOriginsDefault
```

So the trusted origin is always derived from the env var if set.

## Permanent Fix Required

User must update Hostinger panel env vars and recreate the container:

```
PAPERCLIP_PUBLIC_URL=https://paperclip.somosflux.com.br
PAPERCLIP_ALLOWED_HOSTNAMES=paperclip.somosflux.com.br,srv1651876.hstgr.cloud
```

## Quick Test for Future Sessions

```bash
# Check current env vars
docker inspect paperclip-tjjz-paperclip-1 --format '{{range .Config.Env}}{{println .}}{{end}}' | grep PAPERCLIP

# Check config.json
docker exec paperclip-tjjz-paperclip-1 cat /paperclip/instances/default/config.json | python3 -m json.tool | grep -A5 '"auth"\|"allowedHostnames"'

# Check recent auth logs
docker logs paperclip-tjjz-paperclip-1 --tail 30 2>&1 | grep -i "origin\|auth\|403\|401"

# Test login via Docker network (bypass origin)
docker exec paperclip-tjjz-paperclip-1 curl -s -X POST "http://localhost:3100/api/auth/sign-in/email" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{"email":"user@email.com","password":"test"}'
```
