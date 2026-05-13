---
name: flux-agency-standards
description: "Padrões de arquitetura, estrutura e qualidade para todas as skills da Agência Flux. Define template de SKILL.md, naming conventions, tools registry, e o modelo de product-marketing-context por cliente. Deve ser consultado ao criar, refatorar ou auditar qualquer skill do domínio flux/. Também usá-lo quando for analisar repositórios externos de skills para extrair melhorias aplicáveis à Flux."
version: 1.1.0
metadata:
  hermes:
    tags: [flux-agency, standards, architecture, skills, quality, skill-library]
    related_skills: [flux-orchestrator, flux-prompt-engineer, flux-meta-ads-balance-alert, flux-meta-ads-relatorio, flux-ads-audit, flux-competitor-spy, flux-daily-briefing, flux-toprank-seo, flux-x-monitor, flux-copy-estetica, flux-social-estetica, flux-landing-page-cro]
---

# Flux Agency Standards — Arquitetura de Skills

**Objetivo:** garantir que toda skill da Agência Flux siga padrões consistentes de estrutura, qualidade e integração, inspirados nas melhores práticas do ecossistema (ex: `coreyhaines31/marketingskills`).

---

## Princípios Fundamentais

1. **Product-Marketing-Context como fundação** — toda skill de marketing começa lendo o contexto do cliente
2. **Skills cross-referencing** — cada skill sabe quando delegar para outra
3. **Tools Registry centralizado** — catálogo unificado de MCPs, scripts e CLIs disponíveis
4. **Estrutura consistente de SKILL.md** — mesmo template para todas as skills
5. **Referências externas** — detalhes em `references/`, SKILL.md enxuto (<500 linhas)
6. **Evals e versionamento** — qualidade automatizada e tracking de versões

---

## Estrutura de Diretórios

```
skills/flux/
├── flux-agency-standards/          # ESTE SKILL — padrões e arquitetura\n│   ├── SKILL.md\n│   └── references/\n│       ├── tools-registry.md       # Catálogo de MCPs, scripts e CLIs\n│       └── skill-template.md       # Template canônico de SKILL.md\n│   └── templates/                  # Templates reutilizáveis (copy, CTAs, criativos)\n├── flux-prompt-engineer/           # Engenharia de prompt para imagens
├── flux-meta-ads-balance-alert/    # Alerta diário de saldo Meta Ads
├── flux-meta-ads-relatorio/        # Relatórios semanal/mensal Meta Ads
├── flux-ads-audit/                 # Auditoria de anúncios
├── flux-competitor-spy/            # Espionagem competitiva
├── flux-daily-briefing/            # Briefing diário de IA/marketing
├── flux-toprank-seo/               # SEO para clínicas de estética
├── flux-x-monitor/                 # Monitoramento X/Twitter
├── flux-social-estetica/             # Social media PT-BR para estética
├── flux-copy-estetica/               # Copywriting PT-BR para estética
├── flux-landing-page-cro/            # CRO PT-BR para landing pages de estética
├── VERSIONS.md                       # Tracking de versão centralizado
└── contexts/                       # Product-Marketing-Context por cliente
    ├── taciana.md
    ├── luana.md
    ├── proton.md
    └── alpha.md
```

---

## Template Canônico de SKILL.md

Toda skill Flux deve seguir esta estrutura (ordem fixa):

```markdown
---
name: flux-nome-da-skill
description: "O que faz + quando usar + trigger phrases. Mencionar skills relacionadas para scope boundaries."
version: X.Y.Z
prerequisites: []  # Skills que DEVEM ser carregadas antes desta (ex: [flux-competitor-spy])
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [skill-a, skill-b]
---

# Nome da Skill

**You are an expert [role].** Your goal is to [objetivo principal].

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered.

Gather this context (ask if not provided):
- [Contexto específico 1]
- [Contexto específico 2]

---

## [Framework/Processo Principal]

### Step 1: [Nome]
...

### Step 2: [Nome]
...

---

## Output Format

Definir formato exato do entregável esperado.

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| ... | ... | ... |

---

## Task-Specific Questions

1. [Pergunta 1]
2. [Pergunta 2]

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| ... | ... | MCP/CLI/Script | [link](path) |

---

## Related Skills

- **skill-x**: Para [quando usar]
- **skill-y**: Para [quando usar]
```

### Regras de nomenclatura

- Prefixo `flux-` obrigatório
- lowercase, hyphens, sem underscores
- Nome no nível de CLASSE (ex: `flux-ads-audit`, não `flux-audit-anuncio-taciana-hoje`)
- Máximo 64 caracteres
- Deve corresponder ao nome do diretório

---

## Product-Marketing-Context por Cliente

Cada cliente da Flux deve ter um arquivo de contexto em `skills/flux/contexts/{cliente}.md` contendo:

| Seção | Conteúdo |
|-------|----------|
| Product Overview | Nome da clínica, categoria, modelo de negócio |
| Target Audience | ICP, personas, dores, jobs to be done |
| Problems & Pain Points | Dores principais, por que alternativas falham |
| Competitive Landscape | Concorrentes diretos, secundários, indiretos |
| Differentiation | Diferenciais, como resolve diferente |
| Objections | Top 3 objeções + respostas |
| Customer Language | Como pacientes descrevem problemas (verbatim) |
| Brand Voice | Tom, estilo, personalidade |
| Proof Points | Métricas, depoimentos, cases |
| Goals | Meta primária, ação de conversão, métricas atuais |

**Uso:** toda skill Flux que interage com cliente DEVE começar lendo este arquivo.

---

## Tools Registry da Flux

Ver `references/tools-registry.md` para o catálogo completo. Resumo:

| Ferramenta | Tipo | Método | Status |
|------------|------|--------|--------|
| Meta Ads | Ads | MCP `mcp_meta_ads_*` + Graph API | ✅ Ativo |
| GHL | CRM/Automação | MCP `mcp_ghl_*` | ✅ Ativo |
| Fal.ai | Imagens/Vídeo | MCP `mcp_fal_ai_*` | ✅ Ativo |
| Open Design | Design UI | HTTP (design.somosflux.com.br:7456) | ✅ Ativo |
| Paperclip | Documentos | HTTP (paperclip.somosflux.com.br) | ✅ Ativo |
| X/Twitter | Social | xurl CLI | ⚠️ Sem credenciais |
| Google Ads | Ads | MCP `mcp_google_ads_*` | 🔧 Setup pendente |

### Scripts fixos

| Script | Propósito | Cron |
|--------|-----------|------|
| `/opt/data/scripts/meta_ads_real_balance.py` | Saldo real Meta Ads | `1ca2c29ca1d8` (9AM BRT) |
| `/opt/data/scripts/meta_ads_motiva_sms_context.sh` | SMS teste Motiva | `744263672cb4` (9AM BRT) |

---

## Lições do Marketing Skills (coreyhaines31)

Análise completa em 2026-05-12. Principais padrões absorvidos:

### O que já aplicamos (status 2026-05-12 — Grande Refatoração)
- ✅ **12 skills Flux** seguindo template canônico 9/9 seções (8 refatoradas + 3 criadas)
- ✅ **4 contextos de cliente** em `contexts/` (Taciana, Luana, Proton, Alpha) — modelo padronizado com 10 seções (campos a preencher via briefing)
- ✅ **VERSIONS.md** criado com tracking de versão + changelog
- ✅ **Tools Registry** completo em `references/tools-registry.md` — MCPs, CLIs, scripts fixos, cron jobs, domínios
- ✅ **Skills PT-BR** adaptadas: `flux-copy-estetica`, `flux-social-estetica`, `flux-landing-page-cro`
- ✅ Skills cross-referencing — cada skill sabe delegar para outras via Related Skills

### Pendências reais (2 itens)
- 🟡 **Adicionar `evals/`** nas skills para testes automatizados (padrão aspiracional; `coreyhaines31/marketingskills` usa `evals.json`)
- 🟡 **Criar `README.md`** no diretório `flux/` como índice navegável de todas as skills (padrão do marketingskills; cada skill linkada com descrição e tags)

### Melhorias aplicadas (2026-05-13 — Análise marketingskills #2)
- ✅ **`prerequisites`** adicionado ao template canônico de SKILL.md
- ✅ **`templates/`** adicionado à estrutura de diretórios por skill
- ✅ **Padrões de granularidade** documentados: skills devem ser classe, não monolíticas nem atômicas
- ✅ **`references/port-occupancy-debug.md`** adicionado ao `docker-traefik-routing` com método `/proc-only`

### Anti-padrões identificados (NÃO fazer)
- ❌ Skills com estruturas diferentes entre si (dificulta manutenção)
- ❌ Skills que não referenciam o product-marketing-context
- ❌ Skills sem "Common Mistakes" ou pitfalls
- ❌ Skills que não sabem quais ferramentas estão disponíveis
- ❌ Nomes de skill no nível de tarefa única (devem ser classe)

---

## Workflow de Criação/Atualização de Skill

1. **Antes de criar:** verificar se skill existente cobre o domínio (patch > create)
2. **Criar seguindo o template canônico** desta skill
3. **Registrar em `VERSIONS.md`** com versão inicial 1.0.0
4. **Adicionar evals** se possível (`evals/evals.json`)
5. **Referenciar tools relevantes** do registry
6. **Cross-reference** skills relacionadas
7. **Após uso real:** atualizar pitfalls e common mistakes com aprendizados

---

## Integração com Claude Code (Windows)

O usuário coordena Hermes Agent (VPS) com Claude Code (Windows) via:
- **Repo compartilhado:** `mauriciogoncalvesrj-ctrl/Flux-Agencia`
- **Protocolo:** `flux-comms/` directory para cross-agent communication
- **Memória:** cada ambiente tem seu `MEMORY.md` no repo

Skills Flux residem no Hermes Agent (VPS) e são a fonte de verdade para execução. O Claude Code no Windows pode consultar o repo para contexto, mas a execução de skills acontece no Hermes.
