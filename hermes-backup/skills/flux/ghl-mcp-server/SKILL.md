---
name: ghl-mcp-server
description: Install, configure, test, and troubleshoot the GoHighLevel MCP server (busybee3333/go-high-level-mcp-2026-complete) on the VPS. Gives Hermes Agent direct access to 563+ GHL tools via MCP stdio.
---

# GHL MCP Server — Install & Maintain

## Trigger conditions
- User asks to install, configure, or test GHL MCP integration
- GHL MCP tools are missing or return errors
- User provides GHL credentials and wants to connect

## Prerequisites
- Node.js 18+ (v20.19 on VPS at `/usr/bin/node`)
- Git access to GitHub
- GHL credentials:
  - `GHL_API_KEY` — **Agency API key** (`pit-...` format) works with this server, though docs say Private Integration key. If `pit-` key fails, generate a Private Integration key in GHL Settings → Integrations → Private Integrations.
  - `GHL_LOCATION_ID` — sub-account/location ID (e.g., `qhKd29hCIeOS3TAcA9FW` for Flux)
  - `GHL_BASE_URL` — `https://services.leadconnectorhq.com` (default)

## Installation steps

### 1. Clone and build
```bash
cd /opt/data
git clone https://github.com/busybee3333/go-high-level-mcp-2026-complete.git ghl-mcp
cd ghl-mcp
npm install
npm run build
```
Build compiles TypeScript → `dist/` (~2.5MB). Includes a React UI build step (`src/ui/react-app` → `dist/app-ui/`).

### 2. Add credentials to .env
```bash
echo "GHL_API_KEY=pit-..." >> /opt/data/.env
```
`GHL_LOCATION_ID` should already exist. If not:
```bash
echo "GHL_LOCATION_ID=<location_id>" >> /opt/data/.env
```

### 3. Configure in config.yaml
Add (or update) under `mcp_servers:`:
```yaml
  ghl:
    command: node
    args:
    - /opt/data/ghl-mcp/dist/server.js
    env:
      GHL_API_KEY: ${GHL_API_KEY}
      GHL_BASE_URL: https://services.leadconnectorhq.com
      GHL_LOCATION_ID: ${GHL_LOCATION_ID}
    timeout: 120
    connect_timeout: 60
```
The `server.js` entry uses **stdio transport** (not HTTP). This is the correct entry for Hermes Agent MCP integration.

### 4. Test API key (direct curl)
```bash
curl -s -m 10 \
  -H "Authorization: Bearer pit-..." \
  -H "Version: 2021-07-28" \
  "https://services.leadconnectorhq.com/locations/<LOCATION_ID>"
```
Should return JSON with location details (name, city, website, etc.).

### 5. Test MCP server tools
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | \
  GHL_API_KEY=pit-... \
  GHL_LOCATION_ID=... \
  GHL_BASE_URL=https://services.leadconnectorhq.com \
  timeout 15 node /opt/data/ghl-mcp/dist/server.js 2>/dev/null
```
Should return JSON array of 563+ tools.

### 6. Reload Hermes
After config changes, Hermes needs to reload to pick up new MCP servers. The tools will appear automatically in the next session or after MCP reload.

## What you get
563+ tools across 46 categories: contacts (31), conversations (20), opportunities (10), calendar (14), blog (7), email (5), locations (24), social media (17), store/ecommerce (18+10), payments (20), invoices (39), voice AI (11), agent studio, phone system (15), workflows (8), surveys (9), custom objects (9), associations (10), proposals (4), funnels, forms, and more.

## Credential reference (Flux)
| Variable | Value |
|---|---|
| `GHL_AGENCY_API_KEY` | `pit-8409c09d-e873-4a74-9675-668781b7f708` |
| `GHL_AGENCY_ID` | `0-302-583` |
| `GHL_SNAP_ESTETICA_ID` | `6WSmoPEuyPFa3VXaHpGR` |
| `GHL_LOCATION_ID` | `qhKd29hCIeOS3TAcA9FW` |

## Pitfalls
- **⚠️ Agency key ≠ Location key (CRITICAL)**: GHL has two token scopes: **Agency Token** (`pit-...`) can ONLY access agency-level endpoints (`/locations/search`, `/locations/{id}`). **Location-scoped Private Integration key** is required for 99% of the 563 tools (contacts, pipelines, calendars, conversations, opportunities, etc.). If you see `401 "The token is not authorized for this scope"` or `401 "Token's user type mismatch!"`, the `.env` almost certainly has the Agency key duplicated into `GHL_API_KEY` — they must be DIFFERENT keys. See `references/api-scope-matrix.md`.
- **GHL_API_KEY must be a Location key, not the Agency key**: In `/opt/data/.env`, `GHL_API_KEY` must be a Private Integration token generated **inside the sub-account** (Settings → Integrations → Private Integrations). `GHL_AGENCY_API_KEY` is the agency-level key. Both are `pit-...` format but with different scopes. On 2025-05-11, both keys were set to the same Agency token, causing all location-scoped MCP tool calls to fail with 401.
- **Don't use `npx gohighlevel-mcp`**: That's a different/older package. Use the local build at `/opt/data/ghl-mcp/dist/server.js`.
- **HTTP server is overkill for Hermes**: The project has `main.js` (HTTP/Express) and `server.js` (stdio). For Hermes Agent MCP, use `server.js` (stdio transport).
- **Build required**: TypeScript source won't run directly. Always run `npm run build` after pulling updates.
- **React UI apps are built into dist/app-ui/**: They're for Claude Desktop visual features. Not used by Hermes but the build step includes them.
- **Invalid tool schema causes full request failure (CRITICAL)**: The `mcp_ghl_create_invoice` tool (and possibly others) defines JSON Schema properties with `type: "array"` but **missing the required `items` field**. This causes HTTP 400 errors (`Invalid schema for function 'mcp_ghl_create_invoice': In context=('properties','items'), array schema missing items`) from the LLM provider, which **fails the entire API call** (not just that one tool). When this happens, Hermes falls back to another provider, but if the schema is still invalid, every attempt fails. The fix is to patch `dist/server.js` (or the TypeScript source and rebuild): find the tool definition for `create_invoice` and add `"items": {}` to any array property missing it. After patching, restart Hermes. Check with: `docker logs hermes-flux 2>&1 | grep "Invalid schema"`.

## Project structure (key files)
| File | Purpose |
|---|---|
| `src/server.ts` | Stdio MCP server entry (→ `dist/server.js`) |
| `src/main.ts` | HTTP/Express server with Streamable HTTP + SSE |
| `src/enhanced-ghl-client.ts` | GHL API client with cache, retry, rate-limit tracking |
| `src/tool-registry.ts` | Auto-discovers and registers all tool classes |
| `src/tools/*-tools.ts` | 45 tool modules, one per API category |
| `src/clients/ghl-api-client.ts` | Base GHL API client (~6857 lines, full type coverage) |
| `src/types/ghl-types.ts` | TypeScript type definitions (~6688 lines) |

## References
- `references/api-scope-matrix.md` — Agency vs Location token scopes, which endpoints each can hit, debugging quick-check commands, and Flux sub-account list
