# Bug kimi-k2.6 (opencode-go) — reasoning_details

**Data de descoberta:** 2026-05-15
**Data de mitigação:** 2026-05-15
**Status:** Resolvido via workaround de perfil
**Severidade:** P1 — quebra pipelines multi-turn e delegação

## Sintoma

Erro HTTP 400 ao fazer chamadas sequenciais (multi-turn) ou `delegate_task` com kimi-k2.6 via opencode-go:

```
Extra inputs are not permitted, field: messages[N].reasoning_details
```

O provider opencode-go rejeita o campo `reasoning_details` quando ele é repassado como input na chamada seguinte. O kimi-k2.6 retorna esse campo na resposta, e o Hermes o inclui na mensagem seguinte, causando a rejeição.

## Impacto

1. **delegate_task falha** em pipelines multi-turn (ex: Creative Agent → Revisor → Prompt Engineer)
2. **Sessões de orquestração** travam na segunda chamada
3. **Fluxo criativo de 5 portões** impossível de executar com kimi-k2.6
4. **Multi-turn no chat direto** com Hermes via Telegram/CLI também afetado

## Workaround aplicado

### 1. Perfil flux-orchestrator → deepseek-v4-pro

Arquivo: `/opt/data/profiles/flux-orchestrator/config.yaml`

```yaml
model:
  default: deepseek-v4-pro   # era: kimi-k2.6
  provider: ollama-cloud
```

**Por que funciona:** deepseek-v4-pro não retorna `reasoning_details`, então o campo nunca chega ao input da próxima chamada.

### 2. Quando deepseek-v4-pro não é ideal

| Cenário | Problema | Solução |
|---------|----------|---------|
| Pipeline criativo (5 portões) | deepseek-v4-pro é analítico, não criativo | Usar perfil `flux-creative` com GLM-5.1 para copy/design/prompt, depois voltar a deepseek-v4-pro na síntese |
| Tarefa única de orquestração simples | deepseek-v4-pro é overkill | Funciona, custo marginal aceitável |
| Delegate_task com multi-turn no subtarefa | O sub-agente herda deepseek-v4-pro → OK | Não há problema |

### 3. Isolar kimi-k2.6 para chamadas simples

Se precisar usar kimi-k2.6 (ex: reasoning tasks complexas):
- Limitar a **uma única chamada** sem delegação
- Ou usar em `cronjob` com `no_agent: true` (executa script, não faz multi-turn)

## Reversão (se o bug for corrigido)

Se a Nous Research ou DeepSeek corrigirem o bug no provider opencode-go:

```bash
sed -i 's/deepseek-v4-pro/kimi-k2.6/g' /opt/data/profiles/flux-orchestrator/config.yaml
```

Ou editar manualmente com `nano` / `vim`.

## Regressão

Bug documentado no `reasoning_details` apareceu na versão opencode-go ~2026-05-14, possivelmente após atualização do modelo kimi-k2.6 na Ollama Cloud.

---

**Relacionado:** Veja também `flux-orchestrator/SKILL.md` na seção Common Mistakes para a regra de "NUNCA delegar vision_analyze".
