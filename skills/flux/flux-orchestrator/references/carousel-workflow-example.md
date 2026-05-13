# Carousel Workflow — Pipeline Completo de 5 Portões

**⚠️ Este workflow SUBSTITUI o anterior (2026-05-13).** O fluxo antigo (Research + Creative → Orquestrador) foi considerado INCOMPLETO em auditoria. O pipeline correto inclui 5 portões obrigatórios, cada um com aprovação antes do próximo.

## Estrutura do Fluxo Completo

```
MAURICIO: "cria carrossel educativo sobre [tema] para [cliente]"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ ORCHESTRATOR: Classifica → 2+ domínios → Decompõe       │
│                                                         │
│  FASE 1 — PARALELO                                      │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │ 🔍 Research Agent     │  │ 🖊️ PORTÃO 1: Copywriter  │ │
│  │ toolsets: web,search, │  │ Skill: flux-copy-estetica │ │
│  │   browser             │  │ toolsets: file            │ │
│  │ goal: tendências,     │  │ goal: headlines, copy,    │ │
│  │   concorrência, dores │  │   CTA, hashtags, legenda  │ │
│  │ output: dados mercado │  │ output: copy aprovada     │ │
│  └──────────┬───────────┘  └────────────┬─────────────┘ │
│             │                           │               │
│             ▼                           ▼               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ORCHESTRATOR: Revisa dados Research + Aprova Copy   │ │
│  │   • Verifica se dados Research são reais (não       │ │
│  │     alucinação) — complementa com busca própria     │ │
│  │   • Valida copy contra compliance ANVISA/CFM       │ │
│  └──────────────────────┬──────────────────────────────┘ │
│                         │                                │
│  FASE 2 — SEQUENCIAL (cada portão depende do anterior)  │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 🎨 PORTÃO 2: Designer / Direção de Arte             │ │
│  │ Skills: social-media-carousels, ad-creative-design  │ │
│  │ Input: copy aprovada + dados Research               │ │
│  │ Output: brief visual detalhado (paleta, composição, │ │
│  │   safe zones, hierarquia, restrições)               │ │
│  │ Gatekeeper: brief NÃO pode ser "imagem bonita"      │ │
│  └──────────────────────┬──────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ⚙️ PORTÃO 3: Engenheiro de Prompt                   │ │
│  │ Skill: flux-prompt-engineer                         │ │
│  │ Input: copy aprovada + brief visual                 │ │
│  │ Output: prompts técnicos em inglês, 1 por slide     │ │
│  │ Gatekeeper: consultar prompts-db.json, checklist    │ │
│  └──────────────────────┬──────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 🔍 PORTÃO 4: Analista / Revisor de Briefing        │ │
│  │ Skills: design-critique, visual-audit               │ │
│  │ Input: todos os artefatos dos portões 1-3           │ │
│  │ Output: score de prontidão ≥ 8 ou rejeição          │ │
│  │ Gatekeeper: NÃO gera se score < 8                   │ │
│  └──────────────────────┬──────────────────────────────┘ │
│                         │                                │
│                         ▼                                │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 🖼️ PORTÃO 5: Geração + Auditoria (Orquestrador)     │ │
│  │ MCP: mcp_fal_ai_generate_image                      │ │
│  │   • Gera 1 slide de teste → audita → aprova         │ │
│  │   • Gera demais slides com mesmo padrão             │ │
│  │   • Vision analyze em TODOS os slides               │ │
│  │   • Overlay de texto via Python/Pillow              │ │
│  │   • Score DQS (1-10) por slide                     │ │
│  │   • Registra prompts aprovados em prompts-db.json   │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## Responsabilidades por Portão

| Portão | Quem Executa | Como | Skills Obrigatórias |
|--------|-------------|------|---------------------|
| **1. Copywriter** | Sub-agente (delegate_task) | Paralelo com Research Agent | `flux-copy-estetica` |
| **2. Designer** | Sub-agente (delegate_task) | Sequencial — depende da copy aprovada | `social-media-carousels`, `ad-creative-design` |
| **3. Prompt Engineer** | Sub-agente (delegate_task) OU Orquestrador | Sequencial — depende do brief visual | `flux-prompt-engineer` |
| **4. Revisor** | **Orquestrador** diretamente | Aplica checklist de 12 pontos | `flux-prompt-engineer/references/pre-generation-checklist.md` |
| **5. Geração** | **Orquestrador** via MCP | Gera imagens + audita + registra | `fal-ai`, `vision_analyze` |

---

## Delegation Templates por Fase

### FASE 1: Paralelo (Research + Copywriter)

```python
delegate_task(tasks=[
    {
        goal: "Pesquisar tendências de conteúdo, dores do público-alvo e benchmarking competitivo sobre [tema]...",
        context: """
[PÚBLICO-ALVO]: [quem são, faixa etária, dores]
[OBJETIVO DA PESQUISA]: alimentar a copy e o design do carrossel
[FORMATO DE OUTPUT]:
  - 5-8 dores principais do público (com fontes ou marcadas como inferidas se web falhar)
  - 3-5 tendências de conteúdo para Instagram 2026
  - Benchmark de 3-5 concorrentes (o que postam, formatos, engajamento)
  - Tema recomendado + ângulo editorial
  - Palavras-chave e hashtags de alto alcance
[FONTES DESEJADAS]: Instagram, Sebrae, ABF, Google Trends
[NOTA]: Se ferramentas web/browser falharem, use dados de treinamento mas MARQUE como '[DADO INFERIDO]'.
""",
        toolsets: ["web", "search", "browser"]
    },
    {
        goal: "Criar copy completa para carrossel de 10 slides sobre [tema] para [cliente]...",
        context: """
[IDENTIDADE DA MARCA]: [cliente] — [descrever voz, tom, diferenciais]
[PÚBLICO-ALVO]: [ICP detalhado]
[FORMATO]: Instagram Carrossel (10 slides, 1080×1080 px)
[OBJETIVO]: [conversão desejada]

## CONTEÚDO DA SKILL FLUX-COPY-ESTETICA:
[COLAR conteúdo completo de flux-copy-estetica/SKILL.md]

## COMPLIANCE OBRIGATÓRIO:
- SEM promessa de resultado garantido (ANVISA/CFM)
- SEM jargão médico incompreensível
- Linguagem da paciente > jargão médico
- CTA específico com verbo de ação

## FORMATO DE OUTPUT:
### Slide 1 — CAPA
**Headline:** [hook — 3-5 palavras que param o scroll]
**Corpo:** [1-2 frases de contexto]
**Visual:** [descrição DETALHADA do que deve aparecer na imagem de fundo — cores, composição, elementos, iluminação, estilo]

[repetir para slides 2-10]

### 📝 Legenda do Post
[texto completo para caption do Instagram]

### #️⃣ Hashtags
[5-8 hashtags relevantes]

### 🎨 Briefing Visual Geral
[Paleta de cores, tipografia, estilo consistente para todos os slides]
""",
        toolsets: ["file"]
    }
])
```

### FASE 2: Sequencial (Designer → Prompt Engineer → Revisor → Geração)

**Portão 2 (Designer):** Orquestrador faz a direção de arte carregando `social-media-carousels` e `ad-creative-design`, ou delega como sub-agente.

**Portão 3 (Prompt Engineer):** Orquestrador carrega `flux-prompt-engineer`, consulta `prompts-db.json`, e converte cada brief visual em prompt técnico.

**Portão 4 (Revisor):** Orquestrador aplica `pre-generation-checklist.md`. Se score < 8, volta ao portão problemático.

**Portão 5 (Geração):** Orquestrador via `mcp_fal_ai_generate_image`.

---

## Limitação Conhecida: Sub-agentes herdam o modelo do Orquestrador

O `delegate_task` atual NÃO suporta override de modelo por task. Todos os sub-agentes usam o mesmo modelo do Orquestrador.

**Workaround para o futuro:**
- O Orquestrador pode trocar de modelo ANTES de delegar (ex: mudar para GLM-5.1 antes de delegar tarefas criativas, depois voltar para deepseek-v4-pro para síntese)
- Ou: portões 1-4 são executados pelo próprio Orquestrador (não como sub-agentes), permitindo trocar de modelo entre portões

**Recomendação atual:** Para carrosséis, o Orquestrador deve usar GLM-5.1 (melhor para prompt engineering) durante os portões 1-4, e deepseek-v4-pro apenas na síntese final.

---

## Métricas da Sessão Corrigida (2026-05-13)

| Métrica | Valor |
|---------|-------|
| Tempo Research Agent | ~7 min |
| Tempo Copywriter (Portão 1) | ~3 min (estimado, NÃO foi executado separadamente) |
| Tempo Designer (Portão 2) | ~5 min (estimado, NÃO foi executado) |
| Tempo Prompt Engineer (Portão 3) | ~5 min (estimado, NÃO foi executado) |
| Tempo Revisor (Portão 4) | ~3 min (estimado, NÃO foi executado) |
| Tempo Geração 10 imagens | ~12 min |
| **Tempo total estimado (pipeline completo)** | **~35 min** |
| **Tempo real gasto (pipeline incompleto)** | **~22 min** |

**Conclusão:** O pipeline completo adiciona ~13 minutos, mas elimina retrabalho, garante compliance, e produz criativos com qualidade consistentemente alta (score ≥ 8).

---

## Pitfalls ATUALIZADOS

| Pitfall | Sintoma | Correção |
|---------|---------|----------|
| Pular os 5 portões | Criativo gerado sem copy aprovada, sem direção de arte, sem revisão | Seguir `pre-generation-checklist.md` — NUNCA gerar sem checklist completo |
| Creative Agent acumula 3 papéis | Copywriter + Designer + Prompt Engineer no mesmo agente | Separar em portões distintos com gatekeepers |
| Não carregar `flux-copy-estetica` | Copy genérica, sem compliance, sem frameworks | Portão 1 OBRIGA carregar a skill |
| Não carregar `flux-prompt-engineer` | Prompts fracos, modelo errado, sem consulta ao `prompts-db.json` | Portão 3 OBRIGA carregar a skill |
| Não verificar dados do Research Agent | Dados de treinamento tratados como fato | Orquestrador revisa na Fase 1 e complementa com busca própria |
| Sub-agentes sem o melhor LLM | Copy/design criados com modelo analítico em vez de criativo | Orquestrador troca para GLM-5.1 antes dos portões criativos |
| Gerar sem consultar `prompts-db.json` | Prompts duplicados, sem rastreabilidade, sem melhoria contínua | Portão 3 consulta e Portão 5 registra |
| Não auditar com `vision_analyze` | Slides com texto alucinado, cores erradas, inconsistência visual | Portão 5 audita TODOS os slides |
| Não registrar score no `prompts-db.json` | Base de conhecimento não evolui | Portão 5 registra com score, modelo, e notas |

---

## Verificação Pós-Geração (inalterada)

Após gerar imagens, SEMPRE verificar com `vision_analyze`:
- Se a composição corresponde ao brief
- Se a paleta de cores está correta
- Se NÃO há texto alucinado na imagem
- Se o estilo está consistente com o brief geral
