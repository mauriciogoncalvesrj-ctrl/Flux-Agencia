# Pre-Generation Checklist — 5 Portões Obrigatórios

**REGRA DE OURO:** NUNCA gere uma imagem sem passar por TODOS os 5 portões. Cada portão produz um artefato aprovado que alimenta o próximo. Se qualquer portão falhar, PARE e corrija antes de avançar.

---

## PORTÃO 1: COPYWRITER 🖊️

**Skill responsável:** `flux-copy-estetica`
**Artefato produzido:** Copy aprovada (headline, corpo, CTA, legenda, hashtags)

### Checklist
- [ ] `flux-copy-estetica` foi carregada via `skill_view('flux-copy-estetica')`?
- [ ] Contexto do cliente carregado de `contexts/{cliente}.md` (ou identidade Flux para conteúdo autoral)?
- [ ] Canal e formato definidos (Instagram carrossel, Meta Ads, etc.)?
- [ ] Estágio de consciência do público identificado (problem-aware, solution-aware, etc.)?
- [ ] Framework de copy escolhido (PAS, BAB, Prova Social)?
- [ ] Headline segue fórmula testada (Dor+Solução, Pergunta, Número+Resultado)?
- [ ] CTA é específico (verbo de ação + o que ganha)?
- [ ] Compliance ANVISA/CFM verificado:
  - [ ] SEM promessa de resultado garantido
  - [ ] SEM jargão médico incompreensível
  - [ ] SEM comparação direta com concorrentes
  - [ ] SEM "sem dor", "sem riscos", "método milagroso"
- [ ] Linguagem da paciente > jargão médico?
- [ ] Uma ideia por slide/parágrafo?
- [ ] Objeções comuns respondidas?

**Gatekeeper:** A copy só avança se ≥ 5/5 nos critérios principais.

---

## PORTÃO 2: DESIGNER / DIREÇÃO DE ARTE 🎨

**Skills responsáveis:** `social-media-carousels`, `ad-creative-design`, `brand-identity-system`
**Artefato produzido:** Briefing visual completo (layout, paleta, tipografia, composição, safe zones, restrições)

### Checklist
- [ ] Skills de design carregadas (`social-media-carousels` para Instagram, `ad-creative-design` para Meta)?
- [ ] Formato/aspect ratio CORRETO para a plataforma destino?
  - Instagram Carrossel: 1080×1080 (1:1) ou 1080×1350 (4:5)
  - Meta Ads Feed: 1080×1350 (4:5)
  - Stories/Reels: 1080×1920 (9:16)
- [ ] Safe zones definidas? (top 10% = badge, inner 80% = conteúdo, bottom 10% = CTA)
- [ ] Hierarquia visual clara (F-Pattern: hook → imagem → detalhes → CTA)?
- [ ] Paleta de cores definida com hex codes?
- [ ] Tipografia definida (família, peso, tamanho para cada nível)?
- [ ] Estilo visual definido (ex: "editorial photography", "luxury medical aesthetic")?
- [ ] Elementos PROIBIDOS listados (ex: no people, no text on image, no clutter)?
- [ ] Elementos OBRIGATÓRIOS listados (ex: logo, gradiente, textura)?
- [ ] Brief visual é DETALHADO o suficiente? (cores, composição, elementos, iluminação, lente, estilo)
- [ ] Consistência visual garantida entre todos os slides? (paleta e estilo GLOBAL)
- [ ] Para texto complexo: estratégia definida (overlay pós-produção vs. texto integrado)?

**Gatekeeper:** O brief visual só avança se tiver TODOS os campos preenchidos — sem "imagem bonita" genérico.

---

## PORTÃO 3: ENGENHEIRO DE PROMPT ⚙️

**Skill responsável:** `flux-prompt-engineer`
**Artefato produzido:** Prompts técnicos em inglês, um por slide, prontos para geração

### Checklist
- [ ] `flux-prompt-engineer` carregada via `skill_view('flux-prompt-engineer')`?
- [ ] `prompts-db.json` consultado para prompts aprovados similares?
- [ ] Modelo correto escolhido para cada slide?
  - Imagem base sem texto → Flux 2 Pro / Seedream
  - Imagem com texto integrado → `image_generate`
  - Layout complexo com UI → GPT Image 2
- [ ] Prompt técnico está em INGLÊS? (regra #1)
- [ ] Exclusões (negativos) no FINAL do prompt? (regra #2 — modelos pesam mais o final)
- [ ] Estrutura do prompt segue o padrão do modelo?
  - Flux 2 Pro: FOTO STYLE → CENA → ELEMENTOS → COMPOSIÇÃO → PALETA → EXCLUSÕES
  - image_generate: LAYOUT → IMAGEM → TIPOGRAFIA → OVERLAY → ESTILO
- [ ] Termos técnicos de fotografia incluídos? (lente, abertura, iluminação)
- [ ] Paleta de cores com hex codes?
- [ ] Prompt entre 80-300 palavras?
- [ ] Todo texto visível está em PT-BR, exatamente como aprovado pelo copywriter?
- [ ] Texto na imagem < 20% da área (Meta Ads)?
- [ ] CTA está em zona segura (bottom 20%)?
- [ ] Custo estimado dos 10 slides < orçamento definido?

**Gatekeeper:** Prompt só avança se ≥ 8/10 no checklist. Prompts rejeitados voltam ao Portão 2 ou 3 para ajuste.

---

## PORTÃO 4: ANALISTA / REVISOR DE BRIEFING 🔍

**Skills responsáveis:** `design-critique`, `visual-audit`
**Artefato produzido:** Briefing final aprovado com score de prontidão, ou rejeição com feedback

### Checklist
- [ ] Copy final (Portão 1) está consistente com os prompts (Portão 3)?
- [ ] Brief visual (Portão 2) está fielmente traduzido nos prompts (Portão 3)?
- [ ] Aderência ao posicionamento da marca (Flux ou cliente)?
- [ ] Público-alvo correto? (B2B = donas de clínica, B2C = pacientes)
- [ ] Tom e voz consistentes em todos os slides?
- [ ] Compliance ANVISA/CFM/CONAR verificado em TODOS os slides?
- [ ] Nenhuma copy foi INVENTADA pelo engenheiro de prompt fora do aprovado pelo copywriter?
- [ ] Número de slides está correto para o formato?
- [ ] Slides 1 (capa) e último (CTA) têm atenção redobrada?
- [ ] Algum slide está genérico demais e precisa de refinamento?
- [ ] Dados do Research Agent (se houver) foram verificados? Não são alucinação?
- [ ] **Se dados do Research Agent usam fontes de treinamento (web tools falharam):**
  - [ ] Orquestrador marcou quais dados são verificáveis vs. inferidos?
  - [ ] Orquestrador complementou com busca própria (web_search nativo)?

**Gatekeeper:** 
- Score ≥ 8/10 → AVANÇAR para geração
- Score 5-7 → VOLTAR ao portão problemático com feedback específico
- Score < 5 → REPROVAR briefing; reiniciar do portão com problema

---

## PORTÃO 5: GERAÇÃO + AUDITORIA 🖼️

**Executor:** Orquestrador (MCP Fal.ai)
**Artefato produzido:** Imagens geradas + scores de qualidade + registro em `prompts-db.json`

### Checklist de Geração
- [ ] Todos os 4 portões anteriores foram APROVADOS?
- [ ] Modelo e parâmetros conferidos antes de disparar?
- [ ] Gerar 1 slide de teste primeiro? (slide 1 ou slide mais representativo)
- [ ] Se teste OK → gerar os demais (paralelo se possível)
- [ ] Texto NÃO foi incluído nos prompts de imagem base? (texto = overlay pós-produção)

### Checklist de Auditoria Pós-Geração
- [ ] **TODOS os slides** passaram por `vision_analyze`?
- [ ] Score DQS (Design Quality Score) atribuído a cada slide (1-10)?
  - Legibilidade: /5
  - Coerência visual: /5
  - Hierarquia: /5
  - CTA: /5
  - Premium feel: /5
- [ ] Slide com score < 8 → REPROVADO. Registrar problema e re-gerar.
- [ ] Texto alucinado detectado? → Se sim, re-gerar SEM texto no prompt.
- [ ] Consistência visual entre slides verificada? (mesma paleta, mesmo estilo)?
- [ ] Overlay de texto aplicado corretamente? (Python/Pillow ou compose_images)
- [ ] Texto final confere com a copy aprovada no Portão 1?

### Checklist de Registro
- [ ] Prompt APROVADO registrado em `prompts-db.json` com:
  - `model`: modelo usado
  - `image_size`/`aspect_ratio`: dimensão
  - `prompt`: prompt completo em inglês
  - `category`: categoria
  - `approved_by`: "flux-prompt-engineer"
  - `score`: nota final do Portão 5
- [ ] Se o prompt foi rejeitado e re-gerado, registrar o problema no campo `notes`?

---

## Resumo Rápido (para o Orquestrador)

Antes de disparar QUALQUER `mcp_fal_ai_generate_image`, confirme:

```
✅ Portão 1 (Copywriter): Copy aprovada? [ ]
✅ Portão 2 (Designer): Brief visual detalhado? [ ]
✅ Portão 3 (Prompt Engineer): Prompt técnico validado? [ ]
✅ Portão 4 (Revisor): Briefing aprovado com score ≥ 8? [ ]
⏳ Portão 5 (Geração): DISPARAR agora [ ]
```

Se QUALQUER checkbox estiver vazio → **NÃO gere.** Corrija o portão pendente primeiro.
