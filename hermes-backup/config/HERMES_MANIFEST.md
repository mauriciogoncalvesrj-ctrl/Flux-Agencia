# 🧠 Hermes Agent — Configuração, Memória e Personalidade

> Agência Flux · Documentação de referência · 2026-05-10

---

## 1️⃣ Configurações do Hermes (`config.yaml`)

### Modelo Principal

| Campo | Valor |
|---|---|
| `model.default` | `deepseek-v4-pro` |
| `model.provider` | `opencode-go` |
| `model.base_url` | `https://opencode.ai/zen/go/v1` |
| `model.api_key` | `${OPENCODE_GO_API_KEY}` (env) |

### Fallbacks (Provider Failover)

| Posição | Provider | Modelo |
|---|---|---|
| 1º fallback | `opencode-go` | `glm-5.1` |
| 2º fallback | `opencode-go` | `kimi-k2.6` |

### Display / Personalidade

| Campo | Valor |
|---|---|
| `display.personality` | `kawaii` |
| `display.language` | `pt-br` |
| `display.skin` | `default` |
| `display.compact` | `false` |
| `display.show_reasoning` | `false` |
| `display.tui_status_indicator` | `kaomoji` |

### TTS (Text-to-Speech)

| Campo | Valor |
|---|---|
| `tts.provider` | `edge` |
| `tts.edge.voice` | `en-US-AriaNeural` |

### STT (Speech-to-Text)

| Campo | Valor |
|---|---|
| `stt.enabled` | `true` |
| `stt.provider` | `local` |
| `stt.local.model` | `base` |

### Memória

| Campo | Valor |
|---|---|
| `memory.memory_enabled` | `true` |
| `memory.user_profile_enabled` | `true` |
| `memory.memory_char_limit` | `2200` |
| `memory.user_char_limit` | `1375` |

### Gateway (Telegram ativo)

| Campo | Valor |
|---|---|
| `telegram.reactions` | `false` |
| `telegram.channel_prompts` | `{}` |
| `telegram.allowed_chats` | `''` |

### Segurança

| Campo | Valor |
|---|---|
| `security.autht_secrets` | `false` (explicitamente desabilitado por HERMES_REDACT_SECRETS=false) |
| `security.tirith_enabled` | `true` |
| `privacy.redact_pii` | `false` |
| `approvals.mode` | `manual` |

### Delegação / Subagentes

| Campo | Valor |
|---|---|
| `delegation.max_concurrent_children` | `3` |
| `delegation.max_spawn_depth` | `2` |
| `delegation.orchestrator_enabled` | `true` |
| `delegation.child_timeout_seconds` | `600` |

### MCP Servers (Nativo)

| Nome | Tipo | Descrição |
|---|---|---|
| `fal-ai` | Binário Python | `/opt/data/fal-mcp-venv/bin/fal-mcp` · 18 tools de geração de imagem/vídeo |
| `camofox` | npx | Camofox Browser stealth (porta 172.18.0.8:9377) |
| `meta-ads` | npx | Meta Ads Library API |
| `ghl` | npx | GoHighLevel CRM API |
| `n8n` | npx | n8n Automation API |

### Checkpoints

| Campo | Valor |
|---|---|
| `checkpoints.enabled` | `true` |
| `checkpoints.max_snapshots` | `20` |
| `checkpoints.retention_days` | `7` |

---

## 2️⃣ Variáveis de Ambiente (`.env`)

```
# Provider
OLLAMA_API_KEY=***
OPENCODE_GO_API_KEY=***

# Telegram Gateway
TELEGRAM_BOT_TOKEN=***
TELEGRAM_ALLOWED_USERS=1212203404
TELEGRAM_HOME_CHANNEL=1212203404
TELEGRAM_HOME_CHANNEL_THREAD_ID=

# Fal.ai
FAL_KEY=***

# Camofox
CAMOFOX_API_KEY=***

# GitHub
GITHUB_TOKEN=***
```

---

## 3️⃣ Memória Persistente

### 🧠 Memory (notas pessoais do agente)

> Limite: 2200 caracteres (~89% utilizado)

- **Ollama Cloud API** usa `/api/chat` (Bearer auth) com 39 modelos. OpenClaw v2026.5.7: @atlas_fluxia_bot ativo. Modelo primário: opencode-go.
- **Meta Ad Library** 100% bloqueado do VPS — requer VPN/proxy para scraping.
- **Usuário (Maurício/Flux)** comunica preferências visuais via batches de imagens, não descrições verbais. Para design (carrosséis, conteúdo visual), analisar imagens via vision API e produzir sem pedir feedback repetitivo.
- **Ambiente:** Hostinger VPS (8GB RAM + 4GB swap). Domain: somosflux.com.br. HERMES_REDACT_SECRETS=false. `docker compose` N/A dentro hermes-flux — usar `docker run`.
- **Serviços:** Hermes (3GB), OpenClaw (2GB), Paperclip (1GB, port 3100), WebUI (512MB, hub.somosflux.com.br), Traefik (256MB), Open Design (512MB, design.somosflux.com.br:7456, 111 skills).
- **Hermes:** fallback glm-5.1+kimi-k2.6, checkpoints on, delegation depth 2, backup diário 03:00UTC.
- **OpenClaw:** Telegram @atlas_fluxia_bot conectado.
- **Open Design:** Docker container porta 7456, precisa DNS A record para design.somosflux.com.br.
- **Paperclip:** senha reset para FluxIA2026! (2026-05-09). PAPERCLIP_PUBLIC_URL=paperclip.somosflux.com.br. Origin bypass patched.
- **CTO agent do Paperclip** fixado: Hermes CLI instalado, adapter=hermes_local, model=deepseek-v4-pro. Instalação do Hermes CLI no Paperclip via apt python3, copy venv+modules, symlink, copy config+.env, chown.
- **Agência Flux:** IA para Clínicas de Estética. Stack: GHL, Meta Ads, Google Ads, Hermes, OpenClaw, Paperclip. Meta: R$100k/mês. Dores: tráfego, anúncios, conteúdo — quer tudo automatizado. Ação > conversa.
- **Skills da Flux:** pipeline skill + 2 cron jobs (conteúdo seg 9h, anúncios seg 9h30 UTC).
- **Fal.ai MCP** instalado. Binary: `/opt/data/fal-mcp-venv/bin/fal-mcp`. Config em config.yaml. FAL_KEY no .env (key válida, mas saldo esgotado — precisa recarregar em fal.ai/dashboard/billing).

### 👤 User Profile (quem você é)

> Limite: 1375 caracteres (~99% utilizado)

- **Brasileiro falante de português** com conhecimento técnico limitado. Prefere explicações simples, diretas, sem jargão. Usa Hostinger VPS managed panel (botão "Atualizar").
- Espera **explicações com prós/contras/raciocínio** — não aceita "faça X" sem entender por quê.
- Prioriza **simplicidade**, explica **relevância prática**, não assume conhecimento de Docker/YAML.
- Deseja que eu **identifique modelo e provider no início de cada resposta** no formato:
  `⚡ usando deepseek-v4-pro (ollama-cloud)` + linha separadora ────────────
- Se o modelo mudar (ex: visão auxiliar), indica o modelo correto.
- Para **problemas recorrentes em serviços/domínios já configurados**, sempre começa com `session_search` para verificar histórico antes de diagnosticar do zero. Corrige assistentes que ignoram histórico.
- **Controle de execução:** o usuário enfileira múltiplas tarefas e só quer que eu inicie quando ele disser "inicia" ou "pode iniciar". Não executa tarefas na fila sem aprovação explícita. Pode mandar múltiplas mensagens (áudio + texto) antes dar o start.

---

## 4️⃣ Soul (Manifesto de Personalidade)

O **soul** do Hermes Agent é definido pelo sistema prompt base + a personalidade `kawaii` configurada em `display.personality`. Aqui está o núcleo:

### Prompt Base do Sistema

> You are Hermes Agent, an intelligent AI assistant created by Nous Research. You are helpful, knowledgeable, and direct. You assist users with a wide range of tasks including answering questions, writing and editing code, analyzing information, creative work, and executing actions via your tools. You communicate clearly, admit uncertainty when appropriate, and prioritize being genuinely useful over being verbose unless otherwise directed below. Be targeted and efficient in your exploration and investigations.

### Personalidade Ativa: `kawaii`

O sistema Hermes aplica uma camada de personalidade ao modo de interação. A personalidade `kawaii` caracteriza-se por:

- **Tom amigável e acolhedor**, com expressões visuais (kaomoji como indicadores de status)
- **Empatia implícita** na comunicação — mais próxima, menos robótica
- **Uso de emoji/kaomoji** como linguagem de status (configurado em `tui_status_indicator: kaomoji`, ex: `◴`, `◵`, `◶`, `◷` no terminal)
- **Clareza sem frieza** — direto mas não abrupto
- **Entusiasmo contido** — não exagerado, mas genuíno

### Convenções de Comunicação Específicas do Usuário

| Convenção | Aplicação |
|---|---|
| Header de modelo | Sempre no início: `⚡ usando <model> (<provider>)` + linha `──────────────────────────` |
| Português brasileiro | Todos os termos, nomes de botões e descrições |
| Explicação com razão | Prós/contras ao propor soluções |
| Histórico antes de diagnóstico | `session_search` antes de re-diagnosticar problemas conhecidos |
| Execução por aprovação | Só executa após "inicia" ou "pode iniciar" explícito |
| Batch de imagens | Para design, auto-analisa sem pedir feedback textual |

---

## 5️⃣ Skills Principais (Ativas na Agência Flux)

### Skills da Categoria `flux` (Agência Flux)

| Skill | Descrição |
|---|---|
| `flux-ads-audit` | Auditoria automática de anúncios Meta/GHL · score 0-100 · quick wins |
| `flux-competitor-spy` | Espionagem competitiva via Meta Ads Library + Camofox |
| `flux-daily-briefing` | Newsletter matinal de IA, LLMs, GHL, Hermes, OpenClaw |
| `flux-toprank-seo` | Otimização para citação por IAs (ChatGPT, Claude, Perplexity) |
| `flux-agencia-pipeline` | Pipeline automatizado — conteúdo + anúncios + estratégia de tráfego |
| `flux-agencia-conteudo` | Calendário editorial, Reels, carrosséis, posts, Stories |
| `flux-agencia-copywriting` | Headlines, legendas, VSLs, criativos persuasivos |
| `flux-agencia-crm` | GoHighLevel, pipelines, automações, Conversation AI |
| `flux-agencia-estrategia` | Visão holística — conecta marketing, vendas, CRM, IA |
| `flux-agencia-inteligencia` | Benchmarking, tendências, ofertas, oportunidades |
| `flux-agencia-operacoes` | Checklists, onboarding, relatórios, processos |
| `flux-agencia-sdr` | Qualificação de leads, SPIN, BANT, GPCT, agendamento |
| `flux-agencia-trafego` | Meta Ads, Google Ads, segmentação, métricas, otimizações |

### Skills da Categoria `productivity` (Criadas Recentemente)

| Skill | Descrição |
|---|---|
| `text-reviewer` | Reve textos preservando voz do autor · clareza, estrutura, tom |
| `daily-priorities` | Briefing matinal de tarefas e prioridades · framework da Flux |

### Skills DevOps / Infra Importantes

| Skill | Descrição |
|---|---|
| `hermes-github-backup` | Backup automático diário do Hermes para GitHub |
| `docker-traefik-routing` | Correção de roteamento Traefik · Gateway Timeout |
| `paperclip-admin` | Administração e troubleshooting do Paperclip |
| `webhook-subscriptions` | Event-driven agent runs |
| `hermes-agent` | Configuração e manutenção do Hermes Agent |
| `openclaw` | Deploy e manutenção do OpenClaw |

### Skills MLOps / AI

| Skill | Descrição |
|---|---|
| `fal-ai` | Geração de imagem/vídeo via Fal.ai · 40+ modelos |
| `comfyui` | Geração com ComfyUI · REST API |
| `open-design` | Open-source alternativo ao Claude Design · 111 skills · 72 design systems |
| `local-llm-deployment` | Deploy de LLMs locais (Gemma, Llama, Mistral) |

---

## 6️⃣ Cron Jobs Ativos

| Job | Agenda | Entrega | Descrição |
|---|---|---|---|
| `weekly-report-flux` | `0 17 * * 5` (sexta 17h UTC) | `telegram:1212203404` | Relatório semanal de avanços, pendências e próximos passos |
| *(anterior)* | Seg 9h UTC | — | Pipeline de conteúdo (skill `flux-agencia-pipeline`) |
| *(anterior)* | Seg 9h30 UTC | — | Pipeline de anúncios (skill `flux-agencia-pipeline`) |

---

## 7️⃣ Resumo da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│  Agência Flux — Infraestrutura de IA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🖥️ Hostinger VPS (8GB RAM + 4GB swap)                         │
│     Domain: somosflux.com.br                                    │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  🧠 Hermes  │  │ 🔧 OpenClaw │  │ 📎 Paperclip│             │
│  │  (3GB RAM)  │  │  (2GB RAM)  │  │  (1GB RAM)  │             │
│  │             │  │             │  │  Porta 3100 │             │
│  │  Telegram   │  │  Telegram   │  │  Web:3100   │             │
│  │  Cron jobs  │  │  @atlas_    │  │  senha:set  │             │
│  │  MCP servers│  │  fluxia_bot │  │             │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 🌐 WebUI    │  │ 🛡️ Traefik  │  │ 🎨 Design   │             │
│  │  (512MB)    │  │  (256MB)    │  │  (512MB)    │             │
│  │ hub.somos   │  │  Proxy SSL  │  │ design.somos│             │
│  │ flux.com.br │  │             │  │ flux.com.br │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  🔑 Providers: Opencode Go (primário) · Ollama (backup)       │
│  📦 Storage: 4GB swap · Checkpoints · GitHub Backup            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8️⃣ Repositórios

| Repositório | Caminho Local | Descrição |
|---|---|---|
| `hermes-backup` | `~/.hermes/hermes-backup-repo/hermes-backup/` | Backup da config, skills e configuração |
| Paperclip CTO | *(integrado)* | Hermes CLI com adapter hermes_local |

---

## 9️⃣ Notas de Manutenção

- **Swap:** O VPS não tem swap por padrão. Considerar ativar se OOM killer matar containers.
- **Ollama Cloud:** `api.nousresearch.com` está sem DNS (NXDOMAIN). Usar `https://opencode.ai/zen/go/v1`.
- **Fal.ai:** Saldo esgotado — precisa recarregar.
- **OpenClaw WhatsApp:** Não funciona no container (falta dependências nativas).
- **Daily Backup:** 03:00 UTC para GitHub (skill `hermes-github-backup`).

---

> Atualizado em: 2026-05-10 · Modelo primário: deepseek-v4-pro · Provider: opencode-go
