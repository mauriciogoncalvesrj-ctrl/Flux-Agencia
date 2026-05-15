# Flux Model Routing Policy — GPT + OpenCode Go

Última validação: **2026-05-15**

## Objetivo

Direcionar modelos por função dentro da Agência Flux usando a nova arquitetura sem Ollama Cloud: **GPT/OpenAI Codex + OpenCode Go**.

A política substitui a allowlist antiga de Ollama Cloud e define quando usar DeepSeek V4 Pro/Flash, GPT e modelos de visão Qwen.

## Regra de allowlist/bloqueio

### Permitidos para seleção automática

- **OpenCode Go/Zen** (`opencode-go`) via `https://opencode.ai/zen/go/v1`
- **OpenAI Codex** (`openai-codex`) para camada premium/código

### Não usar automaticamente

- `ollama-cloud` e endpoint `https://ollama.com/v1`
- modelos legados: `qwen3-vl:235b`, `qwen3.5:cloud`, `gemma4:31b`, `ministral-3:8b`, `qwen3-coder-next`, `glm-5.1` como default de perfil
- Claude, Gemini, OpenRouter e outros providers externos, salvo pedido explícito do Mauricio

## Política de gasto

- **80% OpenCode Go**: DeepSeek Pro/Flash + Qwen vision.
- **15% GPT/OpenAI Codex**: devops, código, revisão premium e tarefas críticas.
- **5% premium GPT**: emergências, auditoria final e casos de alto valor.

## Limitação técnica atual do Hermes

`delegate_task` **não tem roteamento nativo por tarefa/modelo**.

Comportamento atual:

1. Se `delegation.model/provider/base_url` estiver vazio, o subagente herda o modelo do perfil/orquestrador.
2. Se `delegation.model/provider/base_url` estiver preenchido, **todos** os subagentes usam esse modelo global.
3. Não existe parâmetro nativo em `delegate_task` para `model=` ou `provider=` por task.

Portanto:

- Use `delegate_task(tasks=[...])` apenas para lotes que possam rodar no mesmo modelo.
- Para tarefas que exigem modelos diferentes, separar em etapas ou usar perfis/processos Hermes específicos por função.
- O orquestrador deve reportar no final se os subagentes herdaram o modelo ou se houve override global via `delegation.*`.

## Matriz de perfis ativos

| Perfil | Modelo primário | Provider | Fallbacks | Função |
|---|---|---|---|---|
| `flux-orchestrator` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `qwen3.5-plus` → `kimi-k2.6` | Planejamento, decomposição, coordenação, síntese |
| `flux-devops` | `gpt-5.5` | `openai-codex` | `deepseek-v4-pro` → `deepseek-v4-flash` → `kimi-k2.6` | Código, Hermes, infra, debugging |
| `flux-research` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` | Pesquisa, benchmarks, documentação |
| `flux-creative` | `deepseek-v4-pro` | `opencode-go` | `deepseek-v4-flash` → `gpt-5.5` | Copy, ideação, narrativa, engenharia de prompt |
| `flux-meta-ads` | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` → `gpt-5.5` | Métricas, funil, diagnóstico de campanhas |
| `flux-vision` | `qwen3.5-plus` | `opencode-go` | `qwen3.6-plus` → `gpt-5.5` | OCR, screenshots, QA visual, análise de referências |
| `flux-compress` | `deepseek-v4-flash` | `opencode-go` | `deepseek-v4-pro` | Compressão, triagem, títulos, resumos rápidos |

## Matriz de roteamento por domínio

### Orquestração / planejamento estratégico

- **Principal:** `deepseek-v4-pro` via `opencode-go`
- **Uso:** decompor tarefas, coordenar especialistas, tarefas longas, síntese cross-domínio
- **Fallbacks:** `deepseek-v4-flash` → `qwen3.5-plus` → `kimi-k2.6` fallback-only

### DevOps / código / debugging / refatoração

- **Principal:** `gpt-5.5` via `openai-codex`
- **Uso:** configuração Hermes, debugging, scripts, refatoração de skills/config, análise de logs
- **Fallbacks:** `deepseek-v4-pro` → `deepseek-v4-flash` → `kimi-k2.6` fallback-only

### Pesquisa / web / documentação / benchmark

- **Principal:** `deepseek-v4-pro` via `opencode-go`
- **Uso:** pesquisa profunda, comparação de ferramentas/modelos, briefing técnico, documentação
- **Fallbacks:** `deepseek-v4-flash` → `gpt-5.5`

### Criativo / copy / social / ideação

- **Principal:** `deepseek-v4-pro` via `opencode-go`
- **Uso:** copy PT-BR, ideação de criativos, variações de ângulo, narrativa de campanha, prompt engineering
- **Fallbacks:** `deepseek-v4-flash` → `gpt-5.5`

### Meta Ads / análise de métricas / funil

- **Principal:** `deepseek-v4-flash` via `opencode-go`
- **Uso:** relatórios de volume, diagnóstico inicial, análise de performance e funil
- **Escalar para:** `deepseek-v4-pro` quando exigir diagnóstico estratégico pesado
- **Fallback:** `gpt-5.5`
- **Observação:** cálculos devem ser feitos com ferramenta determinística (`terminal`/Python), não mentalmente pelo LLM.

### Vision / OCR / layout / screenshots

- **Principal:** `qwen3.5-plus` via `opencode-go`
- **Fallbacks:** `qwen3.6-plus` → `gpt-5.5`
- **Uso:** OCR, análise de layout, screenshots, QA visual de criativos e landing pages
- **Não usar:** `minimax-m2.5` para visão — teste retornou HTTP 400 / não suporta imagem.

### Compressão / título / triagem / tarefas simples

- **Principal:** `deepseek-v4-flash` via `opencode-go`
- **Fallback:** `deepseek-v4-pro`
- **Uso:** compressão de contexto, resumos intermediários, títulos, triagem leve

## Quirks operacionais

1. **Cloudflare OpenCode Go:** chamadas diretas via Python podem retornar `403 / 1010`; usar `curl` com `User-Agent: Hermes-Agent/1.0`.
2. **`kimi-k2.6`:** fallback-only por bug `reasoning_details` em multi-turn/delegação.
3. **`mimo-v2.5`:** fallback-only; confirmou padrão semelhante de `reasoning_details`/`content:null`.
4. **`minimax-m2.5`:** não é modelo de visão no OpenCode Go.
5. **Segredos:** manter `${OPENCODE_GO_API_KEY}` e nunca commitar valores reais.

## Configuração recomendada

Manter `delegation.*` vazio nos perfis:

```yaml
delegation:
  model: ''
  provider: ''
  base_url: ''
  api_key: ''
```

Motivo: evita forçar todos os subagentes para um único modelo errado.

## Smoke test obrigatório depois de mudanças

1. Validar YAML de todos os `config.yaml`.
2. Testar uma chamada mínima por perfil.
3. Confirmar o cabeçalho/modelo esperado.
4. Buscar referências legadas a `ollama-cloud` em configs ativos.
