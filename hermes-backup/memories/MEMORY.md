Ollama Cloud API: use `https://ollama.com/v1/` (NOT api.ollama.com — 301 redirect). Bearer auth. 39 models. Primary: glm-5.1 (prompt engineering/vision), deepseek-v4-pro (reasoning), kimi-k2.6 (speed).
§
User (Mauricio/Flux) communicates visual preferences via batches of reference images, not verbal descriptions. For design tasks (carousels, visual content), proactively analyze all images via vision API and produce output without repeatedly asking for text/audio feedback. Prefers receiving versions and iterating silently.
§
Environment: Hostinger VPS (8GB RAM + 4GB swap). Domain: somosflux.com.br. HERMES_REDACT_SECRETS=false. `docker compose` N/A inside hermes-flux — use `docker run`. Services: Hermes (3GB), OpenClaw (2GB), Paperclip (1GB, port 3100), WebUI (512MB, hub.somosflux.com.br), Traefik (256MB), Open Design (512MB, design.somosflux.com.br:7456, 111 skills).
§
Hermes: fallback glm-5.1+kimi-k2.6, checkpoints on, delegation depth 2, daily backup 03:00UTC. OpenClaw: Telegram @atlas_fluxia_bot paired. Open Design: Docker container port 7456, needs DNS A record for design.somosflux.com.br.
§
Paperclip password reset to FluxIA2026! (2026-05-09). PAPERCLIP_PUBLIC_URL stale — needs https://paperclip.somosflux.com.br. Origin bypass patched (lost on recreation). CTO agent fixed: Hermes CLI installed, adapter set to hermes_local, model=deepseek-v4-pro. Hermes CLI install in Paperclip: apt python3, copy venv+modules, symlink, copy config+.env, chown.
§
Agência Flux: IA p/ Clínicas Estética. Stack: GHL, Meta Ads, Google Ads, Hermes, OpenClaw, Paperclip. Meta: R$100k/mês. Pain: tráfego, anúncios, conteúdo — quer tudo automatizado. Ação > conversa. Pipeline skill + 2 cron jobs (conteúdo seg 9h, anúncios seg 9h30 UTC).
§
Fal.ai MCP installed. Binary: /opt/data/fal-mcp-venv/bin/fal-mcp. Config in config.yaml under mcp_servers.fal-ai. FAL_KEY in .env (key set, but balance exhausted — needs top-up at fal.ai/dashboard/billing). 18 tools available once funded.
§
User coordinates Hermes Agent (VPS) with Claude Code (local Windows machine) via shared GitHub repository `mauriciogoncalvesrj-ctrl/Flux-Agencia`, using `flux-comms/` directory protocol for cross-agent communication.