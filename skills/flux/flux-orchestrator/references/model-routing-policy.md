# Flux Model Routing Policy — Ollama Cloud + OpenCode

Última validação: 2026-05-14

## Objetivo

Direcionar modelos por função dentro da Agência Flux usando, por enquanto, **somente modelos disponíveis em Ollama Cloud e OpenCode**.

Esta política existe para evitar que o orquestrador escolha automaticamente modelos reservados, especialmente `gpt-5.5`, quando Mauricio quer testar e comparar os modelos disponíveis em Ollama Cloud/OpenCode.

## Regra de allowlist/bloqueio

### Permitidos para seleção automática

- **Ollama Cloud** via endpoint OpenAI-compatible `https://ollama.com/v1`
- **OpenCode Go/Zen** via provider configurado no Hermes, quando disponível

### Reservados / não usar automaticamente

Não selecionar automaticamente, salvo quando Mauricio pedir explicitamente:

- `gpt-5.5`
- `gpt-5.5-pro`
- modelos GPT/OpenAI fora da allowlist
- Claude, Gemini, Anthropic, OpenRouter e outros providers externos fora de Ollama Cloud/OpenCode

## Limitação técnica atual do Hermes

`delegate_task` **não tem roteamento nativo por tarefa/modelo**.

Comportamento atual:

1. Se `delegation.model/provider/base_url` estiver vazio, o subagente herda o modelo do orquestrador.
2. Se `delegation.model/provider/base_url` estiver preenchido, **todos** os subagentes usam esse modelo global.
3. Não existe parâmetro nativo em `delegate_task` para `model=` ou `provider=` por task.

Portanto:

- Use `delegate_task(tasks=[...])` apenas para lotes que possam rodar no mesmo modelo.
- Para tarefas que exigem modelos diferentes, separar em etapas ou usar perfis/processos Hermes específicos por função.
- O orquestrador deve reportar no final se os subagentes herdaram o modelo ou se houve override global via `delegation.*`.

## Smoke tests realizados

### Ollama Cloud `/v1/models`

Endpoint respondeu `200` e listou 39 modelos. Modelos relevantes confirmados na lista:

- `glm-5.1`
- `kimi-k2.6`
- `minimax-m2.7`
- `deepseek-v4-pro`
- `deepseek-v4-flash`
- `qwen3.5:397b`
- `qwen3-vl:235b`
- `qwen3-vl:235b-instruct`
- `qwen3-next:80b`
- `qwen3-coder-next`
- `devstral-small-2:24b`
- `devstral-2:123b`
- `gemma4:31b`
- `nemotron-3-super`
- `nemotron-3-nano:30b`
- `mistral-large-3:675b`
- `ministral-3:3b`, `ministral-3:8b`, `ministral-3:14b`

Smoke test `chat/completions` retornou `200` para:

- `glm-5.1`
- `kimi-k2.6`
- `minimax-m2.7`
- `deepseek-v4-flash`
- `qwen3-next:80b`
- `qwen3-coder-next`
- `qwen3-vl:235b`

### OpenCode Go

- `/v1/models` retornou Cloudflare `403 / 1010` via chamada direta Python, mas `chat/completions` funcionou.
- Smoke test `chat/completions` retornou `200` para:
  - `glm-5.1`
  - `kimi-k2.6`
  - `minimax-m2.7`
  - `qwen3.6-plus`
- `qwen3.5-plus` retornou `429` por quota do provider Alibaba.
- `deepseek-v4-flash-free` e `nemotron-3-super-free` retornaram `Model not supported` no OpenCode Go testado.

## Matriz de roteamento recomendada

### Orquestração / planejamento estratégico

**Principal:** `kimi-k2.6`

- Provider preferido: Ollama Cloud ou OpenCode, conforme estabilidade/custo.
- Uso: decompor tarefas, coordenar especialistas, tarefas longas, workflows agentic.

**Fallbacks:**

1. `glm-5.1` — raciocínio técnico/agentic forte.
2. `deepseek-v4-pro` — raciocínio pesado e contexto longo via Ollama Cloud.
3. `deepseek-v4-flash` — coordenação rápida/mais econômica.

### DevOps / código / debugging / refatoração

**Principal:** `glm-5.1` via OpenCode Go.

Uso:

- debugging Hermes
- refatoração de skills/config
- scripts
- análise de logs
- arquitetura técnica

**Fallbacks:**

1. `qwen3-coder-next` via Ollama Cloud — worker de código rápido.
2. `devstral-small-2:24b` via Ollama Cloud — navegação/edição de codebase.
3. `minimax-m2.7` — tarefas de código moderadas e automação.

### Pesquisa / web / documentação / benchmark

**Principal:** `deepseek-v4-flash` via Ollama Cloud.

Uso:

- pesquisa profunda com múltiplas fontes
- sumarização longa
- comparação de ferramentas/modelos
- briefing técnico

**Fallbacks:**

1. `qwen3.5:397b` — generalista forte.
2. `kimi-k2.6` — pesquisa com planejamento agentic.
3. `qwen3-next:80b` — síntese rápida/intermediária.

### Criativo / copy / social / ideação

**Principal:** `gemma4:31b` via Ollama Cloud.

Uso:

- copy PT-BR
- ideação de criativos
- variações de ângulos
- narrativa de campanha

**Fallbacks:**

1. `qwen3.5:397b` — generalista forte para PT-BR e estruturação.
2. `minimax-m2.7` — variações rápidas e tarefas moderadas.
3. `kimi-k2.6` — quando criatividade precisa virar plano de ação agentic.

### Meta Ads / análise de métricas / funil

**Principal:** `deepseek-v4-pro` via Ollama Cloud.

Uso:

- diagnóstico de performance
- cruzamento de campanhas, criativos e funil
- análise estratégica de métricas

**Fallbacks:**

1. `glm-5.1` — raciocínio técnico e auditorias estruturadas.
2. `qwen3.6-plus` via OpenCode Go — análise geral validada em smoke test.
3. `qwen3.5:397b` — síntese e classificação.

Observação: cálculos devem ser feitos com ferramenta determinística (`terminal`/Python), não mentalmente pelo LLM.

### Vision / OCR / layout / screenshots

**Principal pesado:** `qwen3-vl:235b` via Ollama Cloud.

Uso:

- OCR
- análise de layout
- screenshots de ferramentas
- QA visual de criativos e landing pages

**Padrão atual validado:** `qwen3.5:cloud` em `auxiliary.vision`.

**Fallbacks:**

1. `qwen3-vl:235b-instruct`
2. `gemma4:31b`
3. `kimi-k2.6`

### Compressão / título / triagem / tarefas simples

**Principal:** `qwen3-next:80b` via Ollama Cloud.

Uso:

- compressão de contexto
- resumos intermediários
- geração de títulos
- triagem leve

**Fallbacks:**

1. `minimax-m2.7`
2. `ministral-3:14b` ou `ministral-3:8b`
3. `nemotron-3-nano:30b`

## Regras operacionais para o orquestrador

1. Antes de delegar, classificar o tipo de tarefa.
2. Se a tarefa precisar de modelos diferentes, **não misturar tudo em um único batch `delegate_task`**.
3. Agrupar em batch apenas subtarefas que podem usar o mesmo modelo.
4. Não usar `gpt-5.5` nem providers fora de Ollama Cloud/OpenCode automaticamente.
5. Se Mauricio pedir explicitamente outro modelo, obedecer e reportar o override.
6. Sempre reportar no final:
   - modelo do orquestrador
   - modelo esperado dos subagentes
   - se houve herança ou override via `delegation.*`
   - qual slot auxiliar foi usado quando aplicável, por exemplo `auxiliary.vision`

## Configuração recomendada por enquanto

Enquanto não houver perfis/processos separados por função, manter:

```yaml
delegation:
  model: ''
  provider: ''
  base_url: ''
  api_key: ''
```

Motivo: evita forçar todos os subagentes para um único modelo errado.

Para roteamento real por função, criar perfis Hermes separados, por exemplo:

- `flux-orchestrator` → `kimi-k2.6`
- `flux-devops` → `glm-5.1`
- `flux-research` → `deepseek-v4-flash`
- `flux-creative` → `gemma4:31b`
- `flux-vision` → `qwen3-vl:235b` ou `qwen3.5:cloud`

Cada perfil deve deixar `delegation.*` vazio para que seus subagentes herdem o modelo daquele perfil.

## Próximo passo recomendado

1. Criar perfis Hermes por função, sem expor segredos.
2. Configurar cada perfil com um modelo allowlisted.
3. Testar cada perfil com uma tarefa mínima.
4. Só depois ativar uso operacional em produção.
