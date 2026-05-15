# Bug reasoning_details (opencode-go) — kimi-k2.6 e mimo-v2.5

**Data de descoberta:** 2026-05-15  
**Data de mitigação:** 2026-05-15  
**Status:** Mitigado via roteamento de perfis  
**Severidade:** P1 — quebra pipelines multi-turn e delegação

## Sintoma

Erro HTTP 400 ao fazer chamadas sequenciais (multi-turn) ou `delegate_task` com `kimi-k2.6` via `opencode-go`:

```text
Extra inputs are not permitted, field: messages[N].reasoning_details
```

O provider `opencode-go` rejeita o campo `reasoning_details` quando ele é repassado como input na chamada seguinte. O modelo retorna esse campo na resposta, e o Hermes pode incluí-lo na mensagem seguinte, causando rejeição.

## Modelos afetados / suspeitos

- `kimi-k2.6`: confirmado com erro `reasoning_details` em multi-turn.
- `mimo-v2.5`: confirmado padrão semelhante com `reasoning_details` / `content:null`.

## Impacto

1. `delegate_task` falha em pipelines multi-turn.
2. Sessões de orquestração podem travar na segunda chamada.
3. Fluxo criativo de 5 portões fica inseguro com esses modelos.
4. Chat direto via Telegram/CLI também pode ser afetado em conversas longas.

## Workaround aplicado

### 1. Perfil `flux-orchestrator` usa `deepseek-v4-pro`

Arquivo: `/opt/data/profiles/flux-orchestrator/config.yaml`

```yaml
model:
  default: deepseek-v4-pro
  provider: opencode-go
```

**Por que funciona:** `deepseek-v4-pro` não apresentou o bug de `reasoning_details` nos testes desta migração.

### 2. `kimi-k2.6` e `mimo-v2.5` ficam fallback-only

Uso permitido apenas quando:

- for chamada única/single-turn;
- não houver `delegate_task`;
- não houver continuação multi-turn;
- o usuário aceitar risco de fallback.

### 3. Rotas seguras

| Cenário | Modelo recomendado |
|---|---|
| Orquestração | `deepseek-v4-pro` |
| Volume/relatório | `deepseek-v4-flash` |
| DevOps/código premium | `gpt-5.5` via `openai-codex` |
| Visão | `qwen3.5-plus` / `qwen3.6-plus` |

## Reversão

Só promover `kimi-k2.6` ou `mimo-v2.5` novamente se o provider parar de retornar `reasoning_details` em respostas multi-turn ou se o Hermes sanitizar esse campo antes da próxima chamada.

## Regressão

Antes de qualquer promoção, testar:

1. Primeira chamada simples.
2. Segunda chamada usando o histórico anterior.
3. `delegate_task` com pelo menos duas etapas.
4. Verificar ausência de `messages[N].reasoning_details` no erro.
