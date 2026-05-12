---
name: reference-fal-models
description: Ordem preferida de modelos Fal.AI para geração de imagens com texto (carrosseis Flux) — lista de preferência do Mauricio com preços
metadata: 
  node_type: memory
  type: reference
  originSessionId: bd704387-842c-4ce4-90b2-4f2ce47dc477
---

Modelos Fal.AI para geração de imagens com texto, em ordem de preferência do Mauricio:

| Prioridade | Model ID | Custo/imagem |
|-----------|----------|-------------|
| 1 | `fal-ai/bytedance/seedream/v4.5/text-to-image` | $0.04 |
| 2 | `fal-ai/gpt-image-2` | $0.2125 |
| 3 | `fal-ai/nano-banana-2` | $0.08 |
| 4 | `fal-ai/nano-banana-pro` | $0.15 |
| 5 | `fal-ai/nano-banana` | $0.0398 |

**Modelo validado em produção:** `fal-ai/nano-banana-pro` — entrega texto PT-BR corretamente, estética editorial de luxo.

**Modelo a testar primeiro nos próximos carrosseis:** `fal-ai/bytedance/seedream/v4.5/text-to-image` ($0.04) — mais barato, ainda não testado no padrão Flux.

**Endpoint de submit:** `https://queue.fal.run/<model-id>`  
**Parâmetros nano-banana-pro:** `{ prompt, aspect_ratio: "4:5", num_images: 1 }`  
**Parâmetros seedream/gpt-image-2:** verificar docs da API (podem ter parâmetros diferentes).

**Fluxo REST (PowerShell inline — fal-generate.ps1 tem bug de encoding UTF-8 no PS5.1):**
```powershell
$env:FAL_KEY = (Get-Content ".env" | Where-Object { $_ -match "^FAL_KEY=" }).Substring(8).Trim()
$body = @{ prompt = $prompt; aspect_ratio = '4:5'; num_images = 1 } | ConvertTo-Json -Depth 5 -Compress
$headers = @{ 'Authorization' = "Key $env:FAL_KEY"; 'Content-Type' = 'application/json' }
$submit = Invoke-RestMethod -Uri "https://queue.fal.run/fal-ai/nano-banana-pro" -Method POST -Headers $headers -Body $body
# Poll $submit.status_url até status == "COMPLETED"
# Fetch $submit.response_url → $r.images[0].url → Invoke-WebRequest download
```

**FAL_KEY:** guardada em `projects/c--Users-windows--claude/docs/creative/flux-brand/.env` (gitignored).

**Regras de prompt para texto PT-BR correto:**
- Especificar texto literal entre aspas: `headline text "AGENDA CHEIA" in massive bold uppercase`
- Proibir badge de página: `DO NOT include any page number, slide indicator, badge, pill`
- Forçar paleta: `#0A0A0A deep black background, #C9A961 gold`
- Especificar fonte: `Anton/Bebas Neue style, condensed bold uppercase sans-serif`

Linkado: [[reference-flux-visual]] (brand profile + preset Flux), [[project-flux-contexto]] (stack)
