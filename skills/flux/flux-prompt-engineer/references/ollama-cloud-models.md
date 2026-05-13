# Ollama Cloud — Modelos Disponíveis (Maio 2026)

Base URL: `https://ollama.com/v1/` (NOT `api.ollama.com` — that returns 301 redirect)

Auth: Bearer token via `OLLAMA_API_KEY` env var.

## Modelos Prímarios (Agência Flux)

| Modelo | Provider Config | Melhor Para |
|--------|----------------|-------------|
| glm-5.1 | opencode-go | Engenharia de prompt, visão, criatividade |
| deepseek-v4-pro | opencode-go | Raciocínio, análise, fallback |
| kimi-k2.6 | opencode-go | Rapidez, tarefas simples |
| qwen3-vl:235b | opencode-go | Visão computacional (análise de referências) |

## Modelos Complementares

| Modelo | Notas |
|--------|-------|
| deepseek-v3.1:671b | Grande, raciocínio pesado |
| deepseek-v4-flash | Versão rápida do v4 |
| devstral-2:123b | Código/programação |
| gemma3:27b | Small tasks, rápido |
| gemma4:31b | Equilibrado |
| glm-4.7, glm-4.6, glm-5 | Versões anteriores |
| kimi-k2:1t | Trillion params, thinking |
| kimi-k2-thinking | Raciocínio explícito |
| minimax-m2, m2.1, m2.5, m2.7 | Família alternativa |
| nemotron-3-super | NVIDIA |
| qwen3-coder:480b | Código pesado |
| qwen3-coder-next | Última versão |
| qwen3.5:397b | Mid-tier |

## Quirk: API Redirect

`curl https://api.ollama.com/v1/models` → 301 → `https://ollama.com/v1/models`
Use `ollama.com` directly to avoid double-hop. Hermes config already handles this correctly.