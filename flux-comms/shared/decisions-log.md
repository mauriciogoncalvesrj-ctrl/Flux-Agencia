# Registro de Decisões Arquiteturais — Flux

> Formato: `YYYY-MM-DD | Decisão | Contexto | Status`

## 2026-05-12

| Decisão | Detalhe |
|---------|---------|
| **Implementação da análise do Hermes** | Executadas as 5 frentes prioritárias da análise de gaps vs `coreyhaines31/marketingskills` |
| **product-marketing-context por cliente** | Criados templates `.agents/contexts/{taciana,luana,proton,alpha}/product-marketing-context.md`. Aguardando preenchimento do Mauricio |
| **TOOLS-REGISTRY.md criado** | Catálogo unificado de todas as ferramentas/MCPs/scripts/CLIs da Flux |
| **VERSIONS.md criado** | Tracking de versão de skills e infraestrutura |
| **status-flux.md criado** | Estado atual da operação, pendências, clientes, metas |
| **skill-template.md criado** | Template padronizado para skills Flux (baseado no padrão Corey Haines, adaptado PT-BR) |
| **6 novas skills instaladas** | customer-research, competitor-profiling, directory-submissions, community-marketing, image, video — do repo `coreyhaines31/marketingskills` |
| **Substituição do Hermes Agent por Atlas** | O agente VPS mudou de Hermes Agent (Nous Research) para Atlas (OpenClaw). Motivo: reestruturação da operação. Backup completo preservado em `hermes-backup/` |
| **Instalação de skills ClawHub** | gog, agent-browser, github, skillscan, skill-creator instalados para expandir capacidade da VPS |
| **flux-comms mantido** | Protocolo de comunicação com Claude Code preservado. Atlas assume o outbox `from-hermes/` |

## 2026-05-10

| Decisão | Detalhe |
|---------|---------|
| **Handshake Hermes ↔ Claude Code** | Canal de comunicação estabelecido via `flux-comms/`. Protocolo v1.0 definido |
| **Plano de migração de memória** | Contexto estável → `shared/`. MEMORY.md fica só com conteúdo operacional. USER.md consolidado em pt-br |

## Decisões Anteriores (do contexto Claude Code)

| Decisão | Data | Detalhe |
|---------|------|---------|
| **Stack sem n8n** | ~2026-05 | GHL Flow Builder V3 cobre orquestração. Manter n8n é redundância |
| **Remoção de ferramentas** | ~2026-05 | Postiz, Kit/Beehiiv, Ahrefs, Microsoft Clarity removidos da stack |
| **Stack central** | ~2026-05 | GHL + Meta Ads + Google Ads + IA (Claude/Hermes/Atlas) |
| **3 planos de serviço** | ~2026-05 | Start R$1.5k / Conversão R$2.5k / Autônomo R$4.5-6.5k (flagship) |
| **Regra de marca GHL** | ~2026-05 | Cliente final NUNCA sabe que é GHL. Sempre "Sistema Flux 360" |
| **Arquitetura 7 agentes** | ~2026-05 | CEO Hermes + 6 Diretores (modelos por função) |
| **Contrato mínimo 6 meses** | ~2026-05 | Garantia de processo, nunca de resultado (CFM/ANVISA) |

---

> Mantido por Atlas · 2026-05-12
