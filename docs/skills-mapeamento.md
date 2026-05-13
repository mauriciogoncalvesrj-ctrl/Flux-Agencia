# Mapeamento de Skills — Flux Agency

**Data:** 2026-05-12
**Fonte analisada:** https://github.com/VoltAgent/awesome-agent-skills
**Objetivo:** Identificar skills do repositorio open-source que a Flux ja tem, que falta, e que vale a pena adicionar.

---

## Legenda

| Status | Significado |
|---|---|
| ✅ Ja temos | Skill equivalente ja existe no stack Flux |
| 🟡 Parcial | Temos algo parecido, mas nao cobre 100% |
| ❌ Falta | Nao existe no stack atual — oportunidade de adicionar |
| 🔵 Nova | Criada hoje (2026-05-12) |

---

## 1. Copywriting & Aquisicao (Kim Barrett Framework)

| Skill do Repo | Nossa Skill | Status | Gap / Nota |
|---|---|---|---|
| `avatar-extraction` | `market-research` (secao persona) | 🟡 | Temos pesquisa de persona, mas nao extracao sistematica de avatar. Nova skill `flux-copy-acquisition` cobre isso. |
| `offer-extraction` | Nenhuma | ❌ | **Critico.** Nao temos framework de oferta. Coberto agora por `flux-copy-acquisition`. |
| `schwartz-awareness-mapper` | Nenhuma | ❌ | **Critico.** Nao mapeamos nivel de consciencia do publico. Coberto agora por `flux-copy-acquisition`. |
| `mechanism-builder` | Nenhuma | ❌ | **Critico.** Nao temos mecanismo unico documentado. Coberto agora por `flux-copy-acquisition`. |
| `headline-matrix` | Nenhuma | ❌ | Nao geramos matriz de titulos sistematicamente. Coberto agora por `flux-copy-acquisition`. |
| `objection-crusher` | Nenhuma | ❌ | Nao temos banco de objecoes. Coberto agora por `flux-copy-acquisition`. |
| `ad-angle-multiplier` | Nenhuma | ❌ | Nao multiplicamos angulos de criativo. Coberto agora por `flux-copy-acquisition`. |
| `scroll-stopping-creative` | `ads-creative` (hook 0-3s) | 🟡 | Temos guideline de hook, mas nao framework completo. Coberto agora por `flux-copy-acquisition`. |
| `conversion-path-builder` | Nenhuma | ❌ | Nao documentamos funil padrao. Coberto agora por `flux-copy-acquisition`. |
| `performance-diagnosis` | `ads-audit` | 🟡 | Temos auditoria, mas nao checklist de diagnostico especifico por sintoma. Coberto agora por `flux-copy-acquisition`. |
| `full-funnel-campaign-orchestrator` | Nenhuma | ❌ | **Critico.** Nao temos orquestracao de campanha. Criada hoje: `flux-campaign-orchestrator`. |
| `generic-language-killer` | Brand rules (memoria) | 🟡 | Temos regras de brand, mas nao framework sistematico de especificidade. Coberto agora por `flux-copy-acquisition`. |

**Resumo Copy/Aquisicao:**
- ❌ **11 skills faltavam** no nosso stack
- 🔵 **2 criadas hoje:** `flux-copy-acquisition` e `flux-campaign-orchestrator`
- 🟡 **3 parcialmente cobertas** por skills existentes

---

## 2. Marketing & Growth (Corey Haines Framework)

| Skill do Repo | Nossa Skill | Status | Gap / Nota |
|---|---|---|---|
| `ad-creative` | `ads-creative` | ✅ | Ja temos. Cobre criativo cross-platform. |
| `paid-ads` | `ads-google`, `ads-meta`, `ads-linkedin`, `ads-tiktok`, `ads-microsoft`, `ads-apple`, `ads-youtube` | ✅ | Temos especializacao por plataforma. |
| `social-content` | Nenhuma | ❌ | Nao temos skill de conteudo organico Instagram/LinkedIn. **Oportunidade.** |
| `content-strategy` | Nenhuma | ❌ | Nao temos skill de estrategia de conteudo. **Oportunidade.** |
| `marketing-ideas` | Nenhuma | ❌ | Nao temos skill de geracao de ideias de campanha. **Oportunidade.** |
| `copywriting` | `ads-create` (copy brief) | 🟡 | Temos gerador de brief, mas nao skill de copywriting pura. Coberto agora por `flux-copy-acquisition`. |
| `email-sequence` | Nenhuma | ❌ | Nao temos skill de sequencia de e-mail. **Oportunidade.** |
| `pricing-strategy` | Nenhuma | ❌ | Nao temos skill de estrategia de precificacao. **Oportunidade.** |
| `churn-prevention` | Nenhuma | ❌ | Nao temos skill de retencao. **Oportunidade.** |
| `analytics-tracking` | `ads-audit` (tracking audit) | 🟡 | Temos auditoria de tracking, mas nao setup. **Oportunidade.** |
| `form-cro` | Nenhuma | ❌ | Nao temos skill de otimizacao de formularios. **Oportunidade.** |
| `sales-enablement` | Nenhuma | ❌ | Nao temos skill de material de vendas (pitch deck, one-pager). **Oportunidade.** |
| `referral-program` | Nenhuma | ❌ | Nao temos skill de programa de indicacao. **Oportunidade.** |
| `ab-test-setup` | Nenhuma | ❌ | Nao temos skill de teste A/B. **Oportunidade.** |
| `ai-seo` | Nenhuma | ❌ | Nao temos skill de SEO para IA/LLM. **Oportunidade.** |
| `competitor-alternatives` | `ads-competitor` | 🟡 | Temos inteligencia competitiva, mas nao gerador de paginas de comparacao. **Oportunidade.** |
| `launch-strategy` | Nenhuma | ❌ | Nao temos skill de lancamento de produto/campanha. **Oportunidade.** |
| `marketing-psychology` | Nenhuma | ❌ | Nao temos skill de psicologia aplicada ao marketing. **Oportunidade.** |
| `onboarding-cro` | Nenhuma | ❌ | Nao temos skill de onboarding de clientes. **Oportunidade.** |
| `page-cro` | Nenhuma | ❌ | Nao temos skill de CRO de paginas. **Oportunidade.** |
| `popup-cro` | Nenhuma | ❌ | Nao temos skill de popups/modais. **Oportunidade.** |
| `paywall-upgrade-cro` | Nenhuma | ❌ | Nao aplicavel direto (B2B servico, nao SaaS). |
| `product-marketing-context` | Nenhuma | ❌ | Nao temos documento de contexto de produto. **Oportunidade.** |
| `programmatic-seo` | Nenhuma | ❌ | Nao temos skill de SEO programatico. **Oportunidade.** |
| `revops` | Nenhuma | ❌ | Nao temos skill de revenue operations. **Oportunidade.** |
| `schema-markup` | Nenhuma | ❌ | Nao temos skill de schema markup. **Oportunidade.** |
| `seo-audit` | Nenhuma | ❌ | Nao temos skill de auditoria SEO. **Oportunidade.** |
| `signup-flow-cro` | Nenhuma | ❌ | Nao aplicavel direto (B2B servico). |
| `site-architecture` | Nenhuma | ❌ | Nao temos skill de arquitetura de site. **Oportunidade.** |
| `free-tool-strategy` | Nenhuma | ❌ | Nao temos skill de ferramentas gratuitas como lead magnet. **Oportunidade.** |

**Resumo Marketing/Growth:**
- ✅ **2 skills ja temos** (ad-creative, paid-ads)
- 🟡 **3 parcialmente cobertas**
- ❌ **25 skills faltam** — muitas oportunidades

---

## 3. Social Publishing & Multimedia

| Skill do Repo | Nossa Skill | Status | Gap / Nota |
|---|---|---|---|
| `typefully` | Nenhuma | ❌ | Agendamento LinkedIn/X. **Oportunidade baixa** (foco Flux = Instagram). |
| `slack-gif-creator` | Nenhuma | ❌ | GIFs para Slack. **Nao aplicavel.** |
| `sora` | Fal.AI (usamos) | 🟡 | Ja usamos Fal.AI para imagens. Video com Sora seria upgrade. |
| `openai/speech` | Nenhuma | ❌ | Geracao de voz off. **Oportunidade** para Reels. |
| `openai/slides` | Nenhuma | ❌ | Criacao de apresentacoes PPT. **Oportunidade** para propostas. |
| `podcast-generation` | Nenhuma | ❌ | Podcast com IA. **Oportunidade** para conteudo de autoridade. |

**Resumo Multimedia:**
- 🟡 **1 parcialmente coberta** (Fal.AI vs Sora)
- ❌ **5 faltam** — nenhuma critica, mas oportunidades de conteudo

---

## 4. Operational Automation & Research

| Skill do Repo | Nossa Skill | Status | Gap / Nota |
|---|---|---|---|
| `firecrawl` | WebFetch + WebSearch | 🟡 | Ja fazemos scraping manual. Firecrawl seria automatizado. |
| `notion-knowledge-capture` | Nenhuma | ❌ | Nao usamos Notion para knowledge base. **Oportunidade.** |
| `notion-meeting-intelligence` | Nenhuma | ❌ | Preparacao de reunioes com contexto Notion. **Oportunidade.** |
| `notion-research-documentation` | Nenhuma | ❌ | Documentacao de pesquisa no Notion. **Oportunidade.** |
| `spreadsheet` | Nenhuma | ❌ | Analise de dados em planilhas. **Oportunidade** para dashboards. |
| `gws-workflow` | Nenhuma | ❌ | Google Workspace workflows. **Oportunidade** para automatizar docs. |
| `courier-skills` | Nenhuma | ❌ | Notificacoes multi-canal. **Oportunidade** para alertas internos. |
| `sentry-workflow` | Nenhuma | ❌ | Debug de producao. **Nao aplicavel** (nao temos app). |

**Resumo Operational:**
- 🟡 **1 parcialmente coberta**
- ❌ **7 faltam** — oportunidades de eficiencia operacional

---

## 5. Design & Frontend

| Skill do Repo | Nossa Skill | Status | Gap / Nota |
|---|---|---|---|
| `openai/frontend-skill` | Nenhuma | ❌ | Criacao de landing pages. **Oportunidade** para pages de captacao. |
| `web-design-guidelines` | Nenhuma | ❌ | Guidelines de design web. **Oportunidade.** |
| `frontend-design` | Nenhuma | ❌ | Design frontend. **Oportunidade.** |
| `seo-aeo-best-practices` | Nenhuma | ❌ | SEO + AEO (Answer Engine Optimization). **Oportunidade.** |
| `content-experimentation-best-practices` | Nenhuma | ❌ | Testes A/B de conteudo. **Oportunidade.** |

**Resumo Design:**
- ❌ **5 faltam** — oportunidades de landing page e CRO

---

## 6. Crypto (Nao aplicavel)

| Skill do Repo | Status |
|---|---|
| `binance/crypto-market-rank` | Nao aplicavel |
| `binance/query-token-info` | Nao aplicavel |

---

## Resumo Executivo

| Categoria | Ja temos | Parcial | Falta | Nova |
|---|---|---|---|---|
| Copy/Aquisicao | 0 | 3 | 8 | 2 |
| Marketing/Growth | 2 | 3 | 25 | 0 |
| Multimedia | 0 | 1 | 5 | 0 |
| Operational | 0 | 1 | 7 | 0 |
| Design | 0 | 0 | 5 | 0 |
| **Total** | **2** | **8** | **50** | **2** |

---

## Prioridade de Implementacao

### Alta (impacto direto em receita)
1. ✅ ~~`flux-copy-acquisition`~~ (feito hoje)
2. ✅ ~~`flux-campaign-orchestrator`~~ (feito hoje)
3. `email-sequence` — Sequencias de e-mail para leads e clientes
4. `sales-enablement` — Pitch deck, one-pagers, scripts de venda
5. `churn-prevention` — Fluxos de retencao e save offers
6. `social-content` — Conteudo organico Instagram/LinkedIn

### Media (eficiencia e escala)
7. `content-strategy` — Estrategia de conteudo sistematica
8. `analytics-tracking` — Setup e auditoria de tracking
9. `form-cro` — Otimizacao de formularios de captacao
10. `pricing-strategy` — Estrategia de precificacao dinamica
11. `referral-program` — Programa de indicacao entre clinicas
12. `ab-test-setup` — Testes A/B de criativo e copy

### Baixa (nice to have)
13. `notion-knowledge-capture` — Base de conhecimento
14. `spreadsheet` — Dashboards e analise
15. `frontend-skill` / `landing-page-builder` — Landing pages
16. `openai/speech` — Voz off para Reels
17. `openai/slides` — Apresentacoes de proposta

---

## Recomendacao Estrategica

Com **2 skills criadas hoje**, a Flux ja cobre o gap mais critico: **copywriting e orquestracao de campanha**.

**Proximos 30 dias:**
- Implementar `flux-copy-acquisition` em 2-3 campanhas reais
- Testar `flux-campaign-orchestrator` end-to-end
- Criar `email-sequence` e `sales-enablement` (alto impacto em conversao)

**Proximos 90 dias:**
- Criar `social-content` e `content-strategy` (escala de producao)
- Criar `churn-prevention` (retencao = receita recorrente)
- Avaliar `frontend-skill` para landing pages de captacao

---

*Mapeamento produzido por Flux Agency | Baseado em VoltAgent/awesome-agent-skills*
