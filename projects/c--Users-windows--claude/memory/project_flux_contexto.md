---
name: Contexto Flux — stack, modelo de negócio e arquitetura de agentes
description: Decisões arquiteturais e modelo de negócio da Flux — stack sem n8n, 3 planos, 7 agentes
type: project
originSessionId: 952b3788-7ce4-4a01-b468-50576d641a3c
---
## Stack Tecnológica

- **CRM/Orquestração:** GoHighLevel (GHL) com Flow Builder V3 — n8n foi removido (redundante)
- **Ferramentas centrais:** GHL, Meta Ads, Claude (Opus/Sonnet/Haiku), VPS Hostinger
- **Removidos:** n8n, Postiz, Kit/Beehiiv, Ahrefs, Microsoft Clarity
- Para automações fora do GHL: Hermes Agent + ferramentas na VPS

**Why:** GHL cobre o que o n8n faria — manter dois sistemas é complexidade desnecessária.

## Modelo de Negócio — 3 Planos Recorrentes

- **Start** — R$ 1.500/mês — tráfego básico (1 plataforma) + 1 bot + relatório mensal
- **Conversão** — R$ 2.500/mês — Meta+Google + bots completos + inteligência quinzenal + 4 posts
- **Autônomo** ⭐ — R$ 4.500-6.500/mês — tudo + 8 posts + 2 Reels + VSL + espionagem profunda + suporte prioritário

Pitch Autônomo: "time inteiro de marketing por menos do que 1 funcionário CLT". Contrato mínimo 6 meses. Garantia de **processo**, NUNCA de resultado (CFM/ANVISA).

**How to apply:** Em conversa comercial, recomendar 1 plano baseado no diagnóstico (não oferecer 3 juntos). Iniciante (< R$30k/mês) → Start. Média (R$30-80k) → Conversão. Escala (ticket > R$1.5k) → Autônomo.

## Arquitetura de Agentes (7 agentes)

Construída em `J:\Meu Drive\00 - Flux Growth System\agents\`:

| ID | Agente | Modelo |
|---|---|---|
| 0 | CEO Hermes (orquestrador) | kimi-k2.6-cloud |
| 1 | Diretor Sistema GHL | glm-5.1-cloud |
| 2 | Diretor Tráfego | glm-5.1-cloud |
| 3 | Diretor Inteligência de Mercado | deepseek-v4-pro-cloud |
| 4 | Diretor Conteúdo & Funil | kimi-k2.6-cloud |
| 5 | Diretor Comercial | minimax-m2.7-cloud |
| 6 | Diretor Relatórios | deepseek-v4-pro-cloud |

Fallback local de todos: gemma4:e2b na VPS Hostinger. Antes de propor mudança na arquitetura, ler os AGENTS.md atuais.

## Estrutura da Agência (criada em maio/2026)

Pasta: `c:\Users\windows\Projetos-Claude\teste-agencia-ia\flux-agencia\` — índice em `INDICE.md`

- `00-briefing/` — Identidade e posicionamento
- `02-setores/` — 10 setores com funções e métricas
- `03-agentes/` — Hierarquia CEO + 8 Diretores + Subagentes
- `04-playbooks/` — 6 playbooks operacionais
- `06-llms/` — Tabela de LLMs por função
- `07-implantacao/` — Plano de 4 fases (30/60/90 dias + escala)
