---
name: daily-priorities
title: Resumo Diário de Tarefas e Prioridades
description: |
  Gera um briefing matinal estruturado com resumo de tarefas, prioridades
  e foco do dia para o executivo da Agência Flux. Integra contexto de
  projetos ativos (conteúdo, tráfego, CRM, operações) e entrega formato
  acionável para começar o dia com clareza.
author: Agência Flux
tags: [productivity, planning, daily-briefing, priorities, execution]
---

# Resumo Diário de Tarefas e Prioridades

## 1. Propósito

Ser o ritual de abertura do dia: antes de abrir WhatsApp ou inbox,
o usuário recebe um panorama claro do que precisa ser feito, na ordem
que realmente importa — não na ordem que as tarefas chegaram.

## 2. Gatilhos de Uso

- `"meu resumo do dia"` / `"o que eu tenho hoje?"` — gera briefing matinal
- `"prioridades"` / `"o que é urgente?"` — foco apenas no que precisa decidir/agir hoje
- `"resumo da semana"` — panorama dos próximos 5-7 dias
- `"atualiza meu quadro"` — sincroniza estado com fontes externas (kanban, calendário)

## 3. Coleta de Contexto

Antes de gerar o resumo, coletar dados das fontes disponíveis:

### Fontes Primárias (sempre que possível)
- **Kanban do Hermes** (`kanban` tool): cards ativos, em progresso, review
- **Lista de TODO da sessão** (`todo` tool): itens pendentes do dia/session
- **Skills ativas da Agência Flux**: estado de cron jobs, pipelines pendentes
- **Calendário / compromissos**: reuniões, entregas com deadline

### Fontes Secundárias (quando integrado)
- Notas do Obsidian (se houver daily notes)
- E-mails marcados como follow-up
- Mensagens pendentes do Telegram/Discord

### Contexto do Negócio (Agência Flux)
- **Dia de pipeline?** Segunda-feira = conteúdo (9h UTC) + anúncios (9h30 UTC)
- **Meta principal do mês**: tráfego, captação, entrega de cliente?
- **Projetos ativos**: clínicas atendidas, campanhas no ar

## 4. Framework de Priorização

Usar a matriz de priorização híbrida da Flux:

| Pillar | Pergunta | Se sim, sobe na fila |
|---|---|---|
| **Gera Receita** | Isso traz cliente/pagamento em até 7 dias? | 🔴 Topo |
| **Libera Bloqueio** | Alguém está parado esperando isso? | 🔴 Topo |
| **Compromisso Externo** | Tem hora marcada com cliente/fornecedor hoje? | 🟡 Prioridade 2 |
| **Preparação** | Prepara algo que gera receita/semana que vem? | 🟡 Prioridade 2 |
| **Melhoria** | Otimiza processo existente sem urgência? | 🟢 Faz se sobrar tempo |
| **Exploração** | Ideia nova sem caminho claro? | 🔵 Backlog / delega |

> Regra: máximo 3 tarefas no topo 🔴. O resto organiza em 🟡 e 🟢.

## 5. Formato de Entrega

### A) Briefing Matinal Padrão

```
☀️ Resumo de [Dia da semana], [DD/MM]
──────────────────────────

🎯 FOCO DO DIA (1 coisa que se feita, o dia valeu):
[...]

🔴 TOPO DA FILA (3 máx):
1. [...] — [por que está aqui: gera receita / libera bloqueio / compromisso]
2. [...]
3. [...]

🟡 PRIORIDADE 2:
- [...]
- [...]

🟢 SE SOBRAR TEMPO:
- [...]

⏰ COMPROMISSOS COM HORA:
[HH:MM] — [...]
[HH:MM] — [...]

⚠️ BLOQUEIOS / ESPERANDO:
- [...] (esperando por: [...])

💡 Lembrete de pipeline:
[Hoje é dia de X? Alertar e sugerir próximo passo]
──────────────────────────
Total de tarefas ativas: [N]
```

### B) Modo "Apenas o que importa" (urgente/curto)

Se o usuário estiver com pouco tempo ou estiver estressado:
```
⚡ FOCO HOJE:
1. [só a #1 da lista]
2. [só se houver compromisso externo inadiável]

Única pergunta que importa: "Isso gera receita ou libera alguém?"
```

### C) Resumo da Semana

```
📅 Semana de [DD/MM] a [DD/MM]

🔴 Dias críticos:
- Seg: pipeline de conteúdo + anúncios
- Qua: [...]

🎯 Entregas com data fechada:
- [DD/MM] — [...]

📦 Projetos em andamento:
- [...]: [...%] — próximo passo: [...]
```

## 6. Regras de Conduta

| ✅ Fazer | ❌ Evitar |
|---|---|
| Dizer explicitamente *por que* uma tarefa está no topo | Listar 15 tarefas como "prioridade" |
| Limitar a 3 itens no 🔴 topo — força escolha | Mostrar tudo de tudo sem filtro |
| Lembrar dos compromissos com hora antes de sugerir blocos de foco | Sugerir 4h de deep work se tem reunião às 10h |
| Identificar bloqueios onde o usuário está esperando alguém | Esconder dependências externas |
| Se não houver dados, perguntar: "Quais são seus 3 focos hoje?" | Inventar tarefas se não tiver contexto |

## 7. Interação com o Ecosistema Flux

### Kanban
Se houver cards ativos no kanban, mapear:
- `in_progress` → 🔴 Topo (se bloqueia alguém) ou 🟡
- `review` → verificar se precisa de ação do usuário
- `todo` → avaliar se entra na fila de hoje

### Cron Jobs / Skills da Agência
- Segunda: alertar que pipeline de conteúdo vai rodar 9h UTC
- Segunda: alertar que pipeline de anúncios vai rodar 9h30 UTC
- Verificar se skills de inteligência/competidor têm dados novos

### Sessions Passadas
- Usar `session_search` para verificar se há tarefas pendentes de sessões anteriores
- Se o usuário disse "vou fazer depois" — isso é uma tarefa ativa

## 8. Exemplo de Interação

**Usuário:** `"meu resumo do dia"`

**Agente:**
```
☀️ Resumo de Segunda-feira, 05/05
──────────────────────────

🎯 FOCO DO DIA:
Finalizar o roteiro do vídeo de captação da Clínica Bella — 
vai liberar o editor para entregar até quarta.

🔴 TOPO DA FILA:
1. Revisar e aprovar roteiro Bella (libera bloqueio do editor)
2. Reunião 10h com Dr. André — definir orçamento de tráfego maio
3. Pipeline de conteúdo roda 9h UTC: verificar saída dos posts

🟡 PRIORIDADE 2:
- Aprovar arte do carrossel que ficou pendentes sexta

🟢 SE SOBRAR TEMPO:
- Ver relatório de performance da semana passada

⏰ COMPROMISSOS:
10:00 — Dr. André (tráfego maio)
15:00 — Gravação do depoimento da paciente

⚠️ ESPERANDO:
- Arte do carrossel — designer enviou drafts sexta, esperando aprovação sua
──────────────────────────
Total: 5 tarefas ativas
```

## 9. Adaptação ao Estilo do Usuário

O usuário prefere **ação > conversa** e espera **clareza > volume**.

- Nunca entregue um "dashboard" denso. O briefing é para ser lido em 30 segundos.
- Se o usuário não tiver nada na lista, sugerir UMA ação que move a meta do mês.
- Usar linguagem direta, sem corporativismo. "Reunião com Dr. André", não "1:1 de alinhamento estratégico de Q2".
- Se possível, estimar tempo: "~30 min" ao lado da tarefa.
