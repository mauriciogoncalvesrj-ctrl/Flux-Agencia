# 🎨 Programmatic Instagram Carousel SVG Generation

> Técnica usada na Agência Flux para gerar carrosséis do Instagram como SVGs escaláveis, a partir de referências visuais enviadas pelo usuário.

## Ambiente

- Container Hermes Agent (sem PIL, sem wkhtmltoimage)
- Saída: SVG puro (texto) + HTML preview opcional
- Resolução alvo: 1080×1350px (proporção 4:5 do Instagram)

## Design System Padrão (Somos Flux)

| Elemento | Valor |
|----------|-------|
| Fundo | #000000 gradiente para #0a0a0a |
| Destaque | #D4AF37 (dourado) |
| Texto principal | #FFFFFF (branco) |
| Subtítulo | #888888 (cinza) |
| Alerta | #DC5046 (vermelho) |
| Fonte título | Arial Black / Montserrat Black, 48px, uppercase |
| Fonte body | Arial, 20px |
| Badge | borda dourada, texto dourado, raio 16px |
| CTA box | fundo #111, borda dourada, raio 14px |
| Linha base | gradiente dourado horizontal |
| Número slide | topo direito, #333, 20px |

## Fluxo de Trabalho

### 1. Coletar e analisar referências

```python
import base64, requests, os

# Ler API key do Ollama Cloud
with open('/opt/data/.env', 'r') as f:
    for line in f:
        if 'API_KEY' in line and '=' in line:
            api_key = line.split('=', 1)[1].strip().strip('"').strip("'")

# Codificar imagens
with open(path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
image_url = f"data:image/jpeg;base64,{b64}"

# Chamar vision model
payload = {
    "model": "qwen3-vl:235b",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Descreva o ESTILO VISUAL: cores, tipografia, layout, elementos."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    }],
    "max_tokens": 1000
}
response = requests.post("https://ollama.com/v1/chat/completions",
                         headers={"Authorization": f"Bearer {api_key}"},
                         json=payload, timeout=120)
```

### 2. Gerar SVGs em lote

```python
def create_slide(title, subtitle="", body="", slide_num=0, total=1,
                 highlight_words=[], icon="", badge="", cta="", footer=""):
    W, H = 1080, 1350
    GOLD, WHITE, GRAY = "#D4AF37", "#FFFFFF", "#888888"

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append(f'<rect width="{W}" height="{H}" fill="#000"/>')

    # Quebra de linha automática
    words = title.upper().split()
    lines, cur = [], ""
    for w in words:
        test = cur + " " + w if cur else w
        if len(test) <= 22:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    y = 170
    for line in lines:
        color = GOLD if any(hw.upper() in line for hw in highlight_words) else WHITE
        svg.append(f'<text x="{W//2}" y="{y}" font-size="48" font-weight="900" text-anchor="middle" fill="{color}">{line}</text>')
        y += 64

    # ... (subtitle, body, cta, footer, progress bar)
    svg.append('</svg>')
    return '\n'.join(svg)
```

### 3. Empacotar para entrega

```bash
cd /opt/data && tar -czf carrosseis.tar.gz carrosseis/
```

### 4. Preview HTML (opcional)

Criar `preview.html` com CSS que replica o SVG visualmente, para o usuário visualizar no browser antes de converter para PNG.

## Conversão para PNG

Como o container não tem ferramentas de rasterização, orientar o usuário:
- **Opção 1**: Abrir SVG no Chrome → F12 → Capture full size screenshot
- **Opção 2**: Extensão GoFullPage (Chrome)
- **Opção 3**: Importar SVG no Canva (suporta nativo)
- **Opção 4**: cloudconvert.com (SVG → PNG)

## Templates de Estrutura Narrativa

### Storytelling (10 slides)
1. Capa impactante (dor)
2-4. Aprofundar a dor (estatísticas, problemas)
5. Virada ("Até que eu...")
6-7. Solução
8. Resultado (números)
9. Autoridade/posicionamento
10. CTA

### Pipeline Educativo (10 slides)
1. Hook provocativo
2-9. Estágios numerados
10. CTA

### Checklist/Framework (7-9 slides)
1. Capa com título do checklist
2-N. Itens do checklist
N+1. CTA
