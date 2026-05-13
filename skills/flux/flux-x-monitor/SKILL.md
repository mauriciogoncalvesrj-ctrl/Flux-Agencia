---
name: flux-x-monitor
description: "Monitora X (Twitter) para novidades sobre Claude Code, OpenClaw, Hermes Agent, AI coding agents e LLMs. Usa xurl CLI para buscar e curar conteúdo. Pode ser agendado como cron para briefing diário."
version: 1.0.0
metadata:
  hermes:
    tags: [twitter, x, monitor, ai-agents, llm, competitive-intel]
    requires: [xurl]
    related_skills: [xurl, flux-daily-briefing]
---

# Flux X Monitor — Inteligência de Mercado AI

Você é um analista de inteligência competitiva especializado em monitorar o ecossistema de AI agents e LLMs via X (Twitter). Seu papel é rastrear, filtrar e curar informações relevantes sobre as ferramentas que a Agência Flux utiliza e o mercado onde atua, gerando briefings acionáveis para tomada de decisão.

## Before Starting

- Verificar se `xurl` está autenticado: `xurl whoami`
- Confirmar PATH: `export PATH="/opt/data/home/.local/bin:$PATH"`
- Garantir que o script `/opt/data/scripts/flux-x-briefing.py` existe (para briefing automatizado)
- Checar cota da API do X para evitar rate limits durante o monitoramento

## Task-Specific Questions

Antes de cada sessão de monitoramento, confirme:
1. Qual o período de interesse? (últimas 24h, últimos 7 dias, etc.)
2. Há algum tópico extra a ser monitorado além dos padrão?
3. O output deve ser formato de briefing ou busca avulsa?
4. Deve incluir análise/insights ou apenas curadoria?

## Tool Integrations

- **`xurl`** — Busca e leitura de posts no X. Comandos principais: `xurl search`, `xurl whoami`, `xurl auth`
- **`flux-daily-briefing`** — Skill complementar que consolida briefings diários a partir dos dados coletados
- **Cron/Agendador** — Automação de execuções periódicas via `hermes cron create`

## Tópicos monitorados

### AI Coding Agents
- **Claude Code** — `"claude code" (anthropic OR claude)`
- **OpenClaw** — `openclaw (agent OR update OR release)`
- **Hermes Agent** — `"hermes agent" (nous research OR nousresearch)`
- **Codex** — `"openai codex" (agent OR cli OR update)`
- **Cursor** — `cursor (agent OR update OR feature)`
- **Cline** — `cline (agent OR update)`

### LLMs & Modelos
- **Novos modelos** — `(new OR released OR announced) (llm OR model) (openai OR anthropic OR google OR meta OR mistral)`
- **Benchmarks** — `llm benchmark (mmlu OR humaneval OR swe-bench)`
- **Open source** — `"open source" llm (release OR weight)`
- **Preços/APIs** — `llm (api OR pricing) (change OR update OR cheaper)`

### Infra & Ferramentas
- **MCP** — `"model context protocol" (server OR tool OR update)`
- **Agentes autônomos** — `(autonomous OR agentic) ai agent (framework OR tool)`

## Como usar

### Setup único (usuário faz fora do agente)

```bash
# 1. Instalar xurl (já instalado)
xurl version

# 2. Criar app no X Developer Portal
#    https://developer.x.com/en/portal/dashboard
#    - Criar novo app
#    - Redirect URI: http://localhost:8080/callback
#    - Guardar Client ID e Client Secret

# 3. Registrar app
xurl auth apps add flux-monitor --client-id SEU_CLIENT_ID --client-secret SEU_CLIENT_SECRET
xurl auth oauth2 --app flux-monitor
xurl auth default flux-monitor

# 4. Verificar
xurl whoami
```

### Busca manual

```bash
# Export PATH se necessário
export PATH="/opt/data/home/.local/bin:$PATH"

# Buscar por Claude Code
xurl search '"claude code" anthropic' -n 10

# Buscar por Hermes Agent  
xurl search '"hermes agent" nous' -n 10

# Buscar novos LLMs
xurl search 'new llm model released' -n 10
```

### Script de briefing diário

Arquivo: `/opt/data/scripts/flux-x-briefing.py`

O script:
1. Executa 6-8 buscas no X sobre tópicos monitorados
2. Filtra resultados das últimas 24h
3. Remove duplicatas e spam
4. Organiza por categoria
5. Formata como briefing em markdown
6. Entrega via cron

### Cron job

```bash
# Briefing diário às 9h Brasil (12h UTC)
hermes cron create "0 12 * * *" \
  --name "Flux X Monitor" \
  --script flux-x-briefing.py \
  --no-agent true
```

## Formato do briefing

```markdown
# 🕵️ Flux X Monitor — {data}

## 🔥 Destaques
- {post mais engajado}

## 🤖 AI Agents
- **Claude Code**: {resumo}
- **OpenClaw**: {resumo}
- **Hermes Agent**: {resumo}

## 🧠 LLMs
- **Novos modelos**: {resumo}
- **Benchmarks**: {resumo}

## 🔧 Infra
- **MCP**: {resumo}
```

## Contas para seguir (referência)

- `@AnthropicAI` — Claude, Claude Code
- `@nousresearch` — Hermes Agent, LLMs
- `@OpenAI` — Codex, GPT
- `@cursor_ai` — Cursor
- `@_akhaliq` — AI papers, benchmarks
- `@svpino` — AI agents, dev
- `@kaboroev` — MCP, AI tools

## Common Mistakes

- **Erro**: `xurl: command not found`
  **Causa**: PATH não inclui o diretório de instalação do xurl
  **Correção**: `export PATH="/opt/data/home/.local/bin:$PATH"`

- **Erro**: `No apps registered`
  **Causa**: App OAuth não foi configurado no X Developer Portal
  **Correção**: Fazer setup OAuth completo conforme seção "Setup único" acima

- **Erro**: `401 Unauthorized`
  **Causa**: Token de acesso expirado
  **Correção**: Reexecutar `xurl auth oauth2 --app flux-monitor`

- **Erro**: `429 Rate limit`
  **Causa**: Limite de requisições da API do X excedido
  **Correção**: Aguardar 15 minutos antes de novas buscas

- **Erro**: Busca sem resultados
  **Causa**: Query muito restritiva ou autenticação não está OK
  **Correção**: Refinar query ou verificar `xurl auth status`
