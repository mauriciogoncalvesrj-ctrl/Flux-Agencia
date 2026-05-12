Ollama Cloud API: use `https://ollama.com/v1/` (NOT api.ollama.com — 301 redirect). Bearer auth. 39 models. Primary: glm-5.1 (prompt engineering/vision), deepseek-v4-pro (reasoning), kimi-k2.6 (speed).
§
User (Mauricio/Flux) communicates visual preferences via batches of reference images, not verbal descriptions. For design tasks (carousels, visual content), proactively analyze all images via vision API and produce output without repeatedly asking for text/audio feedback. Prefers receiving versions and iterating silently.
§
Environment: Hostinger VPS (8GB RAM + 4GB swap). Domain: somosflux.com.br. HERMES_REDACT_SECRETS=false. `docker compose` N/A inside hermes-flux — use `docker run`. Services: Hermes (3GB), OpenClaw (2GB), Paperclip (1GB, port 3100), WebUI (512MB, hub.somosflux.com.br), Traefik (256MB), Open Design (512MB, design.somosflux.com.br:7456, 111 skills).
§
Hermes: fallback glm-5.1+kimi-k2.6, checkpoints on, delegation depth 2, daily backup 03:00UTC. Context bloat risk: 170KB skills + 563 GHL tools. GHL MCP `create_invoice` invalid schema → HTTP 400. n8n offline, google-ads failing.
§
Paperclip password reset to FluxIA2026! (2026-05-09). PAPERCLIP_PUBLIC_URL stale — needs https://paperclip.somosflux.com.br. Origin bypass patched (lost on recreation). CTO agent fixed: Hermes CLI installed, adapter set to hermes_local, model=deepseek-v4-pro. Hermes CLI install in Paperclip: apt python3, copy venv+modules, symlink, copy config+.env, chown.
§
Meta Ads: report semanal `dec95f276e29` (seg 12:10 UTC), mensal `606f71c16a63` (dia 1 12:10 UTC). Luana Sampaio split por unidade: [JUNDIAI]/[CAJAMAR], compartilhadas 50/50. Display names = nome do cliente. Google Ads MCP: credentials (JSON, Token, CID) provided via chat for VPS setup.
§
GHL MCP: GHL_API_KEY=AGENCY_KEY (same pit- token) → 401 on location tools. Fix: gen Location Private Integration token, replace GHL_API_KEY. See skill ghl-mcp-server. Fal.ai MCP installed (balance exhausted).
§
User coordinates Hermes Agent (VPS) with Claude Code (local Windows machine) via shared GitHub repository `mauriciogoncalvesrj-ctrl/Flux-Agencia`, using `flux-comms/` directory protocol for cross-agent communication.