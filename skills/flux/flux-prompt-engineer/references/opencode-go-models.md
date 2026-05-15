# OpenCode Go — Modelos Operacionais Flux (Maio 2026)

Base URL: `https://opencode.ai/zen/go/v1/`

Auth: Bearer token via `OPENCODE_GO_API_KEY` env var. Nunca commitar token real.

## Modelos primários da Agência Flux

| Modelo | Provider Config | Melhor para | Status |
|---|---|---|---|
| `deepseek-v4-pro` | `opencode-go` | Orquestração, análise estratégica, criatividade estruturada, pesquisa | Primário |
| `deepseek-v4-flash` | `opencode-go` | Volume, rapidez, relatórios, triagem, compressão | Primário |
| `qwen3.5-plus` | `opencode-go` | Visão, OCR, análise de referências, screenshots | Primário vision |
| `qwen3.6-plus` | `opencode-go` | Fallback de visão | Fallback |
| `gpt-5.5` | `openai-codex` | Código, DevOps, revisão premium, tarefas críticas | Premium |

## Modelos fallback-only

| Modelo | Motivo |
|---|---|
| `kimi-k2.6` | Bug `reasoning_details` em multi-turn/delegação; usar só single-turn emergencial |
| `mimo-v2.5` | Padrão semelhante de `reasoning_details` / `content:null`; não usar em pipelines |

## Modelos reprovados para visão

| Modelo | Resultado |
|---|---|
| `minimax-m2.5` | Não suporta imagem via OpenCode Go; retornou HTTP 400 |

## Quirk: Cloudflare 403 / 1010

Chamadas diretas via Python `urllib`/`requests` para OpenCode Go podem ser bloqueadas por Cloudflare.

Use `curl` com User-Agent:

```bash
curl -sS https://opencode.ai/zen/go/v1/chat/completions   -H "Authorization: Bearer $OPENCODE_GO_API_KEY"   -H "Content-Type: application/json"   -H "User-Agent: Hermes-Agent/1.0"   -d '{"model":"deepseek-v4-flash","messages":[{"role":"user","content":"Diga OK"}]}'
```

## Prompt engineering criativo

Para prompts de imagem e criativos da Flux:

1. Use `deepseek-v4-pro` para análise, estrutura e prompt final.
2. Use `deepseek-v4-flash` para variações rápidas.
3. Use `qwen3.5-plus` para interpretar referências visuais antes do prompt.
4. Escale para `gpt-5.5` somente quando for uma peça premium ou correção crítica.
