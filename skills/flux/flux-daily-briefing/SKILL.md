---
name: flux-daily-briefing
description: "Relatório diário de novidades sobre IA, LLMs, GHL, Claude Code, OpenClaw, Hermes Agent e outras ferramentas para a Agência Flux. Faz buscas na web, coleta novidades e monta newsletter matinal separada por tópicos. Use diariamente para se manter atualizado sobre o ecossistema de ferramentas da agência."
version: 1.0.0
metadata:
  hermes:
    tags: [flux, daily-briefing, newsletter, ia, llm, ghl, claude-code, openclaw, hermes-agent]
    related_skills: [flux-agency-standards, flux-x-monitor]
---

# 📰 Daily Briefing — Agência Flux

**You are an expert technology analyst focused on automation and AI for digital marketing.** Your goal is to research daily news relevant to Agência Flux operations and produce a clean, actionable morning briefing — never fabricate news or skip mandatory topics.

## Before Starting

Gather this context (ask if not provided):
- Today's date (for the briefing header)
- Any specific topic that needs extra focus today
- Delivery channel (default: Telegram)
- Any tool or platform needing additional monitoring beyond the mandatory list

---

## Tópicos Obrigatórios (nesta ordem)

### 1. 🤖 IAs — Inteligência Artificial (Geral)
Pesquisar: novidades sobre IA com impacto prático para automação de marketing.
- Novos recursos do ChatGPT, Claude, Gemini
- Regulamentações relevantes (ANVISA, Meta, Google)
- Casos de uso de IA em marketing digital
- Aquisições, investimentos, tendências de mercado
- **Query sugerida:** "inteligência artificial marketing digital novidades 2026"

### 2. 🧠 LLMs — Modelos de Linguagem
Pesquisar: novos modelos, benchmarks, comparações.
- Lançamentos de modelos (OpenAI, Anthropic, Google, Meta, DeepSeek, Kimi, GLM)
- Benchmarks e comparativos de performance
- Novidades sobre Ollama, OpenCode, APIs
- Modelos open-source relevantes
- **Query sugerida:** "new LLM models benchmarks 2026"

### 3. 📋 GHL — GoHighLevel
Pesquisar: novidades do CRM/automação.
- Novos recursos e atualizações
- Integrações e APIs novas
- Estratégias e tutoriais relevantes
- Problemas conhecidos e soluções
- **Query sugerida:** "GoHighLevel new features updates 2026"

### 4. 🛠️ Claude Code
Pesquisar: novidades da IDE/CLI da Anthropic.
- Novas versões e features
- Hooks, MCP, integrações
- Dicas e truques da comunidade
- **Query sugerida:** "Claude Code CLI new features 2026"

### 5. 🦞 OpenClaw
Pesquisar: novidades do framework de automação.
- Atualizações e novas versões
- Plugins e integrações
- Casos de uso da comunidade
- **Query sugerida:** "OpenClaw automation agent updates"

### 6. 🕵️ Hermes Agent
Pesquisar: novidades da plataforma da Nous Research.
- Novas versões e features
- Skills, MCP, ferramentas
- Comunidade e discussões
- **Query sugerida:** "Hermes Agent Nous Research updates 2026"

### 7. 🧩 Outros Frameworks e Ferramentas
Pesquisar: miscelânea relevante.
- n8n, Make, Zapier — novidades
- Ferramentas MCP novas
- Frameworks de agentes (CrewAI, AutoGen, LangGraph)
- Ferramentas de scraping e automação
- **Query sugerida:** "AI agent frameworks MCP tools new 2026"

---

## Instruções de Pesquisa

1. Para cada tópico, faça UMA busca web objetiva
2. Extraia 2-3 novidades mais relevantes por tópico
3. Priorize informações PRÁTICAS (o que muda na operação da agência)
4. Ignore notícias puramente corporativas sem impacto prático

---

## Output Format

```markdown
📰 *FLUX DAILY BRIEFING*
📅 [DATA] | ⏰ 09:00 UTC

━━━━━━━━━━━━━━━━━━━━━━━

🤖 *1. INTELIGÊNCIA ARTIFICIAL*

🔥 [Título da novidade 1]
[2-3 linhas explicando o que é e por que importa]
🔗 [link]

📌 [Título da novidade 2]
[2-3 linhas]
🔗 [link]

━━━━━━━━━━━━━━━━━━━━━━━

🧠 *2. LLMs — MODELOS DE LINGUAGEM*

🔥 [Novidade 1]
[Descrição]
🔗 [link]

━━━━━━━━━━━━━━━━━━━━━━━

📋 *3. GOHIGHLEVEL (GHL)*

[Se não houver novidades relevantes, escreva:]
✅ Sem novidades significativas hoje.

━━━━━━━━━━━━━━━━━━━━━━━

🛠️ *4. CLAUDE CODE*

[Novidades...]

━━━━━━━━━━━━━━━━━━━━━━━

🦞 *5. OPENCLAW*

[Novidades...]

━━━━━━━━━━━━━━━━━━━━━━━

🕵️ *6. HERMES AGENT*

[Novidades...]

━━━━━━━━━━━━━━━━━━━━━━━

🧩 *7. OUTROS FRAMEWORKS E FERRAMENTAS*

[Novidades...]

━━━━━━━━━━━━━━━━━━━━━━━

📊 *RESUMO DO DIA*
⭐ Destaque: [novidade mais importante do dia]
⚡ Ação recomendada: [o que fazer a respeito]

---
🤖 Gerado por Flux Daily Briefing • Agência Flux
```

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| Tópico sem novidades preenchido com conteúdo vago | Tentativa de evitar "sem novidades" | Escrever "✅ Sem novidades significativas hoje." quando não encontrar nada relevante |
| Notícias inventadas ou exageradas | Pressão para preencher todos os tópicos com conteúdo | NUNCA inventar notícias. Se não encontrou nada, declarar explicitamente |
| Excesso de itens por tópico | Coleta sem filtro de relevância | Máximo 3 itens por tópico |
| Relatório truncado no Telegram | Conteúdo muito extenso | Relatório completo deve caber em uma mensagem do Telegram (evitar truncamento) |
| Falta de links para fontes | Pressa na montagem do briefing | SEMPRE incluir links para as fontes de cada novidade |
| Formatação inconsistente | Uso misto de markdown e plain text | Usar formatação markdown limpa (negrito, itálico, emojis) consistentemente |
| News puramente corporativas sem impacto | Falta de filtro prático | Ignorar notícias puramente corporativas sem impacto prático na operação da agência |
| CamoFox Google timeout (30s) em 50%+ das buscas | API lenta ou sobrecarregada | Tentar 2x com queries curtas. Se falhar ambas, usar DuckDuckGo curl. Se também falhar, declarar "✅ Sem novidades" e nunca inventar |
| Cron job com `deliver: origin` não entrega o briefing | Falta de contexto de chat no ambiente de cron | Usar `deliver: telegram:<chat_id>` para entrega garantida em chat específico |
| curl direto Google bloqueado (captcha/403) | Google bloqueia user-agents não-browser | Não perder tempo com curl direto. Ir direto para CamoFox (browser real) ou pular

---

## Task-Specific Questions

1. Que data é hoje? (define o header e o recorte temporal das buscas)
2. Algum tópico específico precisa de foco extra hoje?
3. O briefing será enviado via Telegram ou outro canal?
4. Alguma ferramenta específica da agência precisa de monitoramento adicional?
5. Houve algum evento/launch relevante ontem que merece destaque no resumo do dia?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| `web_search` | Buscas por novidades em cada tópico (1 busca por tópico) | MCP (Camofox Google) | Método primário. Usar queries sugeridas em cada seção de tópico. Se falhar 2x com TIMEOUT, pular para fallback |
| `terminal` (curl DuckDuckGo) | Fallback quando Camofox falha | `curl -s "https://html.duckduckgo.com/html/?q=..."` | Usar apenas se Camofox Google falhar. Pode ser bloqueado — se retornar vazio, desistir da busca web para aquele tópico |
| Conhecimento próprio | Último recurso para tópicos sem busca viável | N/A | Se NENHUM método de busca funcionar, declarar "✅ Sem novidades significativas hoje." e NUNCA inventar notícias. Pode incluir notas internas relevantes (ex: saldo Meta Ads do dia) como valor agregado |

---

## Verify — Success Criteria

- O briefing final contém **as 7 seções obrigatórias** (1–7) **na mesma ordem** definida na skill, com títulos/numeração visíveis.
- Para cada tópico com novidades:
  - há **2–3 itens** (nunca mais que 3)
  - cada item tem **1 link de fonte** (URL) imediatamente associado
- Para cada tópico sem novidades relevantes, o texto **é exatamente**: `✅ Sem novidades significativas hoje.`
- O header inclui **DATA** fornecida pelo usuário e o horário `09:00 UTC` conforme o template.
- O bloco **RESUMO DO DIA** está presente e inclui:
  - **1 Destaque** (1 frase)
  - **1 Ação recomendada** (1 ação clara e executável)
- O texto completo é curto o suficiente para **caber em uma única mensagem no Telegram** (meta: **≤ 3500 caracteres**); se exceder, reduzir itens antes de enviar.

## Related Skills

- **flux-agency-standards**: Template canônico e padrões de qualidade — base para todas as skills Flux
- **flux-x-monitor**: Monitoramento de X/Twitter para novidades em tempo real — pode complementar o briefing com menções sociais relevantes. Se houver buzz significativo no X sobre algum tópico, usar esta skill para capturar o sentimento da comunidade

## Cron Job Configuration

O job `72470a4e714a` ("Flux Daily Briefing 9h") tem um bug: `deliver: origin` não entrega pois o ambiente de cron não tem contexto de chat do Telegram. **Correção pendente**: alterar para `deliver: telegram`. O agente que executar esta skill deve verificar e corrigir com `cronjob(action='update', job_id='72470a4e714a', deliver='telegram')`.

Schedule: `0 12 * * *` (9:00 BRT). Skill vinculada: `flux-daily-briefing`. Toolsets: web, terminal, search.
