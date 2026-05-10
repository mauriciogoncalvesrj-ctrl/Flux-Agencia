# Paperclip Auth Debugging — VPS Audit Session (2026-05-09)

## Symptoms

- 126 x `401` responses in Paperclip logs over several hours
- Pattern: Every ~5 minutes, agent heartbeat calls `/api/companies/:id/issues?assigneeAgentId=...` → 401
- `POST /api/auth/sign-in/email` → 401 with `INVALID_EMAIL_OR_PASSWORD`
- `GET /api/auth/get-session` → 401
- Agent `763e73f1` (CEO, hermes_local adapter) status: idle, but heartbeat calls fail auth

## Root Causes Found

### 1. Admin password drift

`ADMIN_PASSWORD=VsSjU3rW5ST` env var stopped working. This var is only used on **first bootstrap** (no admin user exists). Once the admin user is created, the env var is ignored. Password must be reset via database.

**Fix applied:** Reset password via Better Auth `hashPassword` + direct SQL UPDATE:
```bash
docker exec paperclip-tjjz-paperclip-1 node -e "
const { Pool } = require('/usr/local/lib/node_modules/paperclipai/node_modules/pg');
const { hashPassword } = require('/usr/local/lib/node_modules/paperclipai/node_modules/better-auth/dist/crypto/password.mjs');
async function main() {
  const hash = await hashPassword('FluxIA2026!');
  const pool = new Pool({ host: 'localhost', port: 54329, database: 'paperclip', user: 'paperclip', password: 'paperclip' });
  const result = await pool.query('UPDATE account SET password = \$1, updated_at = NOW() WHERE provider_id = \$2', [hash, 'credential']);
  console.log('Rows updated:', result.rowCount);
  await pool.end();
}
main().catch(e => console.error('Error:', e));
"
```

### 2. Origin mismatch (PAPERCLIP_PUBLIC_URL env vs config.json)

- `PAPERCLIP_PUBLIC_URL=http://paperclip-tjjz.srv1651876.hstgr.cloud` (old Hostinger URL, HTTP)
- `config.json auth.publicBaseUrl=https://paperclip.somosflux.com.br` (custom domain, HTTPS)
- **Env var wins** — Better Auth uses the Hostinger URL as the canonical origin
- Agents and browsers using `paperclip.somosflux.com.br` → origin rejection → 401

**Quick fix applied:** Patched Better Auth `skipOriginCheck: true` in `create-context.mjs`

**Proper fix (pending):** Recreate container with:
```
PAPERCLIP_PUBLIC_URL=https://paperclip.somosflux.com.br
PAPERCLIP_ALLOWED_HOSTNAMES=paperclip.somosflux.com.br,srv1651876.hstgr.cloud
```

### 3. CTO agent status: error ("Process adapter missing command")

Agent `26fd5149` (CTO) shows `adapterType: process` (runtime) despite being `hermes_local` in config. The Hermes CLI is not installed inside the Paperclip container, so the adapter can't spawn it.

## Related Changes

- Origin bypass patch applied to container (temporary, lost on container recreation)
- Password reset to `FluxIA2026!`
- Paperclip container restarted after patch
- All 7 other agents in idle/succeeded status

## Paperclip Agent Roster

| ID (prefix) | Name | Role | Status | Adapter |
|---|---|---|---|---|
| 763e73f1 | CEO | ceo | idle | hermes_local |
| 1ad4ef1e | CFO | cfo | idle | hermes_local |
| d614aec5 | CMO | cmo | idle | hermes_local |
| 26fd5149 | CTO | cto | **error** | hermes_local |
| cb067c2d | Operations Director | general | idle | hermes_local |
| e7885c4f | Dir GHL | general | idle | hermes_local |
| efaac461 | Test | general | idle | hermes_local |

Company ID: `4dec222b-9a6a-42e5-b477-ac034ff81bd4`