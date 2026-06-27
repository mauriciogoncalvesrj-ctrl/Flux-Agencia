---
name: content-engine-pipeline
description: "Content Engine pipeline unificado — copy via mimo API + imagens Fal.ai + overlay Pillow, totalmente funcional"
metadata: 
  node_type: memory
  type: project
  originSessionId: a49deb1e-6df2-49d5-abdb-3960d30d0e0d
---

# Content Engine Pipeline — Funcional

## Status: ✅ OPERACIONAL (2026-06-27)

## O que foi feito
1. **Copy generation** migrada de Ollama Cloud (quebrado) para API mimo (Anthropic format)
2. **Fontes** Montserrat Black + Bold + Inter baixadas em `assets/fonts/`
3. **Overlay** Pillow melhorado (texto maior, vinheta mais forte, subtítulo legível)
4. **Prompts de fundo** variados por tipo de slide (cover, problem, solution, CTA)
5. **Parser de resposta** mimo API corrigido (trata thinking blocks)

## Pipeline: `C:\Users\mauri\flux\engines\content-engine\`

### Comando
```bash
cd C:\Users\mauri\flux\engines\content-engine
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe briefing.py --cliente grupo_flux --tema "seu tema" --formato carrossel --aspect 4:5
```

### Fluxo
```
Briefing → Copy (mimo-v2.5 via API) → Backgrounds (Fal.ai Schnell) → Overlay (Pillow) → PNGs finais
```

### Custo por carrossel
- 6 imagens Schnell: ~R$0.018
- Copy via mimo: gratuito (mesma API do Claude Code)

### Arquivos modificados
- `.env` — MIMO_API_URL, MIMO_API_KEY, MIMO_MODEL
- `config.yaml` — copy.provider: mimo
- `scripts/gerar_copy.py` — formato Anthropic (x-api-key + /v1/messages)
- `scripts/compor_texto.py` — fontes maiores, overlay forte
- `briefing.py` — prompts variados por slide
- `assets/fonts/` — Montserrat-Black.ttf, Montserrat-Bold.ttf, Inter.ttf

### Output de teste
`C:\Users\mauri\flux\engines\content-engine\output\20260627_113112_grupo_flux_5_erros_que_clinicas_cometem_n\`
- 6 backgrounds (bg_slide_*.png)
- 6 finais com texto (slide_*_final.png)
- copy.json

## Clientes disponíveis (config.yaml)
- grupo_flux, proton, humberto, borgatte, rachel_lisboa, alpha_transformadores

## Próximos passos
- Frente 2: Calendário editorial (3 posts/semana)
- Frente 3: Social posting via GHL MCP (agendamento automático)
- Melhorar prompts por território visual (5 territórios do DESIGN.md)
