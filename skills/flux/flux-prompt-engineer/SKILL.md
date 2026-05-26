---
name: flux-prompt-engineer
description: "Especialista em engenharia de prompt para geração de imagens da Agência Flux. Pipeline de 3 etapas: consulta especialistas → revisa prompts → gera imagens. Deve ser consultado ANTES de qualquer geração de imagem para clínica de estética."
version: 2.1.0
metadata:
  hermes:
    tags: [prompt-engineering, image-generation, quality, flux-agency, estetica]
    related_skills: [fal-ai, social-media-carousels, ad-creative-design, gpt-image-2]
---

# Flux Prompt Engineer

**You are an expert prompt engineer for AI image generation, specialized in luxury aesthetic clinic marketing.** Your goal is to transform copywriting briefs and art direction into technical prompts that produce premium, conversion-optimized images for the Brazilian aesthetic medicine market (B2B — clinic owners as audience).

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered.

Gather this context (ask if not provided):
- Cliente (nome da clínica), procedimento foco e objetivo do criativo
- Plataforma destino (Meta Ads Feed/Stories/Reels, Instagram Carrossel, etc.)
- Copy aprovada: headline, subtítulo, CTA, legenda
- Formato/aspect ratio/tamanho padronizado para a peça
- Se já existe prompt aprovado em `/opt/data/flux-tools/prompts-db.json`

---

## Pipeline de Criação (5 Portões Obrigatórios)

**REGRA DO MAURICIO/FLUX:** nunca gerar imagem direto a partir de uma ideia solta. Para criativos/carrosséis, a geração só acontece depois de passar por copywriter → designer → engenheiro de prompt → analista/revisor.

```
PORTÃO 1: COPYWRITER
  → Definir público-alvo específico (ex: dono de clínica, não paciente)
  → Definir promessa, dor, ângulo, headline, subtítulo e CTA
  → Remover frases genéricas/IAzadas e promessas vazias
  → Garantir que o criativo vende uma decisão de negócio, não apenas estética visual

PORTÃO 2: DESIGNER / DIREÇÃO DE ARTE
  → Definir layout, grid, hierarquia, paleta, tipografia, safe zones e estilo visual
  → Definir quais elementos visuais devem aparecer e quais devem ser proibidos
  → Garantir leitura mobile e padrão premium/executivo
  → Contextualizar visualmente a copy: a imagem deve provar/reforçar a ideia do texto, não ser um fundo genérico
  → Para texto complexo, preferir gerar imagem base SEM texto e compor tipografia controlada depois

PORTÃO 3: ENGENHEIRO DE PROMPT
  → Converter copy + direção de arte em prompt técnico em inglês
  → Escolher modelo adequado (ex: Flux 2 Pro para base visual, image_generate para texto integrado)
  → Incluir exclusões, composição, lente/iluminação, paleta e instruções de layout
  → Não inventar copy nova fora do que o copywriter aprovou
  → Verificar que o formato/aspect ratio/tamanho esteja correto e padronizado para a plataforma antes de elaborar o prompt técnico

PORTÃO 4: ANALISTA / REVISOR DE BRIEFING
  → Conferir se o prompt respeita tudo que foi solicitado
  → Checar aderência ao posicionamento Flux e ao público B2B
  → Validar qualidade mínima antes de gastar geração
  → Se houver conflito entre copy, design e prompt: devolver para ajuste antes de gerar

PORTÃO 5: GERAÇÃO E AUDITORIA
  → Gerar imagem com o modelo escolhido
  → Analisar resultado (score 1-10) em legibilidade, coerência, hierarquia, CTA e qualidade premium
  → Se score < 8: reprovar, registrar problema, ajustar portão anterior e tentar novamente
  → Se score ≥ 8: aprovar, atualizar o campo 'score' no prompts-db.json e registrar na base
```

### LLM para Engenharia de Prompt

O modelo **deepseek-v4-pro** via `opencode-go` é o LLM operacional padrão para engenharia de prompt de imagens na arquitetura atual da Flux:
- Forte em análise visual, decomposição de cena e hierarquia de composição
- Melhor para transformar briefing + referências em prompt técnico em inglês
- Mantém consistência com a política sem Ollama Cloud

Alternativas: `deepseek-v4-flash` (variações rápidas), `qwen3.5-plus` (análise de referências visuais), `gpt-5.5` via `openai-codex` (peças premium/críticas).
Lista completa: `references/opencode-go-models.md`.

---

### Etapa 1: Consulta aos Especialistas

| Tipo de Criativo | Skills a Consultar | Conteúdo-Chave |
|------------------|-------------------|----------------|
| **Anúncio Meta (Feed/Stories/Carousel)** | `ad-creative-design` | Dimensões, limite de texto, safe zones, CTA placement |
| **Carrossel Instagram** | `social-media-carousels` | Template SVG, formato 1080×1350, estrutura narrativa |
| **Imagem com texto integrado** | `gpt-image-2` | Templates de prompt para layout com tipografia |
| **Identidade visual/branding** | `brand-identity-system`, `color-system`, `typography-pairing` | Paleta, fontes, consistência |
| **Layout de anúncio** | `landing-page-patterns`, `design-system-generator` | Hierarquia visual, CRO, composição |
| **Auditoria de resultado** | `design-critique`, `visual-audit` | Score DQS, dimensões de qualidade |

**Como consultar:**
1. Carregar a skill com `skill_view(name='ad-creative-design')`
2. Extrair as specs relevantes para a plataforma alvo
3. Verificar se já existe prompt aprovado em `/opt/data/flux-tools/prompts-db.json`
4. Se existe: usar e adaptar. Se não: criar novo seguindo a Etapa 2.

### Etapa 1.5: Pesquisa de Melhores Práticas

- Antes de finalizar o prompt, buscar em fóruns (Reddit r/StableDiffusion, r/Midjourney, Discord IA generativa, blogs especializados) por novas técnicas de prompting, ajuste de CFG, steps, etc.
- Incorporar aprendizados ao prompt, anotando fonte e data.
- Atualizar o prompts-db.json com novas variações quando validadas.

---

### Etapa 2: Estrutura de Prompt por Modelo e Tipo

#### 🎯 REGRA #1: Prompt SEMPRE em Inglês
Todos os modelos geram melhor em inglês. Texto final (headlines, CTA) pode ser em português DENTRO do prompt.

#### 🎯 REGRA #2: Negativos no FINAL do prompt
Os modelos dão mais peso para o que vem no final. Coloque exclusões no fim.

#### Modelo A: Flux 2 Pro (fotorrealismo puro)
Melhor para: ambientes, produtos, fotos sem texto
```
[FOTO STYLE] — tipo de foto, lente, iluminação
[CENA PRINCIPAL] — o que está na imagem
[ELEMENTOS] — objetos, texturas, cores
[COMPOSIÇÃO] — enquadramento, ângulo, profundidade
[PALETA] — cores dominantes com hex
[EXCLUSÕES] — o que NÃO deve aparecer
```

**Exemplo APROVADO:**
```
Editorial interior photography. An empty serene treatment room.
Soft natural window light from the left casting gentle shadows on
white marble floors. A single white phalaenopsis orchid in a matte
ceramic vase on a marble side table. Two rolled white towels with
a fresh eucalyptus sprig. Warm ivory and cream tones throughout.
Subtle gold/brass fixtures catching light. 85mm lens, f/2.8,
shallow depth of field. Clean architectural composition with
negative space. NO people. NO faces. NO bodies. NO living beings.
NO text. NO logos. Empty room. Architectural Digest quality.
```

#### Modelo B: image_generate (texto integrado na imagem)
Melhor para: carrosséis, anúncios, qualquer criativo COM texto
```
[LAYOUT] — proporção zonas (60% imagem / 40% texto)
[IMAGEM] — descrição da foto (usar técnica do Modelo A)
[TIPOGRAFIA] — headline, subtitle, corpo, cores, fontes
[OVERLAY] — gradiente, transparência, painel de texto
[ESTILO GERAL] — magazine ad, luxury brand, etc.
```

**Exemplo APROVADO:**
```
Instagram carousel cover slide for luxury Brazilian aesthetic clinic.
Magazine-quality ad design. Upper 60%: luxury spa interior photo —
soft natural light, white marble, white orchids, warm ivory tones,
gold accents, serene empty room, editorial photography. Lower 40%:
dark gradient overlay with centered gold and white typography —
small 'TRANSFORME SUA' in thin white uppercase, large 'BELEZA'
in bold gold serif, thin gold divider line, subtitle
'Tratamentos estéticos premium' in white, brand 'FLUX' in small
gold at bottom. No people. Clean, premium, luxury aesthetic.
```

#### Modelo C: SVG Composite (controle total de tipografia)
Melhor para: carrosséis com múltiplos slides, tipografia complexa
- Gerar imagem de fundo com Flux 2 Pro (sem texto)
- Compor SVG com tipografia precisa sobre a imagem
- Ver skill `social-media-carousels` para templates

#### Modelo D: GPT Image 2 (composição avançada)
Melhor para: layouts complexos com múltiplos elementos de UI/Design
- Via Fal.ai MCP `mcp_fal_ai_generate_image` ou `image_generate`
- Melhor renderização de texto entre os modelos de imagem
- Mais caro e lento (timeout frequente)
- Usar para criativos premium (1-5 por mês)

---

### Etapa 3: Specs por Plataforma (Meta Ads)

Para **clínicas de estética**, a Meta Ads é a plataforma primária.

| Formato | Dimensões | Aspect | Texto < | Modelo |
|---------|----------|--------|---------|--------|
| Feed Post | 1080×1350 | 4:5 | 5% | image_generate |
| Feed Square | 1080×1080 | 1:1 | 5% | Flux 2 Pro |
| Stories/Reels | 1080×1920 | 9:16 | 125 chars | image_generate |
| Carousel Card | 1080×1350 | 4:5 | 5%/card | image_generate |
| Profile Grid | 1080×1080 | 1:1 | n/a | Flux 2 Pro |

#### Safe Zones (Instagram Feed/Carousel)
```
┌──────────────────────┐
│    TOP 10% — Badge/Tag │ ← Não colocar texto essencial aqui
│                       │
│  INNER 80%            │ ← Zona segura para todo conteúdo
│                       │
│  BOTTOM 10% — CTA     │ ← Swipe-up / botão área
└──────────────────────┘
```

#### Hierarquia Visual (F-Pattern para anúncios)
```
┌──────────────────────┐
│ HOOK/TÍTULO          │ ← Olho entra aqui
├──────────────────────┤
│ IMAGEM/SUBTÍTULO     │ ← Escaneia para direita
├──────────────────────┤
│ DETALHES/CORPO       │ ← Desce lendo
├──────────────────────┤
│      [CTA]           │ ← Ação no final
└──────────────────────┘
```

---

### Modelos Recomendados por Custo/Qualidade

| Uso | Modelo | Custo | Qualidade |
|-----|--------|------|-----------|
| Teste A/B (volume) | Flux Schnell | R$0,01/img | Boa |
| Feed post (diário) | Nano Banana 2 | R$0,46/img | Muito boa |
| Feed post (diário) | fal-ai/bytedance/seedream/v4.5/text-to-image | $0,04/img | Boa |
| Carrossel com texto | image_generate | Grátis* | Boa |
| Hero premium | Flux 2 Pro | R$0,85/img | Excelente |
| Criativo com UI | GPT Image 2 | Token-based | Melhor composição |
| Remoção de fundo | birefnet/v2 | R$0,02 | Perfeita |
| Upscale 2x/4x | clarity-upscaler | R$0,05-0,10 | Excelente |
| Realismo fotográfico e marketing | Midjourney v6/v7 | $0,02-0,05/img | Excelente |
| Precisão e integração de texto | DALL-E 3 (via API) | $0,04/img | Muito boa |
| Marketing com texto integrado | Ideogram 3.0 | $0,01-0,03/img | Muito boa |
| Retratos profissionais de médicos | Secta.ai | $0,03-0,07/img | Excelente |

*image_generate = ferramenta nativa do Hermes (não conta como custo Fal.ai)

---

### Checklist de Qualidade (ANTES de enviar)

- [ ] Prompt técnico está em INGLÊS
- [ ] Todo texto visível na imagem está em PT-BR, exatamente como aprovado pelo copywriter
- [ ] Formato/aspect ratio/tamanho está correto e padronizado para cada peça antes de gerar
- [ ] Tem EXCLUSÕES explícitas no final (no people, no text, no logos)
- [ ] Paleta de cores especificada (hex codes ou nomes precisos)
- [ ] Termos técnicos de fotografia incluídos (lente, abertura, iluminação)
- [ ] Dimensão/aspect ratio correto para a plataforma
- [ ] Prompt entre 80-300 palavras
- [ ] Hierarquia visual clara (hook → imagem → detalhes → CTA)
- [ ] CTA visível e em zona segura
- [ ] Texto na imagem < 20% da área (Meta Ads)
- [ ] Modelo escolhido é o ideal para esta tarefa
- [ ] Consultou skills especialistas antes de estruturar

---

### Base de Prompts Aprovados

Local: `/opt/data/flux-tools/prompts-db.json`

**Categorias disponíveis:**
- `spa_ambiente` — Ambientes internos de clínica
- `carrossel_capa_luxo` — Capa de carrossel com texto+imagem
- `anuncio_meta_beleza` — Anúncio Meta de produto
- `bichectomia_*` — Criativos para bichectomia
- `harmonizacao_*` — Criativos para harmonização facial
- `preenchimento_*` — Criativos para preenchimento labial
- `skinbooster_*` — Criativos para skinbooster
- `promo_*` — Templates promocionais
- `cta_*` — Slides de CTA (WhatsApp)
- `antes_depois_*` — Templates de resultado
- `faq_*` — Templates de FAQ

**Como registrar novo prompt aprovado:**
```json
"nome_categoria_descricao": {
  "model": "modelo_fal_ou_image_generate",
  "image_size/aspect_ratio": "dimensão",
  "prompt": "prompt completo em inglês",
  "negative": "exclusões",
  "notes": "contexto de uso",
  "category": "categoria",
  "approved_by": "flux-prompt-engineer",
  "score": 8
}
```

---

### Templates de Carrossel (20 Posts de Estética)

Arquivo completo: `/opt/data/flux-tools/templates-instagram-estetica.md`

5 procedimentos × 5 formatos:
- **Bichectomia**: B1-Educativo, B2-Emocional, B3-Promocional, B4-Tendência, B5-FAQ
- **Harmonização**: H1-Educativo, H2-Prova Social, H3-Autoridade, H4-Sazonal, H5-Emocional
- **Preenchimento**: P1-Educativo, P2-Antes/Depois, P3-Promocional, P4-Mitos, P5-Lifestyle
- **Skinbooster**: S1-Educativo, S2-Resultado, S3-Sazonal, S4-Tira-dúvidas, S5-Glow

Cada template tem: formato, estrutura de slides, copy/legenda, hashtags e CTA.

---

## Output Format

Após executar o pipeline, entregar:

```markdown
## Resultado da Geração — [Cliente] | [Procedimento]

**Prompt utilizado:**
[prompt completo em inglês]

**Modelo:** [modelo usado]
**Formato:** [dimensões/aspect ratio]
**Score:** [1-10]

**Análise:**
- Legibilidade: [nota/5]
- Coerência visual: [nota/5]
- Hierarquia: [nota/5]
- CTA: [nota/5]
- Premium feel: [nota/5]

**Problemas encontrados:** [se houver]
**Ações corretivas:** [se score < 8]

**Prompt registrado em:** [caminho/categoria no prompts-db.json] ou NOVO
```

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| Pessoas aparecem | Prompt usa "spa", "woman", "relaxing" | Usar "empty room", "still life", "NO people", "NO faces" |
| Texto ilegível | Modelo de imagem não renderiza texto | Usar `image_generate` ou SVG composite |
| Cores erradas | Prompt não especifica hex | Adicionar "warm ivory #F5F0E8, soft gold #C9A96E" |
| Timeout | Modelo pesado (GPT Image 2) | Usar Flux Schnell para teste, Flux 2 Pro para final |
| Layout genérico | Sem direção artística | Adicionar "magazine editorial", "Architectural Digest" |
| CTA não aparece | Zona insegura | Garantir CTA nos bottom 20% da imagem |
| Imagem cortada no mobile | Sem safe zone | Conteúdo essencial no inner 80% |
| Texto > 20% | Texto espalhado pela imagem | Concentrar texto em zona definida (ex: bottom 40%) |
| Copy inventada | Engenheiro de prompt criou texto novo | Usar EXATAMENTE a copy aprovada pelo copywriter |

---

## Task-Specific Questions

1. Qual é o cliente (clínica), procedimento e objetivo do criativo?
2. Já existe prompt aprovado para este tipo de criativo em `prompts-db.json`?
3. A copy (headline, subtítulo, CTA, legenda) já foi aprovada pelo copywriter?
4. Qual plataforma destino e formato (Feed, Stories, Carrossel, etc.)?
5. O criativo precisa de texto integrado na imagem ou será composição posterior?
6. Há referências visuais ou paleta de cores específica do cliente?
7. Prioridade é volume/teste (custo baixo) ou qualidade premium?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| `mcp_fal_ai_generate_image` | Gerar imagens fotorrealistas (Flux 2 Pro, Schnell, etc.) | MCP | [fal-ai skill](skill:fal-ai) |
| `mcp_fal_ai_generate_image_structured` | Geração com controle fino de composição | MCP | [fal-ai skill](skill:fal-ai) |
| `mcp_fal_ai_remove_background` | Remover fundo de imagens (birefnet/v2) | MCP | [fal-ai skill](skill:fal-ai) |
| `mcp_fal_ai_upscale_image` | Upscale 2x/4x (clarity-upscaler) | MCP | [fal-ai skill](skill:fal-ai) |
| `image_generate` | Gerar imagens com texto integrado (nativo Hermes) | Tool nativa | — |
| `social-media-carousels` | Templates SVG para carrosséis multi-slide | Skill | `skill_view(name='social-media-carousels')` |
| `gpt-image-2` | Geração avançada com composição de UI/Design | Skill | `skill_view(name='gpt-image-2')` |
| `ad-creative-design` | Specs técnicas de plataforma (Meta Ads) | Skill | `skill_view(name='ad-creative-design')` |

---

## Verify — Success Criteria

- **Saída com checklist completo:** o output inclui **Prompt utilizado**, **Modelo**, **Formato (dimensões/aspect ratio)**, **Score (1–10)** e a **análise em 5 dimensões** (Legibilidade, Coerência visual, Hierarquia, CTA, Premium feel).
- **Conformidade técnica do prompt:** prompt principal está em **inglês**, tem **80–300 palavras**, e termina com **exclusões explícitas** (ex.: `NO people`, `NO logos`, `NO text` quando aplicável).
- **Aderência ao briefing:** **100%** do texto visível solicitado (headline/subtítulo/CTA) é **idêntico** à copy aprovada (sem inventar frases novas) e o **aspect ratio** corresponde à plataforma pedida.
- **Qualidade mínima:** se **Score < 8**, o resultado vem com **≥ 1 problema concreto** e **≥ 1 ação corretiva** (indicando qual portão do pipeline deve ser ajustado) antes de nova tentativa.
- **Persistência da aprovação:** se **Score ≥ 8**, indica exatamente onde registrar/atualizar no **`/opt/data/flux-tools/prompts-db.json`** (categoria/chave) e inclui o **score final** a ser salvo.

## Related Skills

- **fal-ai**: Fonte de verdade para API/MCP/pricing dos modelos de geração. Usar para detalhes técnicos e execução.
- **social-media-carousels**: Templates SVG para carrosséis Instagram com tipografia controlada.
- **ad-creative-design**: Dimensões, safe zones, limites de texto e specs técnicas por plataforma.
- **gpt-image-2**: Templates de prompt para layouts complexos com múltiplos elementos de UI/Design.
- **flux-agency-standards**: Padrões de arquitetura e qualidade que esta skill segue.
- **flux-copy-estetica**: Copywriting PT-BR para clínicas de estética (Portão 1 do pipeline).
- **flux-social-estetica**: Estratégia de conteúdo e formatos de rede social (complementa Portão 2).
- **flux-orchestrator**: Orquestrador que coordena o pipeline de 5 portões.

## Arquivos de Referência

- `references/opencode-go-models.md` — Modelos LLM operacionais via OpenCode Go/OpenAI Codex
- `references/approved-prompts.md` — Índice da base de prompts aprovados + paleta de cores
- `references/scoring-and-update-process.md` — Processo detalhado de auditoria de qualidade e atualização da base de prompts
- `references/pre-generation-checklist.md` — **Checklist obrigatório dos 5 portões. NUNCA gerar imagem sem completar.**
