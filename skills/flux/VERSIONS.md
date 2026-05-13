# Flux Agency — Versions

Versões atuais de todas as skills da Agência Flux. Agentes podem comparar com versões locais para checar atualizações.

| Skill | Versão | Última Atualização |
|-------|--------|---------------------|
| flux-agency-standards | 1.0.0 | 2026-05-12 |
| flux-prompt-engineer | 2.1.0 | 2026-05-12 |
| flux-meta-ads-balance-alert | 1.0.0 | 2026-05-12 |
| flux-meta-ads-relatorio | 1.0.0 | 2026-05-12 |
| flux-ads-audit | 1.0.0 | 2026-05-12 |
| flux-competitor-spy | 1.0.0 | 2026-05-12 |
| flux-daily-briefing | 1.0.0 | 2026-05-12 |
| flux-toprank-seo | 1.0.0 | 2026-05-12 |
| flux-x-monitor | 1.0.0 | 2026-05-12 |
| flux-social-estetica | 1.0.0 | 2026-05-12 |
| flux-copy-estetica | 1.0.0 | 2026-05-12 |
| flux-landing-page-cro | 1.0.0 | 2026-05-12 |
| flux-orchestrator | 1.0.0 | 2026-05-13 |

## Contextos de Cliente

| Cliente | Versão | Última Atualização | Meta Ads Account |
|---------|--------|---------------------|-------------------|
| Taciana | 1.0.0 | 2026-05-12 | act_911737697183748 |
| Luana | 1.0.0 | 2026-05-12 | act_1073353887241970 |
| Proton | 1.0.0 | 2026-05-12 | act_392106056202806 |
| Alpha | 1.0.0 | 2026-05-12 | act_912031229902602 |

## Changelog

### 2026-05-13 — Camada de Orquestração
- **Criada `flux-orchestrator`** — meta-skill de orquestração multi-agente
  - Define 5 agentes especialistas: Creative, Meta Ads, Research, CRM & Social, DevOps
  - Protocolo de delegação: Classificar → Decompor → Executar (paralelo) → Sintetizar
  - Templates de decomposição por tipo de request (criativo, relatório, LP, pesquisa, infra)
  - Integração com client contexts (carrega automaticamente)
  - Sistema de pré-requisitos entre skills (padrão absorvido do coreyhaines31/marketingskills)
- **Criado `references/decomposition-playbook.md`** — exemplos detalhados de decomposição

### 2026-05-12 — Grande Refatoração
- **Refatoradas 8 skills** para o template canônico `flux-agency-standards`
  - Todas agora têm: Before Starting (product-marketing-context), Common Mistakes, Task-Specific Questions, Tool Integrations, Related Skills
  - Removidos campos não-canônicos: `author`, `category`, `user-invokable`, `argument-hint`, `triggers`
  - Pitfalls convertidos de bullet lists para tabelas Erro|Causa|Correção
- **Criados 4 contextos de cliente** em `skills/flux/contexts/` (Taciana, Luana, Proton, Alpha)
  - Modelo padronizado com 10 seções: overview, ICP, dores, tratamentos, concorrência, diferenciação, objeções, customer language, brand voice, proof points
  - Campos a preencher com cada cliente via briefing
- **Criado VERSIONS.md** (este arquivo)
- **Criado Tools Registry** em `flux-agency-standards/references/tools-registry.md`
  - Catálogo de MCPs (Meta Ads, GHL, Fal.ai, CamoFox), CLIs (xurl), scripts fixos e cron jobs
- **flux-prompt-engineer** 2.0.0 → 2.1.0: adicionadas seções canônicas faltantes
- Análise completa do repositório `coreyhaines31/marketingskills` (41 skills)
  - Identificados 5 padrões arquiteturais absorvidos (product-marketing-context, cross-referencing, tools registry, referenciação externa, common mistakes)
  - Skills originais instaladas em `skills_disabled/productivity/marketingskills/`

### Histórico Anterior
- **2026-05-10:** Skills criadas: `flux-prompt-engineer` (2.0.0), templates Instagram estética, `prompts-db.json`
- **2026-05-11:** `flux-meta-ads-balance-alert` — corrigido bug do `balance` contábil vs real (Graph API `funding_source_details`)
- **2026-05-09:** Paperclip reset senha, CTO agent fix, Hermes CLI instalado no Paperclip
