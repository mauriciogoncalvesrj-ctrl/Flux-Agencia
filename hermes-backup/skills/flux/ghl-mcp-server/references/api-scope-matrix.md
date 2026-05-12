# GHL API Scope Matrix

## Two token scopes, one `pit-` prefix

Both Agency and Location Private Integration tokens use the `pit-` prefix. They are **not interchangeable**.

## Agency Token (`GHL_AGENCY_API_KEY`)

Generated at: Agency-level Settings → API  
Grants access to:

| Endpoint | Method | Works |
|---|---|---|
| `/locations/search?companyId=...` | GET | ✅ |
| `/locations/{locationId}` | GET | ✅ |
| `/oauth/locationToken` | POST | ❌ 401 |
| `/contacts/?locationId=...` | GET | ❌ 401 "not authorized for this scope" |
| `/pipelines/?locationId=...` | GET | ❌ 401 "not authorized for this scope" |
| `/calendars/?locationId=...` | GET | ❌ 401 |
| `/conversations/?locationId=...` | GET | ❌ 401 |

Also returns `401 "Token's user type mismatch!"` on some user-level endpoints.

## Location Private Integration Token (`GHL_API_KEY`)

Generated at: Sub-account Settings → Integrations → Private Integrations  
Scopes selected at creation (contacts.read, opportunities.read, calendars.read, etc.)  
Grants access to all location-scoped endpoints that the MCP server needs.

Must include scopes: `contacts.read`, `contacts.write`, `opportunities.read`, `opportunities.write`, `calendars.read`, `conversations.read`, `conversations.write`, `users.read`, `pipelines.read`, `pipelines.write` (and others as needed).

## Current state (Flux VPS)

- `/opt/data/.env` has `GHL_API_KEY` = `GHL_AGENCY_API_KEY` (same Agency token `pit-8409c0...`)  
- **Result**: All 563+ MCP tools that hit location endpoints return 401  
- **Fix needed**: Generate a new Location Private Integration token inside the Flux sub-account at GHL Settings → Integrations → Private Integrations, then replace `GHL_API_KEY` in `.env` and restart the MCP server.

## Debugging quick check

```bash
# Verify keys are different
GHL_API=$(grep "^GHL_API_KEY=" /opt/data/.env | cut -d= -f2)
GHL_AGENCY=$(grep "^GHL_AGENCY_API_KEY=" /opt/data/.env | cut -d= -f2)
[ "$GHL_API" = "$GHL_AGENCY" ] && echo "PROBLEM: keys are identical (agency key duplicated)" || echo "OK: keys differ"

# Test agency scope (should work)
curl -s -H "Authorization: Bearer $GHL_AGENCY" -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/locations/search?companyId=0-302-583&limit=1"

# Test location scope (will 401 if using agency key)
curl -s -H "Authorization: Bearer $GHL_API" -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/contacts/?locationId=qhKd29hCIeOS3TAcA9FW&limit=1"
```

## Flux sub-accounts (as of 2025-05-11)

| Name | Location ID |
|---|---|
| Flux (agência) | qhKd29hCIeOS3TAcA9FW |
| Borgatte Móveis Sob Medida | CpkKNuUhzR5i5GgjhOkg |
| Clínica Larissa Manso | KZEJKLYOfQKtrO9F0WZ7 |
| Clínica Nathalia Vidal | R0UfFkcxS4Q4p11xSqlT |
| FLUX-MODELO-PADRÃO-ESTÉTICA | 5cAjCredIOuc6jIgtnCB |
| GRUPO ACEL | sUpC1XCyLH8TTmE4rj06 |
| LCX DIGITAL | F7jDGmE1uJLmzIE6So26 |
| Luana Sampaio Cajamar | ONrN4yy0eCfmNbzlnLFc |
| Luana Sampaio Jundiaí | VRqgysb9cvBAO6P0UGlL |
| PROTON MEDIA TENSAO EIRELI – EPP | ILbWTQkk5PF42vqxDBKg |
| TEMPLATE - Móveis Planejados - Padrão | 89kyyVLikZ2jbksI1N4I |