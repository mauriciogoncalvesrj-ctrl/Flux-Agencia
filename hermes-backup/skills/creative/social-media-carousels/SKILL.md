---
name: social-media-carousels
description: Create Instagram/TikTok/LinkedIn carousel slides programmatically as SVG, from visual references or text briefs. Includes style extraction, batch generation, and packaging.
trigger: When the user asks for Instagram carousels, social media slides, visual content, carousel design, or sends reference images for carousel creation.
---

# 📸 Social Media Carousel Creation

Generate professional carousel slides for Instagram, TikTok, LinkedIn, and other platforms using programmatic SVG generation.

## When to Use

- User asks for "carrossel", "carousel", "slides", "posts visuais"
- User sends batches of reference images without verbal explanation
- User wants Instagram/TikTok/LinkedIn content with consistent visual style
- User needs 5–10+ slides with uniform design

## Workflow

### 🚀 Method 1: Complete Slide via Fal.ai (RECOMMENDED)

**When the user wants a finished carousel slide with image AND text together**, use the built-in `image_generate` tool. It produces PNG directly — Telegram will display it natively. No SVG conversion needed.

```python
# Generates a complete slide with integrated text typography
image_generate(
    prompt="Instagram carousel slide for [brand]. The image must include BOTH a photograph AND text typography as one complete designed ad creative. Layout: [describe image area] + [describe text area with fonts, colors, positioning].",
    aspect_ratio="portrait"  # Instagram 4:5
)
```

**Key prompt ingredients for complete slides:**
- Explicitly say "include BOTH a photograph AND text typography as one complete designed ad creative"
- Describe the layout zones (upper/lower or left/right)
- Specify the exact text: headline, subheadline, tagline, brand name
- Mention colors for text (gold, white, etc.)
- Request "magazine-quality" or "luxury brand" style

**This is the PREFERRED method.** The user wants finished ad creatives, not bare images.

### 🛠️ Method 2: SVG Composite (Fallback)

When Fal.ai generation is insufficient or you need pixel-perfect typography control, use the SVG approach:

When the user sends reference images, **do not ask for verbal descriptions**. Analyze them immediately:

```python
import base64, requests

# Read API key from /opt/data/.env
with open('/opt/data/.env', 'r') as f:
    for line in f:
        if 'API_KEY' in line and '=' in line:
            api_key = line.split('=', 1)[1].strip().strip('"').strip("'")

# Encode up to 3 images per call
with open(path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')
image_url = f"data:image/jpeg;base64,{b64}"

headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {
    "model": "qwen3-vl:235b",
    "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Extract style: colors hex, typography, layout, icons, mood."},
        {"type": "image_url", "image_url": {"url": image_url}}
    ]}],
    "max_tokens": 1000
}
response = requests.post("https://ollama.com/v1/chat/completions", headers=headers, json=payload, timeout=120)
```

Extract systematically:
- **Colors**: background, accent, text, alert (get hex codes)
- **Typography**: font style, size hierarchy, uppercase/lowercase
- **Layout**: text position (center/left), image placement, spacing
- **Elements**: badges, progress bars, icons, decorative shapes
- **Narrative structure**: how many slides, what content on each

### 2. Design System

Default palette (adjust based on references):

| Element | Default | Notes |
|---------|---------|-------|
| Background | #000000 → #0a0a0a gradient | Dark, premium feel |
| Accent | #D4AF37 | Gold highlights |
| Text primary | #FFFFFF | White, bold |
| Text secondary | #888888 | Gray subtitles |
| Alert | #DC5046 | Red for warnings |
| Success | #50C878 | Green for positive |
| Resolution | 1080×1350 | Instagram 4:5 ratio |
| Font title | Arial Black, 48px, uppercase | Ultra-bold impact |
| Font body | Arial, 20px | Readable |
| Badge | Border + text in accent color | Rounded corners |
| CTA box | #111 background, accent border | Rounded 14px |
| Progress | Bottom gradient line | Shows slide position |
| Slide number | Top-right, #333, 20px | Discreet |

### 3. Generate SVGs

Use pure SVG (no PIL needed). Key helper: text wrapping.

```python
def wrap_text(text, max_chars=22):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = cur + " " + w if cur else w
        if len(test) <= max_chars:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def create_slide(title, subtitle="", body="", slide_num=0, total=1,
                 highlight_words=[], icon="", badge="", cta="", footer=""):
    W, H = 1080, 1350
    GOLD, WHITE, GRAY = "#D4AF37", "#FFFFFF", "#888888"
    
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    svg.append(f'<rect width="{W}" height="{H}" fill="#000"/>')
    
    # Slide number
    if slide_num > 0:
        svg.append(f'<text x="{W-50}" y="50" font-size="20" text-anchor="end" fill="#333">{slide_num}/{total}</text>')
    
    # Badge
    if badge:
        bw = len(badge) * 14 + 30
        svg.append(f'<rect x="50" y="35" width="{bw}" height="32" rx="16" fill="none" stroke="{GOLD}" stroke-width="1.5"/>')
        svg.append(f'<text x="{50+bw//2}" y="58" font-size="14" font-weight="bold" text-anchor="middle" fill="{GOLD}">{badge}</text>')
    
    y = 170
    
    # Icon
    if icon:
        svg.append(f'<text x="{W//2}" y="{y+70}" font-size="85" text-anchor="middle">{icon}</text>')
        y += 110
    
    # Title (with auto-highlight)
    for line in wrap_text(title.upper(), 22):
        color = GOLD if any(hw.upper() in line for hw in highlight_words) else WHITE
        svg.append(f'<text x="{W//2}" y="{y}" font-size="48" font-weight="900" text-anchor="middle" fill="{color}">{line}</text>')
        y += 64
    
    # ... (subtitle, body, numbers, CTA, footer)
    
    svg.append(f'<rect x="50" y="{H-25}" width="{W-100}" height="3" rx="2" fill="{GOLD}"/>')
    svg.append('</svg>')
    return '\n'.join(svg)
```

### 4. Structure Templates

#### Storytelling (8–10 slides)
```
1. Capa: dor impactante ("Eu gastava R$X e...")
2-4. Aprofundar dor (estatísticas, problemas)
5. Virada ("Até que eu...")
6-7. Solução
8. Resultado (números grandes)
9. Autoridade
10. CTA ("Comenta X")
```

#### Pipeline Educativo (8–10 slides)
```
1. Hook provocativo ("Seu WhatsApp é um cemitério?")
2-N. Estágios numerados com badges
N+1. CTA
```

#### Checklist/Framework (6–9 slides)
```
1. Capa com título do framework
2-N. Itens numerados com bullets
N+1. CTA
```

### 5. Package & Deliver

```bash
cd /opt/data && tar -czf carrosseis.tar.gz carrosseis/
```

Also create optional `preview.html` for browser visualization before rasterization.

### 6. Conversion to PNG

The container lacks rasterization tools. Instruct the user:
- **Chrome**: Open SVG → F12 → Ctrl+Shift+P → "Capture full size screenshot"
- **GoFullPage**: Chrome extension for batch capture
- **Canva**: Import SVG directly (supports native SVG)
- **CloudConvert**: cloudconvert.com (SVG → PNG)

## Pitfalls

- **Do NOT ask for verbal feedback** if user keeps sending images — they communicate visually
- **Do NOT deliver bare images with no text** when the user asked for a carousel — they want complete ad creatives with typography integrated
- **SVG files sent via Telegram appear as documents, not rendered images** — prefer `image_generate` for PNG delivery
- **Do NOT use PIL** — not installed in Hermes container; use pure SVG
- **Do NOT use wkhtmltoimage/chromium** — not available in container
- **Do NOT send >3–4 images per vision call** — will timeout
- **Always set max_tokens** for vision calls (1000–2000)
- **Use `/v1/chat/completions`** not `/api/chat` for Ollama Cloud vision
- **Wrap long titles** — Instagram carousels need readable line breaks
- **Test SVG validity** — open in Chrome before delivering
- **Fal.ai models have DIFFERENT valid `image_size` values** — see `references/fal-ai-model-sizes.md`. Using wrong size = wasted attempts.
- **GPT Image 2 times out often** (120s+) via Fal.ai MCP — use `image_generate` tool as primary path

## References

- `templates/carousel-svg-template.py` — Complete Python template for batch generation
- `references/instagram-design-system.md` — Extended design system with color variations
- `references/fal-ai-model-sizes.md` — Valid image_size values per model (avoid wrong-size errors)
