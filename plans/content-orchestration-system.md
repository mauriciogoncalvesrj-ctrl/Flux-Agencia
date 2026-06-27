# Flux Content Orchestration System — Plano de Implementação

> Data: 2026-06-27
> Status: PLANO — aguardando aprovação

---

## 1. Problema Atual

O pipeline de conteúdo gera imagens e copy **sem análise prévia, sem estratégia, sem revisão**. Resultado: conteúdo que viola brand rules, não se encaixa em nenhum território visual, e não passa em auditoria (2.25/10).

**Causa raiz:** Não existe setor de Inteligência nem de Qualidade — só existe Execução.

---

## 2. Arquitetura — 5 Setores

Inspirado no SEO Agency in a Box (75 agentes, 12 teams, vault system) e adaptado pra realidade Flux.

```
┌─────────────────────────────────────────────────────────┐
│                   FLUX ORCHESTRATOR                      │
│            (recebe pedido → roteia setores)              │
└──────────┬──────────┬──────────┬──────────┬─────────────┘
           │          │          │          │
     ┌─────▼─────┐ ┌──▼───┐ ┌───▼───┐ ┌───▼───┐ ┌────────┐
     │INTELIGÊNCIA│ │ESTRAT│ │CRIAÇÃO│ │QUALITY│ │DISTRIB │
     │  (fase 1)  │ │(f.2) │ │ (f.3) │ │ (f.4) │ │ (f.5)  │
     └────────────┘ └──────┘ └───────┘ └───────┘ └────────┘
```

### Setor 1: Inteligência (ANALISAR)
**O quê:** Pesquisa de mercado, análise de concorrentes, tendências de conteúdo, social listening
**Quem:** 3 sub-agentes paralelos
**Modelo:** deepseek-v4-pro (raciocínio longo)
**Output:** Relatório de insights no vault/03-Research/

| Sub-agente | Função |
|------------|--------|
| `intel-social` | Analisa tendências de conteúdo em redes sociais do nicho (clínicas estética) |
| `intel-competitor` | Espiona concorrentes diretos (conteúdo, formatos, engajamento) |
| `intel-trends` | Identifica tendências sazonais, gatilhos, hooks que estão funcionando |

### Setor 2: Estratégia (PLANEJAR)
**O quê:** Definir pilares de conteúdo, calendário, selecionar tópicos, definir território visual
**Quem:** 1 agente estrategista
**Modelo:** mimo-v2.5-pro (Planejamento)
**Output:** Briefing estruturado no vault/04-Content/

| Decisão | Como |
|---------|------|
| Pilar de conteúdo | Baseado em dados da Inteligência |
| Território visual | 1 dos 5 aprovados (Dona Sobrecarregada, Agenda Vazando, WhatsApp Sistema, Operação Silenciosa, Dossiê) |
| Formato | Carrossel, post único, story, reel |
| Tom | Agressivo, autoritário, provocativo (brand voice) |
| Hooks | Dos 6 hooks aprovados no brand profile |
| CTA | Dos 4 CTAs aprovados |

### Setor 3: Criação (EXECUTAR)
**O quê:** Gerar copy + visual + overlay
**Quem:** 3 sub-agentes paralelos
**Modelo:** mimo-v2.5 (copy), Fal.ai (imagens), Pillow (overlay)
**Output:** PNGs + copy.json no vault/04-Content/drafts/

| Sub-agente | Função |
|------------|--------|
| `create-copy` | Gera copy seguindo template do território, hooks aprovados, UPPERCASE, tom agressivo |
| `create-visual` | Gera prompts de imagem baseados no território visual, paleta correta (preto+dourado) |
| `create-composer` | Compõe overlay com Montserrat Black, hierarquia correta, selo editorial, badge FLUX |

### Setor 4: Qualidade (REVISAR)
**O quê:** Auditoria contra brand rules, DESIGN.md, compliance ANVISA/CFM
**Quem:** 2 sub-agentes paralelos + síntese
**Modelo:** deepseek-v4-pro (análise crítica)
**Output:** Score + lista de correções no vault/04-Content/reviews/

| Sub-agente | Função |
|------------|--------|
| `qa-brand` | Verifica paleta, tipografia, tom, estrutura, templates, território |
| `qa-compliance` | Verifica ANVISA/CFM, claims sem prova, linguagem proibida |

**Scoring:** 1-10 por critério. Média mínima: 7/10 para aprovação.
**Se reprovado:** volta pro Setor 3 com correções específicas (máx 2 iterações).

### Setor 5: Distribuição (PUBLICAR)
**O quê:** Agendar posts, formatar por plataforma, gerar legendas
**Quem:** 1 agente
**Modelo:** mimo-v2.5
**Output:** Posts agendados via GHL MCP ou prontos pra manual

| Plataforma | Formato | Specs |
|------------|---------|-------|
| Instagram Feed | 4:5 (1080x1350) | Carrossel ou post único |
| Instagram Story | 9:16 (1080x1920) | Sequência de slides |
| Instagram Reels | 9:16 | Vídeo curto (HyperFrames) |
| Facebook | 4:5 | Mesmo conteúdo Instagram |
| LinkedIn | 1:1 ou 4:5 | Tom mais institucional |

---

## 3. Fluxo de Execução

### Fluxo padrão (1 post completo)
```
1. PEDIDO chega ao Orchestrator
   │
2. INTELIGÊNCIA (3 agentes paralelos, ~2min)
   │  ├─ intel-social: tendências do nicho
   │  ├─ intel-competitor: o que concorrentes postam
   │  └─ intel-trends: gatilhos sazonais
   │
3. ESTRATÉGIA (1 agente, ~1min)
   │  └─ Seleciona: pilar, território, formato, hooks, CTA
   │
4. CRIAÇÃO (3 agentes paralelos, ~3min)
   │  ├─ create-copy: copy estruturada
   │  ├─ create-visual: prompts de imagem
   │  └─ create-composer: monta PNG final
   │
5. QUALIDADE (2 agentes paralelos + síntese, ~1min)
   │  ├─ qa-brand: auditoria visual/copy
   │  ├─ qa-compliance: ANVISA/CFM
   │  └─ Síntese: score + correções
   │
6. Se score >= 7 → DISTRIBUIÇÃO
   Se score < 7 → volta para CRIAÇÃO (máx 2x)
   │
7. DISTRIBUIÇÃO (1 agente, ~1min)
   └─ Agenda via GHL MCP ou exporta manual
```

**Tempo total estimado:** ~8-10 minutos por post completo

### Fluxo rápido (só copy + imagem, sem inteligência)
```
PEDIDO → CRIAÇÃO → QUALIDADE → DISTRIBUIÇÃO
```
**Tempo:** ~4-5 minutos

---

## 4. Modelos por Tarefa

| Tarefa | Modelo | Justificativa |
|--------|--------|---------------|
| Inteligência (análise) | deepseek-v4-pro | Raciocínio longo, dados complexos |
| Estratégia (planejamento) | mimo-v2.5-pro | Planejamento estruturado |
| Copy (texto) | mimo-v2.5 | Rápido, bom em copy PT-BR |
| Visual (prompts) | mimo-v2.5 | Criativo, bons prompts de imagem |
| Imagem (geração) | Fal.ai Schnell | Rápido, barato ($0.003/img) |
| Qualidade (auditoria) | deepseek-v4-pro | Análise crítica rigorosa |
| Distribuição | mimo-v2.5 | Simples, formatação |

---

## 5. Vault — Memória Compartilhada

Inspirado no SEO Agency in a Box, cada setor escreve no vault, downstream lê:

```
vault/
├── 00-Dashboard/        # Status, métricas
├── 01-Clientes/         # Perfis, brand voice
├── 03-Research/         # Insights da Inteligência
├── 04-Content/
│   ├── briefings/       # Briefings estruturados (Setor 2)
│   ├── drafts/          # Copies + PNGs (Setor 3)
│   ├── reviews/         # Auditorias (Setor 4)
│   └── published/       # Conteúdo aprovado e publicado
└── 05-Templates/        # Templates de copy e visual
```

---

## 6. Skills Necessárias

### Do skills.sh (instalar)
- `social-content` — conteúdo nativo LinkedIn/X/Instagram
- `content-strategy` — calendários editoriais
- `copywriting` — headlines, landing pages, ads
- `ad-creative` — briefs de criativo performance
- `marketing-psychology` — gatilhos comportamentais

### Próprias (já existem, adaptar)
- `flux-ad-creator` — criação de ads Meta para clínicas
- `flux-image-studio` — pipeline de geração de imagem
- `flux-copy-acquisition` — copy de aquisição B2B

---

## 7. Quality Gate — Checklist

Todo conteúdo deve passar:

| # | Check | Critério |
|---|-------|----------|
| 1 | Hook aprovado | Usa 1 dos 6 hooks do brand profile? |
| 2 | UPPERCASE | Headline em caixa alta para impacto? |
| 3 | Paleta correta | Preto + branco + dourado (não ciano dominante)? |
| 4 | Fonte correta | Montserrat Black, tamanho 50-65% da imagem? |
| 5 | Território | Encaixa em 1 dos 5 territórios visuais? |
| 6 | Estrutura | Selo + headline + bullets + solução + CTA + branding? |
| 7 | CTA aprovado | Usa 1 dos 4 CTAs do brand profile? |
| 8 | Compliance | Sem claims sem prova, sem ANVISA/CFM onde necessário? |
| 9 | Brand voice | Tom agressivo, direto, provocativo? |
| 10 | Legibilidade | Texto lido em <1.5 segundos? |

**Score:** Média >= 7 → APROVADO. Média < 7 → REVISAR.

---

## 8. Implementação — Fases

### Fase 1: Foundation (1-2 dias)
- [ ] Criar estrutura do vault
- [ ] Instalar skills do skills.sh (social-content, content-strategy, copywriting, ad-creative, marketing-psychology)
- [ ] Criar arquivos de agente para cada setor
- [ ] Criar templates de briefing e auditoria

### Fase 2: Orchestrator (1 dia)
- [ ] Criar `flux-orchestrator.js` workflow que roteia pedidos
- [ ] Definir regras de roteamento (pedido → setores → agentes)
- [ ] Integrar com vault (leitura/escrita)

### Fase 3: Pipeline Corrigido (1-2 dias)
- [ ] Corrigir `gerar_copy.py` — hooks aprovados, UPPERCASE, tom agressivo
- [ ] Corrigir `compor_texto.py` — paleta preto+dourado, Montserrat Black, hierarquia
- [ ] Corrigir `briefing.py` — prompts baseados em território visual
- [ ] Adicionar selo editorial + badge FLUX + somosflux.com.br

### Fase 4: Quality Gate (1 dia)
- [ ] Criar `qa-brand.md` — checklist de auditoria visual
- [ ] Criar `qa-compliance.md` — checklist ANVISA/CFM
- [ ] Integrar no pipeline: copy+imagem → auditoria → aprovação → distribuição

### Fase 5: Social Posting (1 dia)
- [ ] Integrar GHL MCP pra agendar posts
- [ ] Template de caption com hooks + CTA
- [ ] Formatos por plataforma (Instagram, Facebook, LinkedIn)

---

## 9. Comando Final

```bash
# Fluxo completo: inteligência + estratégia + criação + quality + distribuição
/flux-content "criar carrossel sobre 5 erros de tráfego para clínicas"

# Fluxo rápido: só criação + quality
/flux-content-rapido "post sobre agenda vazando"
```

---

## 10. Referências

- **SEO Agency in a Box** — arquitetura de 75 agentes, vault system, quality gates
- **skills.sh** — 21 marketing skills (social-content, copywriting, ad-creative, content-strategy)
- **Brand Profile** — hooks, paleta, territórios, templates aprovados
- **DESIGN.md** — DNA visual, estrutura obrigatória, regras de cor
- **Creative Templates** — 4 territórios visuais com prompts prontos
