---
name: fal-ai
description: Generate images, video, and audio via Fal.ai API — 40+ models including Flux, Nano Banana, GPT Image 2, Seedance, Kling, Veo. MCP server with 18 tools. Use for marketing creatives, social media posts, ad variations, and video content.
triggers:
  - generate image
  - create image
  - generate video
  - create video
  - remove background
  - upscale image
  - edit image
  - fal.ai
  - flux image
  - nano banana
---

# Fal.ai — Image & Video Generation

## Overview

Fal.ai provides 40+ AI models for image and video generation via a single API. The MCP server (`fal-ai`) offers 18 tools accessible directly from Hermes.

## Available MCP Tools

### Image Generation
- **generate_image** — Create images from text prompts (Flux, Nano Banana, GPT Image 2, etc.)
- **generate_image_structured** — Fine-grained control over composition, lighting, subjects
- **generate_image_from_image** — Transform existing images (style transfer)

### Image Editing
- **remove_background** — Remove backgrounds (transparent PNG)
- **upscale_image** — Upscale 2x or 4x while preserving quality
- **edit_image** — Edit images using natural language instructions
- **inpaint_image** — Edit specific regions using masks
- **resize_image** — Smart resize for social media (Instagram, YouTube, TikTok)
- **compose_images** — Overlay images (watermarks, logos) with precise positioning

### Video
- **generate_video** — Text-to-video generation
- **generate_video_from_image** — Animate images into videos
- **generate_video_from_video** — Video restyling and motion transfer

### Audio
- **generate_music** — Create instrumental music or songs with vocals

### Utility
- **list_models** — Discover 600+ available models with smart filtering
- **recommend_model** — AI-powered model recommendations for your task
- **get_pricing** — Check costs before generating content
- **get_usage** — View spending history and usage stats
- **upload_file** — Upload local files for use with generation tools

## Key Models (Pricing in BRL, US$1 ≈ R$5.70)

### Text-to-Image

| Model | Cost/image | Best for |
|-------|-----------|----------|
| Flux Schnell | ~R$0,01 | Bulk A/B testing |
| Nano Banana | R$0,22 | Fast, good quality |
| Flux 2 Pro | R$0,17/MP | High quality |
| Nano Banana 2 | R$0,46 | Google SOTA |
| Nano Banana Pro | R$0,86 | Top quality |
| GPT Image 2 | Token-based | Best composition |
| Grok Imagine | R$0,13 | Good value |

### Text-to-Video

| Model | Cost/second | Best for |
|-------|------------|----------|
| Seedance 2.0 | R$1,73/seg | Best video quality |
| Kling v3 | R$0,48-0,96/seg | Professional |
| Veo 3.1 | R$0,57-2,28/seg | Google, top quality |
| Grok Imagine Video | R$0,29/seg | Good value |

## Recommended Strategy for Agência Flux

1. **Daily Instagram posts** (500/mês) → Nano Banana 2 (R$0,46/img) = R$230
2. **A/B testing** (300/mês) → Flux Schnell (R$0,01/img) = R$3
3. **Premium hero images** (100/mês) → Flux 2 Pro (R$0,85/img) = R$85
4. **Ad creatives with text** (50/mês) → Nano Banana Pro (R$0,86/img) = R$43
5. **Short Reels** (30/mês, 5s each) → Seedance 2.0 = R$260
6. **Background removal/editing** → Fal.ai tools included

**Total estimate: ~R$621/mês** (vs R$3,000-8,000 manual production)

## Configuration

- MCP server: `/opt/data/fal-mcp-venv/bin/fal-mcp`
- Config key: `mcp_servers.fal-ai` in `/opt/data/config.yaml`
- API key: `FAL_KEY` in `/opt/data/.env`
- Requires real Fal.ai API key from https://fal.ai/dashboard/keys

## Getting an API Key

1. Go to https://fal.ai — sign up
2. Navigate to Dashboard → Keys
3. Create a new key
4. Copy to `FAL_KEY` in `/opt/data/.env`
5. Restart Hermes: `hermes gateway restart`

## Pitfalls

- Without `FAL_KEY`, all tools will fail with auth error
- Video generation can take 30-60 seconds — use appropriate timeouts
- Free tier has limited credits — monitor usage with `get_usage`
- Some models (GPT Image 2) use token-based pricing — check `get_pricing` first
- Resolution multipliers: 2K = 1.5x, 4K = 2x the base price
- **CRITICAL: Each model has DIFFERENT valid `image_size` values.** Flux models use `portrait_3_4`/`portrait_9_16`; GPT Image 2 uses `portrait_4_3`/`portrait_16_9`. Using wrong size = wasted API call. See `social-media-carousels` skill → `references/fal-ai-model-sizes.md` for full table.
- **GPT Image 2 often times out** (120s+) via MCP — prefer `image_generate` built-in tool for text-on-image tasks
- **The `image_generate` tool is a reliable alternative** that handles size mapping internally and produces PNG directly — use it when MCP calls fail