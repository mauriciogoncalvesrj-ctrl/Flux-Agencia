---
name: flux-prompt-engineer
description: "Especialista em engenharia de prompt para geração de imagens da Agência Flux. Pipeline de 3 etapas: consulta especialistas → revisa prompts → gera imagens. Deve ser consultado ANTES de qualquer geração de imagem para clínica de estética."
version: 2.0.0
author: Hermes Agent — Agência Flux
metadata:
  hermes:
    tags: [prompt-engineering, image-generation, quality, flux-agency, estetica]
    related_skills: [fal-ai, social-media-carousels, ad-creative-design, gpt-image-2]
---

# Flux Prompt Engineer v2.0 — Pipeline Completo

**REGRA DE OURO:** Todo prompt de geração de imagem deve passar pelo pipeline de 3 etapas ANTES de ser enviado para qualquer gerador.

---

## Pipeline de Criação (3 Etapas Obrigatórias)

```
ETAPA 1: CONSULTA ESPECIALISTAS
  → Carregar skills relevantes para o tipo de criativo
  → Extrair specs técnicas (dimensões, safe zones, hierarquia visual)
  → Verificar base de prompts aprovados (prompts-db.json)

ETAPA 2: ENGENHARIA DE PROMPT
  → Estruturar prompt usando template específico por modelo
  → Validar contra checklist de qualidade
  → Salvar prompt aprovado na base

ETAPA 3: GERAÇÃO E ITERAÇÃO
  → Enviar prompt para modelo correto
  → Analisar resultado (score 1-10)
  → Se score < 7: registrar problema, ajustar prompt, tentar novamente
  → Se score ≥ 7: aprovar e registrar na base
```

---

## LLM para Engenharia de Prompt

O modelo **GLM-5.1** (opencode-go provider) é o melhor LLM disponível para engenharia de prompt de imagens:
- 1507B parâmetros — criativo e preciso em instruções visuais
- Forte em descrições detalhadas e composição de cenas
- Resposta direta (não-thinking), mais rápido para iteração
- Responde bem a instruções estruturadas em inglês

Alternativas: deepseek-v4-pro (raciocínio/qualidade), kimi-k2.6 (rapidez).

Lista completa de modelos Ollama Cloud: ver `references/ollama-cloud-models.md`.

**OBSERVAÇÃO:** A tabela de modelos/pricing abaixo tem sobreposição com o skill `fal-ai`. Use `fal-ai` para detalhes de API/MCP; este skill foca em **qual modelo usar para qual tipo de criativo**.

**Sobreposição com `fal-ai`:** Ambos skills listam modelos de geração de imagem. Regra: `fal-ai` é a fonte de verdade para API/MCP/pricing; este skill decide **qual modelo escolher para qual tipo de criativo** e fornece os templates de prompt.

---

## Etapa 1: Consulta aos Especialistas

### Para cada tipo de criativo, carregar os skills:

| Tipo de Criativo | Skills a Consultar | Conteúdo-Chave |
|------------------|-------------------|----------------|
| **Anúncio Meta (Feed/Stories/Carousel)** | `ad-creative-design` | Dimensões, limite de texto, safe zones, CTA placement |
| **Carrossel Instagram** | `social-media-carousels` | Template SVG, formato 1080×1350, estrutura narrativa |
| **Imagem com texto integrado** | `gpt-image-2` | Templates de prompt para layout com tipografia |
| **Identidade visual/branding** | `brand-identity-system`, `color-system`, `typography-pairing` | Paleta, fontes, consistência |
| **Layout de anúncio** | `landing-page-patterns`, `design-system-generator` | Hierarquia visual, CRO, composição |
| **Auditoria de resultado** | `design-critique`, `visual-audit` | Score DQS, dimensões de qualidade |

### Como consultar:
1. Carregar a skill com `skill_view(name='ad-creative-design')`
2. Extrair as specs relevantes para a plataforma alvo
3. Verificar se já existe prompt aprovado em `/opt/data/flux-tools/prompts-db.json`
4. Se existe: usar e adaptar. Se não: criar novo seguindo a Etapa 2.

---

## Etapa 2: Estrutura de Prompt por Modelo e Tipo

### 🎯 REGRA #1: Prompt SEMPRE em Inglês
Todos os modelos geram melhor em inglês. Texto final (headlines, CTA) pode ser em português DENTRO do prompt.

### 🎯 REGRA #2: Negativos no FINAL do prompt
Os modelos dão mais peso para o que vem no final. Poe exclusões no fim.

### Modelo A: Flux 2 Pro (fotorrealismo puro)
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

### Modelo B: image_generate (texto integrado na imagem)
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

### Modelo C: SVG Composite (controle total de tipografia)
Melhor para: carrosséis com múltiplos slides, tipografia complexa
- Gerar imagem de fundo com Flux 2 Pro (sem texto)
- Compor SVG com tipografia precisa sobre a imagem
- Ver skill `social-media-carousels` para templates

### Modelo D: GPT Image 2 (composição avançada)
Melhor para: layouts complexos com múltiplos elementos de UI/Design
- Via Fal.ai MCP ou `image_generate`
- Melhor renderização de texto entre os modelos de imagem
- Mais caro e lento (timeout frequente)
- Usar para criativos premium (1-5 por mês)

---

## Specs por Plataforma (Meta Ads)

Para **clínicas de estética**, a Meta Ads é a plataforma primária.

| Formato | Dimensões | Aspect | Texto < | Modelo |
|---------|----------|--------|---------|--------|
| Feed Post | 1080×1350 | 4:5 | 5% | image_generate |
| Feed Square | 1080×1080 | 1:1 | 5% | Flux 2 Pro |
| Stories/Reels | 1080×1920 | 9:16 | 125 chars | image_generate |
| Carousel Card | 1080×1350 | 4:5 | 5%/card | image_generate |
| Profile Grid | 1080×1080 | 1:1 | n/a | Flux 2 Pro |

### Safe Zones (Instagram Feed/Carousel)
```
┌──────────────────────┐
│    TOP 10% — Badge/Tag │ ← Não colocar texto essencial aqui
│                       │
│  INNER 80%            │ ← Zona segura para todo conteúdo
│                       │
│  BOTTOM 10% — CTA     │ ← Swipe-up / botão área
└──────────────────────┘
```

### Hierarquia Visual (F-Pattern para anúncios)
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

## Etapa 3: Checklist de Qualidade (ANTES de enviar)

- [ ] Prompt está em INGLÊS (texto final pode ser PT-BR dentro do prompt)
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

## Erros Comuns e Correções

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

---

## Arquivos de Referência

- `references/ollama-cloud-models.md` — Modelos LLM disponíveis no Ollama Cloud e configuração
- `references/approved-prompts.md` — Índice da base de prompts aprovados + paleta de cores

## Base de Prompts Aprovados

Local: `/opt/data/flux-tools/prompts-db.json`

### Categorias disponíveis:
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

### Como usar:
1. Ler a base: `cat /opt/data/flux-tools/prompts-db.json | jq '.spa_ambiente'`
2. Adaptar o prompt para o contexto específico
3. Se resultado for score ≥ 7, registrar variação na base

### Como registrar novo prompt aprovado:
Adicionar ao JSON com estrutura:
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

## Modelos Recomendados por Custo/Qualidade

| Uso | Modelo | Custo | Qualidade |
|-----|--------|------|-----------|
| Teste A/B (volume) | Flux Schnell | R$0,01/img | Boa |
| Feed post (diário) | Nano Banana 2 | R$0,46/img | Muito boa |
| Carrossel com texto | image_generate | Grátis* | Boa |
| Hero premium | Flux 2 Pro | R$0,85/img | Excelente |
| Criativo com UI | GPT Image 2 | Token-based | Melhor composição |
| Remoção de fundo | fal-ai/birefnet/v2 | R$0,02 | Perfeita |
| Upscale 2x/4x | fal-ai/clarity-upscaler | R$0,05-0,10 | Excelente |

*image_generate = ferramenta nativa do Hermes (não conta como custo Fal.ai)

---

## Integração com Pipeline de Conteúdo

Este skill integra com:
- **flux-agencia-conteúdo** → gera o briefing de texto primeiro
- **flux-agencia-copywriting** → fornece headlines e CTA para os slides
- **flux-agencia-trafego** → define qual formato/plataforma do criativo
- **social-media-carousels** → estrutura multi-slide com SVG
- **ad-creative-design** → specs técnicas da plataforma

### Fluxo de produção completo:
1. Conteúdo define qual procedimento e tipo de post
2. Copywriting escreve headline, subtítulo, CTA, legenda
3. **flux-prompt-engineer** (ESTE SKILL) consulta especialistas, estrutura prompt, valida
4. Geração com modelo correto
5. Tráfego seleciona formato e coloca no Meta Ads

---

## Templates de Carrossel (20 Posts de Estética)

Arquivo completo: `/opt/data/flux-tools/templates-instagram-estetica.md`

5 procedimentos × 5 formatos:
- **Bichectomia**: B1-Educativo, B2-Emocional, B3-Promocional, B4-Tendência, B5-FAQ
- **Harmonização**: H1-Educativo, H2-Prova Social, H3-Autoridade, H4-Sazonal, H5-Emocional
- **Preenchimento**: P1-Educativo, P2-Antes/Depois, P3-Promocional, P4-Mitos, P5-Lifestyle
- **Skinbooster**: S1-Educativo, S2-Resultado, S3-Sazonal, S4-Tira-dúvidas, S5-Glow

Cada template tem: formato, estrutura de slides, copy/legenda, hashtags e CTA.