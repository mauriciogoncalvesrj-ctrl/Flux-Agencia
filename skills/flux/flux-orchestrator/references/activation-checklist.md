# Activation Checklist — flux-orchestrator

Checklist que o agente DEVE seguir ao receber QUALQUER request do Mauricio.

## Passo 0: O request é multi-domínio?

Pergunte: este request envolve **2 ou mais** destas áreas?
- 🎨 Criativo (imagens, copy, design)
- 📊 Meta Ads (campanhas, relatórios, saldo)
- 🔍 Pesquisa (concorrentes, SEO, tendências)
- 🏢 CRM & Social (GHL, pipelines, posts)
- ⚙️ DevOps (infra, servidor, domínios)

**Se sim → ATIVAR ORQUESTRADOR.** Carregar `skill_view('flux-orchestrator')` imediatamente.

## Passo 0.1: HARD GATE de delegação

Antes de executar qualquer ação direta:

```
1. Domínios detectados: ________
2. Frentes independentes/paralelas: ________
3. Precisa MCP/side-effect exclusivo do orquestrador? ________
4. delegate_task chamado? SIM/NÃO + motivo
5. Modelo dos sub-agentes: herdado ou direcionado por delegation.*?
```

**Regra obrigatória:** se houver 2+ domínios ou 2+ frentes independentes, chamar `delegate_task(tasks=[...])` antes da solução direta. Se houver mais tarefas que `delegation.max_concurrent_children`, dividir em lotes.

**Só não delegar quando:**
- A tarefa for trivial e de domínio único;
- A execução depender de MCP/side-effect indisponível para sub-agentes;
- For apenas a síntese final dos outputs já delegados.

No relatório final, incluir: “Delegação: feita/não feita; motivo; modelo dos sub-agentes”.

## Passo 1: Classificar (5 segundos)

```
1. Cliente(s): ______________ → Se for a própria Flux Agência, pular contexts/ (não existe). Usar identidade Flux diretamente. Se for clínica, carregar contexts/{cliente}.md
2. Contexto tem dados reais? → Se cheio de [PREENCHER], alertar Mauricio
3. Domínios: _______________ → Quantos? (1 = delegar direto, 2+ = decompor)
4. Paralelizável? __________ → Sim = dispatcher paralelo, Não = sequencial
5. Precisa de MCPs? ________ → Se sim, orquestrador reserva
6. Vai gerar imagens? ______ → Se sim, ATIVAR MODO 5 PORTÕES (ver Passo 0.5)
```

## Passo 0.5: Vai gerar imagens? ATIVAR PIPELINE DE 5 PORTÕES

**SE o request envolve geração de imagens (carrossel, post, anúncio):**

```
⚠️ MODO 5 PORTÕES ATIVADO — Ver flux-prompt-engineer/references/pre-generation-checklist.md

PORTÃO 1 🖊️ Copywriter → flux-copy-estetica (aprova copy)
PORTÃO 2 🎨 Designer → social-media-carousels, ad-creative-design (aprova brief visual)
PORTÃO 3 ⚙️ Prompt Engineer → flux-prompt-engineer (aprova prompt técnico)
PORTÃO 4 🔍 Revisor → Orquestrador aplica pre-generation-checklist (score ≥ 8)
PORTÃO 5 🖼️ Geração + Auditoria → Orquestrador via MCP Fal.ai
```

**⚠️ Importante:** Usar a política vigente de roteamento: `flux-creative`/`deepseek-v4-pro` para portões criativos, `flux-vision`/`qwen3.5-plus` para análise visual, e `flux-orchestrator`/`deepseek-v4-pro` para síntese final. Não usar modelos legados como default criativo.

## Passo 2: Decompor e Anunciar

Escrever no chat o que vai acontecer:
```
🎯 Classificação: [N] domínios para [cliente]
⚠️ Pipeline de 5 portões ativado para geração de imagens
🔍 Delegando Research Agent: [tarefa] (paralelo com Portão 1)
🖊️ Portão 1 — Copywriter: [tarefa] (paralelo com Research)
⏳ Aguardando aprovação para avançar para Portão 2...
```

## Passo 3: Executar delegate_task

### FASE 1 — Paralelo (Research + Copywriter)
```
delegate_task(tasks=[
  {goal: "Pesquisar...", context: "...", toolsets: ["web", "search", "browser"]},
  {goal: "Criar copy...", context: "[flux-copy-estetica full content] + [cliente]", toolsets: ["file"]},
])
```

### FASE 2 — Sequencial (Designer → Prompt Engineer → Revisor → Geração)
Portões 2-5 executados sequencialmente, cada um dependendo do output aprovado do anterior.

## Passo 4: Sintetizar

Coletar outputs → Cruzar dados → Aplicar voz da marca → Preencher lacunas → Formatar entrega

## Anti-padrões

- ❌ Receber request multi-domínio e resolver sozinho sem carregar orquestrador
- ❌ Delegar sem anunciar os agentes (usuário não vê o que está acontecendo)
- ❌ Delegar com contexto vazio (sub-agente recebe `[PREENCHER]`)
- ❌ Não paralelizar quando possível (chamar delegate_task 3x sequencial em vez de 1x com array)
- ❌ Incluir texto (headlines, CTAs) no prompt de geração de imagem — modelos NÃO renderizam texto confiável. Gerar só o visual, aplicar texto via compose_images ou programaticamente
- ❌ Confiar cegamente nos dados do Research Agent — ferramentas web/browser podem falhar e o agente usa dados de treinamento. Revisar dados críticos na síntese
- ❌ **PULAR OS 5 PORTÕES** — gerar imagem sem copywriter, designer, prompt engineer e revisor. Este é o erro MAIS GRAVE. NUNCA gere sem o checklist completo.
- ❌ **Usar modelo errado nos portões criativos** — seguir `references/model-routing-policy.md`: criativo em `deepseek-v4-pro`, visão em `qwen3.5-plus`, GPT apenas para camada premium/devops.
- ❌ **Não consultar prompts-db.json** antes de criar novos prompts. Sempre verificar se já existe prompt aprovado similar.
- ❌ **Não registrar prompts aprovados** no `prompts-db.json` após geração bem-sucedida.
