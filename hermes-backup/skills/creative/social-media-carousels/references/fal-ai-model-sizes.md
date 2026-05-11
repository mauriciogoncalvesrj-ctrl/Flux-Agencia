# Fal.ai Model Size Validations

Each Fal.ai model accepts DIFFERENT `image_size` values. Using the wrong one causes immediate failure. This reference documents known-valid sizes per model.

## Flux Models (`fal-ai/flux-*`)

| Model | Valid `image_size` values |
|-------|--------------------------|
| `fal-ai/flux-2-pro` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |
| `fal-ai/flux/schnell` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |
| `fal-ai/flux/dev` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |
| `fal-ai/flux-pro/v1.1` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |
| `fal-ai/flux-pro/v1.1-ultra` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |

## GPT Image 2 (`openai/gpt-image-2`)

| Model | Valid `image_size` values |
|-------|--------------------------|
| `openai/gpt-image-2` | `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`, `auto` |

## Nano Banana Models (`fal-ai/nano-banana*`)

| Model | Valid `image_size` values |
|-------|--------------------------|
| `fal-ai/nano-banana-2` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |
| `fal-ai/nano-banana-pro` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |

## Grok (`xai/grok-imagine-image`)

| Model | Valid `image_size` values |
|-------|--------------------------|
| `xai/grok-imagine-image` | `square`, `landscape_4_3`, `landscape_16_9`, `portrait_3_4`, `portrait_9_16` |

## Key Pattern

**Most Fal.ai native models** (Flux, Nano Banana, Grok) use this set:
```
square, landscape_4_3, landscape_16_9, portrait_3_4, portrait_9_16
```

**OpenAI models** (GPT Image 2) use a DIFFERENT set:
```
square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9, auto
```

## Instagram Carousel Format

| Instagram format | Ratio | Closest `image_size` |
|-----------------|-------|---------------------|
| Feed carousel | 1:1 (1080x1080) | `square` |
| Feed portrait | 4:5 (1080x1350) | `portrait_3_4` or `portrait_4_3` |
| Stories/Reels | 9:16 (1080x1920) | `portrait_9_16` or `portrait_16_9` |

## Pitfall: MCP Layer Validation

The MCP tool wrapper sometimes applies its own validation that differs from the API's. If you get an error like:
```
'portrait_4_3' is not one of ['square', 'landscape_4_3', ...]
```
But the API docs say `portrait_4_3` IS valid — try `square` as a universal fallback, or use the `image_generate` tool which handles size mapping internally.

## Timeouts

- **GPT Image 2**: Often times out at 120s. Avoid for time-sensitive tasks. Use `image_generate` built-in tool instead.
- **Flux models**: Usually complete in 2-10s.
- **Nano Banana models**: Usually complete in 1-5s.
