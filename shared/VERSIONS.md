# VERSIONS.md — Flux Skills & Infraestrutura

> Tracking de versão das skills próprias da Flux e da infraestrutura de agentes.
> Skills do Corey Haines versionadas no repo original (`marketingskills/VERSIONS.md`).
>
> *Last updated: 2026-05-12 · Mantido por Atlas*

---

## 🏛️ Infraestrutura

| Componente | Versão | Data | Status |
|---|---|---|---|
| **Atlas (OpenClaw)** | 1.0.0 | 2026-05-12 | ✅ Ativo |
| **OpenClaw Gateway** | (auto) | 2026-05-09 | ✅ Ativo |
| **Modelo Primário** | kimi-k2.6 (opencode-go) | 2026-05-12 | ✅ Ativo |
| **VPS Hostinger** | 8GB/4GB swap | 2026-05-09 | ✅ Ativo |

---

## 🧩 Skills Flux (próprias)

| Skill | Versão | Última Atualização | Status | Notas |
|---|---|---|---|---|
| **flux-meta-ads-relatorio** | 1.0.0 | 2026-05-10 | ✅ Ativo | Cron: seg 12:10 UTC + dia 1 |
| **flux-meta-ads-balance-alert** | 1.0.0 | 2026-05-10 | ✅ Ativo | On-demand |
| **flux-daily-briefing** | 1.0.0 | 2026-05-10 | ✅ Ativo | Diário |
| **flux-toprank-seo** | 1.0.0 | 2026-05-10 | ✅ Ativo | On-demand |
| **flux-competitor-spy** | 1.0.0 | 2026-05-10 | ✅ Ativo | On-demand |
| **flux-ads-audit** | 1.0.0 | 2026-05-10 | ✅ Ativo | On-demand |
| **flux-prompt-engineer** | 1.0.0 | 2026-05-10 | ✅ Ativo | On-demand |
| **flux-x-monitor** | 1.0.0 | 2026-05-10 | ✅ Ativo | On-demand |
| **ghl-mcp-server** | 1.0.0 | 2026-05-10 | ⚠️ Location 401 | Token fix pendente |

---

## 📦 Skills Externas (ClawHub / Corey Haines)

| Skill | Versão | Instalada em | Status |
|---|---|---|---|
| **openclaw-marketing-skills** (33 skills) | (pacote) | 2026-05-12 | ✅ Instalado |
| **product-marketing-context** | 1.1.0 | 2026-05-12 | ✅ Template criado p/ 4 clientes |
| **instagram-carousel** | release-v1 | 2026-05-10 | ✅ Instalado |
| **clawhub** | latest | 2026-05-12 | ✅ Instalado |
| **agent-browser** | latest | 2026-05-12 | ✅ Instalado |
| **github** | latest | 2026-05-12 | ✅ Instalado |
| **skillscan** | latest | 2026-05-12 | ✅ Instalado |
| **skill-creator** | latest | 2026-05-12 | ✅ Instalado |

---

## 📋 Documentação

| Documento | Versão | Data | Status |
|---|---|---|---|
| **glossario.md** | 1.0.0 | 2026-05-12 | ✅ Ativo |
| **decisions-log.md** | 1.0.0 | 2026-05-12 | ✅ Ativo |
| **TOOLS-REGISTRY.md** | 1.0.0 | 2026-05-12 | ✅ Criado |
| **VERSIONS.md** (este) | 1.0.0 | 2026-05-12 | ✅ Criado |
| **status-flux.md** | 1.0.0 | 2026-05-12 | 🔴 Pendente |
| **product-marketing-context (4 clientes)** | 1.0.0 | 2026-05-12 | 🟡 Templates criados, aguardando preenchimento |

---

## 🔄 Changelog

### 2026-05-12
- **NEW:** TOOLS-REGISTRY.md criado (catálogo unificado de ferramentas)
- **NEW:** VERSIONS.md criado (este arquivo)
- **NEW:** `.agents/contexts/{taciana,luana,proton,alpha}/product-marketing-context.md` — templates criados
- **NEW:** Análise de gaps vs `coreyhaines31/marketingskills` concluída
- **CHANGE:** Hermes Agent → Atlas (OpenClaw)

### 2026-05-10
- **NEW:** flux-comms/ protocolo estabelecido (Hermes ↔ Claude Code)
- **NEW:** glossario.md, decisions-log.md criados
- **NEW:** 8 perfis Flux ativos no Hermes

---

> **Convenção de versionamento:** `MAJOR.MINOR.PATCH`
> - MAJOR: Mudança estrutural (re-escrita da skill, troca de framework)
> - MINOR: Nova funcionalidade ou seção
> - PATCH: Correção, ajuste de prompt, update de referência
