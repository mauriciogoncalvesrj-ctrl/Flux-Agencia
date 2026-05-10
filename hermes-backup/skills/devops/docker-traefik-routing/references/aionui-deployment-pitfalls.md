# AionUI Deployment Pitfalls on Docker + Traefik

Session context: deploying AionUI (aionui:v1.9.25) on a Hostinger VPS behind Traefik v3.6 with custom domain, HTTPS, and basic auth.

## Discovery 1: AionUI Has NO Portuguese (pt-BR) Locale

The language dropdown inside AionUI Settings → Language shows only:
- 日本語 (Japanese)
- 한국어 (Korean)
- Türkçe (Turkish)
- Русский (Russian)
- Українська (Ukrainian)
- English

There is NO Portuguese/Português/Português (Brasil) option. If the user requires a Portuguese UI, **AionUI is not suitable**. The Hermes WebUI (`nesquena/hermes-webui`) has full `pt` locale with `_speech: 'pt-BR'` and should be used instead.

## Discovery 2: AionUI ONLY Supports OpenClaw (Not Hermes Agent)

The "Add Remote Agent" modal explicitly states:
> "Only remote OpenClaw connections are supported for now. Other agents are in development."

AionUI cannot connect to Hermes Agent directly. It is designed exclusively for OpenClaw gateway connections via WebSocket (`wss://`). If the goal is to manage Hermes Agent, use the Hermes WebUI instead.

## Discovery 3: Dual Authentication Layers

When deploying AionUI behind Traefik with basic auth, users encounter TWO separate logins:

1. **Traefik Basic Auth** — The browser prompts for username/password before showing any content. This is the Traefik middleware (`traefik.http.middlewares.aionui-auth.basicauth.users`).
2. **AionUI Internal Login** — After passing Traefik auth, the AionUI web app shows its OWN login screen with a brand name "AionUi", username/password fields, and a "Remember me" checkbox.

**This confuses users.** The Traefik credentials (`flux / FluxIA2026`) are NOT the AionUI admin credentials.

### AionUI Default Admin Credentials

On first startup, AionUI generates a random admin password and prints it to stdout:
```
🔐 Or Use Initial Admin Credentials / 或使用初始管理员凭证:
   Username / 用户名: admin
   Password / 密码:   l0F8E*z44Odm
```

**Action required:** Log in with `admin` + generated password, then change the password inside the AionUI settings immediately.

## Discovery 4: OpenClaw Gateway Bind Blocks External Connections

Even if Traefik routes `wss://hub.somosflux.com.br:64551` to the OpenClaw container, OpenClaw's internal gateway config may reject connections:

```json
{
  "gateway": {
    "mode": "local",
    "port": 64551,
    "bind": "lan",
    "auth": { "mode": "token" }
  }
}
```

The `"bind": "lan"` value means OpenClaw listens on `0.0.0.0` inside its own container (Docker bridge), but `"mode": "local"` may restrict connections to same-container or same-host. For remote AionUI connections, OpenClaw likely needs `"mode": "remote"` or the token-based auth configured correctly.

**Diagnosis:**
```bash
docker exec openclaw-4vbk-openclaw-1 cat /data/.openclaw/openclaw.json | grep -A5 '"gateway"'
```

**Fix:** Change OpenClaw config to `"mode": "remote"` and ensure the AionUI WebSocket URL includes the gateway token.

**Warning:** Exposing OpenClaw gateway to the public internet without proper token auth is a security risk. The gateway token acts as a password.

## Discovery 5: DNS Must Exist BEFORE Traefik Route

Traefik/Let's Encrypt performs HTTP-01 validation. If the A record for the custom subdomain (e.g., `hub.somosflux.com.br`) does not resolve to the server IP **before** the container starts, certificate issuance fails repeatedly.

**Workflow:**
1. User adds DNS A record in DNS panel (`hub` → `2.24.85.2`)
2. Wait for propagation (or verify with `host hub.somosflux.com.br`)
3. THEN create the Traefik router/container with the domain

## Discovery 6: Container Labels Are Immutable

If a container was started without Traefik labels (e.g., `aionui` initially launched with only `-p 127.0.0.1:25808:25808`), you cannot add labels later. You must:

```bash
docker stop aionui
docker rm aionui

docker run -d \
  --name aionui \
  --network proxy \
  --restart unless-stopped \
  -p 127.0.0.1:25808:25808 \
  -e AIONUI_ALLOW_REMOTE=true \
  -e AIONUI_HOST=0.0.0.0 \
  -l "traefik.enable=true" \
  -l "traefik.http.routers.aionui.rule=Host(\`hub.somosflux.com.br\`)" \
  -l "traefik.http.routers.aionui.entrypoints=websecure" \
  -l "traefik.http.routers.aionui.tls.certresolver=letsencrypt" \
  -l "traefik.http.services.aionui.loadbalancer.server.port=25808" \
  -l "traefik.http.routers.aionui.middlewares=aionui-auth" \
  -l "traefik.http.middlewares.aionui-auth.basicauth.users=flux:\$apr1\$..." \
  aionui:v1.9.25
```

## Summary Decision Matrix

| User Goal | AionUI | Hermes WebUI |
|---|---|---|
| Portuguese UI | ❌ Not supported | ✅ Full pt-BR |
| Connect to Hermes Agent | ❌ Not supported | ✅ Native |
| Connect to OpenClaw | ✅ Native (WebSocket) | ❌ Not supported |
| Dashboard / multi-agent view | ✅ Yes | ❌ No |
| Dark theme | ✅ Yes | ✅ Yes |

When the user wants "a visual panel for my Hermes Agent in Portuguese", the correct answer is **Hermes WebUI**, not AionUI.
