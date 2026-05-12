---
name: ads-carousel
description: "Text-heavy carrossel generator no padrao Flux Agency (clinicas de estetica BR). Gera carrosseis de 4-10 slides com tipografia bold uppercase PT-BR, paleta preto+dourado+cyan+alerta, e 4 sub-estilos (cyber/luxo/alerta/personal-brand). Diferente de ads-generate: ESTE skill PERMITE e EXIGE texto na imagem. Triggers on: carrossel, criativo Flux, padrao Flux, slide instagram, post clinica, criativo de clinica, gerar carrossel."
user-invokable: true
---

# Ads Carousel: Gerador de Carrossel Padrao Flux

Gera carrosseis Instagram (4-10 slides) seguindo o DNA visual da Flux Agency.
Diferente da skill `ads-generate` (que proibe texto na imagem), esta skill
**injeta o texto como parte do design** — porque no padrao Flux a headline E o anuncio.

## Quick Reference

| Comando | O que faz |
|---------|-----------|
| `/ads carousel` | Modo interativo: pergunta tema e gera 7 slides |
| `/ads carousel --tema "ralo de dinheiro" --slides 7` | Gera carrossel especifico |
| `/ads carousel --estilo luxo` | Forca sub-estilo (luxo, cyber, alerta, personal) |
| `/ads carousel --estilo personal` | Carrossel com foto do Mauricio |

## Pre-requisitos

- `~/.banana/presets/flux-clinicas.json` deve existir (criado em 2026-05-12)
- `projects/c--Users-windows--claude/docs/creative/flux-brand/flux-brand-profile.json` deve existir
- banana-claude com nanobanana-mcp configurado

## Os 4 Sub-Estilos Flux

Sempre selecione UM dos 4 antes de gerar (ou misture entre slides):

### A. Cyber/Tech (azul-cyan + preto)
- **Usar quando:** hooks sobre IA, futuro, dados, transformacao, 2026
- **Paleta:** `#0A1428` deep navy + `#00D4FF` electric cyan + `#FFFFFF`
- **Elementos:** HUD, holograma humano, circuitos azuis, dashboards futuristas
- **Exemplo:** "O FIM DAS CLINICAS COMUNS EM 2026", "RAIO-X DO LUCRO"

### B. Luxo/Educacional (preto + dourado)
- **Usar quando:** carrossel educacional, prova social, lista numerada, autoridade
- **Paleta:** `#0A0A0A` preto + `#C9A961` dourado + `#E8DCC4` cream + `#FFFFFF`
- **Elementos:** icones line-art dourados, paginacao top-right (1/7), tipografia bold condensada
- **Exemplo:** "O RALO DE DINHEIRO", "TRAFEGO SEM FUNIL", "ESTRATEGIA + SISTEMA"

### C. Alerta/Polemico (preto + amarelo alerta + vermelho)
- **Usar quando:** hooks de medo, urgencia, denuncia, problema doloroso
- **Paleta:** `#0A0A0A` + `#FFB400` warning yellow + `#D62828` red
- **Elementos:** faixas listradas amarelo/preto, triangulo de alerta, fagulhas, concreto rachado
- **Exemplo:** "LEAD BARATO VAI QUEBRAR SUA CLINICA", "PARE DE PERDER DINHEIRO"

### D. Personal Brand (preto + dourado + foto Mauricio)
- **Usar quando:** autoridade pessoal, CTA do fundador, branding pessoal
- **Paleta:** preto + dourado + foto do Mauricio (blazer marrom-bege OU jaqueta verde-oliva, camiseta preta, barba grisalha)
- **Layout:** Mauricio a direita 40-50%, headline grande a esquerda
- **Exemplo:** "O CEREBRO POR TRAS DA SUA ESCALA", "IA NAO E MAGICA, E METODO"

## Processo

### Step 1: Verificar Preset Flux

Confirmar que `~/.banana/presets/flux-clinicas.json` existe. Se nao existir, parar e instruir o usuario a rodar o setup do brand-profile.

### Step 2: Coletar Inputs

Perguntar em UMA mensagem:
1. **Tema/dor:** Qual problema/oportunidade da clinica? (ex: "leads que nao convertem", "no-show alto")
2. **Numero de slides:** 4, 6, 7 ou 10 (default: 7)
3. **Sub-estilo dominante:** A (cyber) | B (luxo) | C (alerta) | D (personal) | mix
4. **CTA final:** palavra-chave do comentario (ex: "FUNIL", "ESTRATEGISTA", "RAIO-X")

### Step 3: Estruturar o Carrossel

Use o **template Flux de 7 slides** (ajustar para 4/6/10):

| Slide | Funcao | Sub-estilo recomendado |
|-------|--------|------------------------|
| 1 | Hook polemico/pergunta (capa) | C (alerta) ou A (cyber) |
| 2 | Problema 1 + agitar | B (luxo) |
| 3 | Problema 2 + agitar | B (luxo) ou C (alerta) |
| 4 | Custo de nao agir (numero forte) | C (alerta) |
| 5 | Solucao Flux (metodo) | B (luxo) ou A (cyber) |
| 6 | Prova social (60+ clinicas) | B (luxo) |
| 7 | CTA "Comenta X" + chevron | C (alerta) ou D (personal) |

### Step 4: Construir o Banana Prompt para CADA Slide

Use a formula **Flux 6-Component** (diferente da formula 5-component da ads-generate):

```
[SUB_STYLE] aplicado do flux-clinicas.json
[HEADLINE_TEXT] texto literal em PT-BR a ser renderizado na imagem, UPPERCASE, em fonte bold condensada
[SUBHEAD_TEXT] subtitulo curto em PT-BR (opcional)
[PAGE_NUMBER] formato N/N posicionado top-right (ex: "1/7")
[VISUAL_ELEMENT] objeto/cena/textura que ocupa 25-35% da imagem
[COMPOSITION] headline 50-65% area, visual a direita ou background, CTA bottom
```

**REGRAS CRITICAS — DIFERENTE da ads-generate:**

1. **PERMITIR texto na imagem.** NUNCA adicionar "no text, no labels, no readable words". O texto E o design.
2. **Especificar o texto literal** entre aspas no prompt: `headline text "O RALO DE DINHEIRO" in bold uppercase condensed sans-serif gold color #C9A961`
3. **Sempre PT-BR**, com acentuacao correta.
4. **Forcar a paleta:** comecar o prompt com `"#0A0A0A deep black background, #C9A961 gold accent"`.
5. **Especificar fonte:** "Anton font OR Bebas Neue OR Oswald style — condensed bold uppercase sans-serif".
6. **Page number:** adicionar `"page indicator '1/7' in small pill top-right corner, gold border"`.

### Step 5: Exemplo Completo de Prompt (Sub-estilo B - Luxo)

Para o slide "O RALO DE DINHEIRO" (1/7):

```
#0A0A0A deep black background, #C9A961 gold premium accent,
headline text "O RALO DE DINHEIRO" rendered in massive bold uppercase condensed
sans-serif (Anton/Bebas Neue style), white #FFFFFF top word and gold #D4AF37
bottom word, occupying 55% of left half of frame.
Subhead text "Por que sua clinica atrai leads, mas nao lucra?" in smaller
medium-weight sans-serif white below headline.
Top-right corner: small pill-shaped page indicator "1/7" with gold border
on dark background.
Right 40% of frame: dramatic close-up photograph of a metal drain with
brazilian Real banknotes (R$100, R$50) being sucked down, water splash,
deep shadows, cinematic low-key lighting, warm gold rim light from upper-left.
Bottom edge: thin gold diagonal ornament line, three small gold icons with
micro-labels "Voce atrai leads / Mas perde pelo caminho / E o lucro escorre".
Aspect ratio 4:5 (1080x1350), instagram carousel format, premium luxury
direct-response brazilian aesthetic, no cheesy stock, no white background.
```

### Step 6: Gerar via Banana MCP

Para cada slide:
1. Ativar preset: `banana activate-preset flux-clinicas`
2. `set_aspect_ratio` 4:5 (1080x1350)
3. `gemini_generate_image` com o prompt construido
4. Salvar em `./ad-assets/flux-carrossel/[tema-slug]/slide-[N]-of-[total].png`
5. Para sub-estilo D (Personal Brand): passar a foto de referencia do Mauricio como image input se disponivel em `~/.claude/projects/c--Users-windows--claude/docs/creative/refs-mauricio/`

### Step 7: Validacao Visual

Apos gerar cada slide, usar Claude vision para checar:
- [ ] Texto da headline esta legivel e correto em PT-BR (sem typo de acentuacao)
- [ ] Paleta esta dentro da paleta Flux (preto/dourado/cyan/alerta — sem rosa/pastel/azul-bebe)
- [ ] Page number aparece top-right
- [ ] Composicao: headline domina, visual a direita/atras
- [ ] Sub-estilo coerente com o tema

Se algum slide falhar, regerar UMA vez com prompt ajustado.

### Step 8: Output e Relatorio

```
Carrossel Flux gerado: [tema]
Sub-estilo dominante: [A/B/C/D/mix]
Slides:
  ✓ slide-1-of-7.png — Hook: "[headline]" (estilo C)
  ✓ slide-2-of-7.png — Problema: "[headline]" (estilo B)
  ...
  ✓ slide-7-of-7.png — CTA: "Comenta [PALAVRA]" (estilo C)

Salvos em: ./ad-assets/flux-carrossel/[tema-slug]/
Custo total: $[N] (banana)
Proximo: revisar slides e postar no Instagram da @somosflux
```

## Sequencia de Hooks Padrao (Templates Prontos)

Use estes como ponto de partida — substituir [variavel]:

### Template 1: O Ralo (problema oculto)
1. "O RALO DE [PROBLEMA]" — hook
2. "O LEAD ESFRIA EM MINUTOS" — velocidade
3. "TRAFEGO SEM FUNIL" — sistema furado
4. "O CUSTO DA NAO-ESTRATEGIA" — 70% de perda
5. "NOSSA SOLUCAO: FUNIL COMPLETO" — metodo
6. "ESTRATEGIA + SISTEMA" — 60+ clinicas
7. "PARE DE PERDER DINHEIRO — Comenta 'FUNIL'" — CTA

### Template 2: Polemica + autoridade
1. "[X] VAI QUEBRAR SUA CLINICA" — polemica
2. "A verdade que as agencias escondem"
3. "Por que [pratica comum] e armadilha"
4. "O que clinicas que escalam fazem diferente"
5. "O metodo Flux em 3 passos"
6. "+60 clinicas, R$1M gerenciados"
7. "Vamos jogar o jogo grande? — Comenta 'ESTRATEGISTA'"

### Template 3: Personal brand
1. "O CEREBRO POR TRAS DA SUA ESCALA" (D)
2. "IA NAO E MAGICA, E METODO" (D)
3-5. educacional luxo (B)
6. "+60 CLINICAS ACELERADAS" (B)
7. "VAMOS JOGAR O JOGO GRANDE?" (D)

## Regras-Chave (NUNCA quebrar)

1. **TEXTO NA IMAGEM E OBRIGATORIO** — esta skill existe justamente porque ads-generate proibe texto. Aqui texto E o produto.
2. **Sempre PT-BR** com acentuacao correta. Validar visualmente.
3. **Paleta restrita** a `flux-clinicas.json`. Sem cor pastel, sem branco como fundo dominante.
4. **Numeracao de slide** sempre top-right.
5. **Headline ocupa 50-65%** da imagem (regra de ouro Flux).
6. **CTA do slide final** sempre formato: "Comenta '[PALAVRA]' e eu te mostro [beneficio]".
7. **Brand rules Flux:** NUNCA mencionar GHL/GoHighLevel — usar "Sistema Flux 360".

## Reference Files

- `~/.banana/presets/flux-clinicas.json` — preset com paleta + 4 sub-estilos
- `~/.claude/projects/c--Users-windows--claude/docs/creative/flux-brand/flux-brand-profile.json` — brand DNA completo
- `J:/Meu Drive/.../SOMOS FLUX/#09 - Conteudo/ABRIL/images/` — pasta de refs visuais (25 imagens)
