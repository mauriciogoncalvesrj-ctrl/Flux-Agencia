# Headless OAuth Flow with gog — Step-by-Step

## Context
Hermes runs on a headless VPS with no browser. The standard `gog auth add` opens a browser locally, which fails on the server.

## Solution: `--remote` flag

The `--remote` flag splits OAuth into two steps that can be executed on different machines.

### Step 1 — Generate the auth URL (on the server)

```bash
gog auth add "USER_EMAIL" \
  --remote --step 1 \
  --services gmail,calendar,drive,docs,slides,sheets,contacts,tasks,people,forms,meet,analytics,searchconsole,ads,youtube \
  --json
```

Output: a JSON object with `"url"` field. Copy this URL and send it to the user.

### Step 2 — Exchange the redirect URL (on the server, after user completes step)

The user opens the URL in their browser, authenticates with Google, and gets redirected. They must copy the **final redirect URL** from the browser address bar (it contains the authorization code).

```bash
gog auth add "USER_EMAIL" \
  --remote --step 2 \
  --auth-url "PASTE_REDIRECT_URL_HERE" \
  --services gmail,calendar,drive,docs,slides,sheets,contacts,tasks,people,forms,meet,analytics,searchconsole,ads,youtube \
  --json
```

### Verification

```bash
gog auth list --json
gog auth status --json
gog me --json          # profile info (People API)
```

## Pitfalls

1. **Auth URL expires**: The URL from Step 1 is time-sensitive. If the user waits too long, Step 2 will fail with an invalid grant error. Generate a fresh URL if needed.
2. **Redirect URL must be exact**: Copy the FULL redirect URL from the browser, including all query parameters (`?code=...&scope=...&authuser=...&prompt=...`). Partial URLs cause "Invalid authorization code" errors.
3. **Services list must match**: The `--services` argument in Step 2 must be identical to Step 1. If they differ, the token scopes won't match and some services will fail.
4. **Consent screen in Testing mode**: If the Google Cloud project OAuth consent screen is in "Testing" mode (not published), only added test users can authenticate. Add the user's email under APIs & Services → OAuth consent screen → Test users before sending the URL.

## When the user sends their email

The workflow is:
1. Ask user for their Google email
2. Run Step 1 on the server
3. Send the generated URL to the user (Telegram)
4. User opens URL in browser, authorizes, copies redirect URL
5. User sends redirect URL back
6. Run Step 2 on the server
7. Verify with `gog auth list`

## Timezone consideration for reminders

If the user asks for a reminder at a specific local time (e.g. "7:30 da manhã horário Brasil"), convert to UTC for cron:
- BRT (Brasília) = UTC-3
- 7:30 BRT = 10:30 UTC
- Cron expression: `30 10 * * *`

The cron runs in UTC. Always clarify with the user whether they mean morning or evening, and confirm the date (today vs tomorrow).