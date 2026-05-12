# Tools Registry — Flux

> Catálogo unificado de ferramentas disponíveis para skills e agentes Flux.
> Skills devem consultar este registro para saber qual ferramenta usar, via qual interface.
>
> *Last updated: 2026-05-12 · Mantido por Atlas*

---

## 🎯 Plataformas Core

| Ferramenta | Interface | Auth | Status | Notas |
|---|---|---|---|---|
| **GoHighLevel (GHL)** | MCP Server | GHL_API_KEY | ⚠️ Location tools com 401 | Substituir token por Location Private Integration |
| **Meta Ads** | MCP Server | Token via env | ✅ Ativo | Relatórios semanais (seg 12:10 UTC) e mensais (dia 1) |
| **Google Ads** | MCP Server | Credentials JSON + Token + CID | ❓ Setup pendente | Credenciais fornecidas via chat |

---

## 🧠 IA & Modelos

| Ferramenta | Interface | Provider | Notas |
|---|---|---|---|
| **kimi-k2.6** | OpenClaw (opencode-go) | Primário | Contexto longo, bom raciocínio |
| **deepseek-v4-pro** | OpenClaw (opencode-go) | Fallback 1 | Reasoning forte |
| **glm-5.1** | OpenClaw (ollama cloud) | Fallback 2 | Prompt engineering, visão |
| **minimax-m2.7** | OpenClaw (ollama cloud) | Fallback 3 | Velocidade |
| **Ollama Cloud** | API (`ollama.com/v1`) | Bearer token | 21 modelos disponíveis |

---

## 🎨 Criação Visual

| Ferramenta | Interface | Auth | Status | Notas |
|---|---|---|---|---|
| **Fal.ai** | MCP Server | FAL_KEY | 🔴 Saldo zerado | Recarregar para usar |
| **Open Design** | HTTP API | — | ✅ Ativo | `design.somosflux.com.br:7456`, 111 skills |
| **Puppeteer + Chromium** | CLI local | — | ✅ Ativo | HTML → PNG, carrosséis Instagram |
| **Image Generate (OpenClaw)** | Tool nativa | FAL_KEY / Provider | ✅ Configurado | Via `image_generate` tool |

---

## 📊 Relatórios & Automação

| Ferramenta | Interface | Schedule | Notas |
|---|---|---|---|
| **flux-meta-ads-relatorio** | Skill + Script Python | Semanal (seg 12:10 UTC) | `dec95f276e29` |
| **flux-meta-ads-relatorio (mensal)** | Skill + Script Python | Mensal (dia 1 12:10 UTC) | `606f71c16a63` |
| **flux-meta-ads-balance-alert** | Skill + Cron | On-demand | Alertas de saldo de conta |
| **flux-daily-briefing** | Skill + Cron | Diário | Briefing de anúncios |
| **flux-toprank-seo** | Skill | On-demand | Auditoria SEO |
| **flux-competitor-spy** | Skill | On-demand | Análise competitiva |
| **flux-ads-audit** | Skill | On-demand | Auditoria de anúncios |
| **flux-prompt-engineer** | Skill | On-demand | Engenharia de prompt |

---

## 📡 MCP Servers Disponíveis

| MCP Server | Comando | Status | Dependências |
|---|---|---|---|
| **Meta Ads** | `npx @mist-cloud/mcp-meta-ads` | ✅ | Token Meta |
| **GHL** | `npx @mist-cloud/mcp-ghl` | ⚠️ | GHL_API_KEY (Location scope) |
| **Google Ads** | `npx @mist-cloud/mcp-google-ads` | ❓ | Credentials pendentes |
| **Fal.ai** | `npx @mist-cloud/mcp-fal` | 🔴 | Saldo zerado |

---

## 🔧 Scripts & Utilitários

| Ferramenta | Path | Linguagem | Notas |
|---|---|---|---|
| **meta_ads_real_balance.py** | (na VPS) | Python | Saldo real de conta de anúncios |
| **gerar-relatorio.py** | `skills/flux/flux-meta-ads-relatorio/scripts/` | Python | Geração de relatório Meta Ads |
| **relatorio-template.html** | `skills/flux/flux-meta-ads-relatorio/templates/` | HTML | Template visual de relatório |
| **gerar_pdf_analise.py** | `workspace/` | Python | Geração de PDF de análise |

---

## 🌐 Infraestrutura

| Ferramenta | Interface | Host | Notas |
|---|---|---|---|
| **Atlas (OpenClaw)** | Telegram + Web | `openclaw.somosflux.com.br` | Agente principal VPS |
| **Open Design** | HTTP | `design.somosflux.com.br:7456` | 111 skills de design |
| **Paperclip** | HTTP | `paperclip.somosflux.com.br` | Porta 3100, password: FluxIA2026! |
| **WebUI** | HTTP | `hub.somosflux.com.br` | Interface web |
| **Traefik** | Proxy | VPS | Roteamento de domínios |
| **Hostinger VPS** | SSH | `somosflux.com.br` | 8GB RAM + 4GB swap |

---

## 📦 CLIs Disponíveis (Node.js)

| Ferramenta | Comando | Notas |
|---|---|---|
| **GitHub CLI** | `gh` | Issues, PRs, workflows |
| **Whisper** | `whisper` | Transcrição local PT-BR |
| **ffmpeg** | `ffmpeg` | Processamento de vídeo/áudio |
| **Puppeteer** | (via Node.js) | Automação browser headless |

---

## 🔗 Integrações Externas

| Ferramenta | Tipo | Status | Notas |
|---|---|---|---|
| **Telegram Bot** | Mensageria | ✅ Ativo | `@atlas_fluxia_bot` (Mauricio → Atlas) |
| **GitHub (Flux-Agencia)** | Git | ✅ Ativo | `mauriciogoncalvesrj-ctrl/Flux-Agencia` |
| **Firecrawl** | API | ✅ Ativo | Web scraping e search |

---

## 🚫 Descontinuado / Removido

| Ferramenta | Motivo |
|---|---|
| **n8n** | GHL Flow Builder V3 cobre orquestração |
| **Postiz** | Fora da stack |
| **Kit/Beehiiv** | Fora da stack |
| **Ahrefs** | Fora da stack |
| **Microsoft Clarity** | Fora da stack |
| **Hermes Agent (Nous)** | Substituído por Atlas (OpenClaw) — backup em `hermes-backup/` |

---

> **Uso:** Toda skill Flux deve referenciar este registro para saber quais ferramentas estão disponíveis e em qual estado.
>
> **Manutenção:** Atlas atualiza este arquivo quando novas ferramentas são adicionadas/removidas.
