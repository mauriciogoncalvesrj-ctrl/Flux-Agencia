# Fal.ai — Text Rendering Limitations

**Status: Confirmed in production (2026-05-13, Seedream 4.5)**

## The Problem

ALL text-to-image models on Fal.ai (Seedream, Flux, Nano Banana, etc.) are **unreliable for rendering text**. When you include text in a prompt (headlines, logos, CTAs, labels), the model may:

- Render garbled/illegible characters
- Omit the text entirely
- Produce hallucinated text (wrong words, mixed languages)
- Render text in the wrong position or scale

This is a **fundamental limitation of diffusion-based image generation**, not specific to any model.

## Session Evidence

**2026-05-13 — Seedream 4.5:** Generated carrossel cover for Flux Agência. Prompt included explicit text placement ("large white bold modern text 'Sua clínica está pronta para 2026?'... robot emoji"). Result: high-quality visual with correct composition, palette, and style — but **zero text rendered**. Vision analysis confirmed: "Não há nenhum tipo de texto, logo, marca d'água ou tipografia visível."

## Correct Workflow

```
❌ WRONG: Include text in the image generation prompt
✅ RIGHT: Generate visual-only background → apply text in post-production
```

### Option A: Image + Text Overlay (Fal.ai compose_images)

1. Generate background image via `mcp_fal_ai_generate_image` (no text in prompt)
2. Create a separate text-only image (generated or programmatic) with transparent background
3. Use `mcp_fal_ai_compose_images` to overlay text onto background

### Option B: Programmatic Assembly (social-media-carousels skill)

1. Generate background image(s) via Fal.ai
2. Use `social-media-carousels` skill with slideshow lib to compose final slides
3. Add text, logos, overlays programmatically with precise positioning

### Option C: Post-Processing Tools

- Canva API
- Sharp/Pillow (server-side image composition)
- Figma API

## When Text DOES Work

The exception: **GPT Image 2** (via `image_generate` built-in tool) sometimes renders text correctly because it uses a different architecture (autoregressive + diffusion hybrid). However, it often times out (120s+) via MCP. For text-heavy creatives, prefer the built-in `image_generate` tool over Fal.ai MCP.

## Models Tested

| Model | Text Rendering | Notes |
|-------|---------------|-------|
| Seedream 4.5 | ❌ Failed | Beautiful visuals, zero text |
| Flux 2 Pro | ⚠️ Unreliable | Occasional garbled words |
| Nano Banana 2 | ❌ Failed | Ignores text instructions |
| GPT Image 2 | ⚠️ Partial | Works sometimes, but times out often |

## Takeaway for Creative Agent / Orchestrator

When the Creative Agent produces a visual brief with text placement, the Orchestrator must:
1. Strip text from the Fal.ai generation prompt
2. Generate the visual background only
3. Apply text overlay via compose_images or programmatic assembly
4. NEVER expect the model to render headlines, CTAs, or logos
