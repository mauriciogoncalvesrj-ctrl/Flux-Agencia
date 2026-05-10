---
name: Arquitetura 7 agentes Flux
description: Estrutura multi-agente Flux — CEO Hermes + 6 Diretores especializados, cada um com modelo Ollama Cloud alocado
type: project
originSessionId: fa9626c9-cbb4-4f66-a229-79d66fc3b380
---
Arquitetura aprovada e construída em `J:\Meu Drive\00 - Flux Growth System\agents\`:

| ID | Agente | Modelo |
|---|---|---|
| 0 | CEO Hermes (orquestrador) | kimi-k2.6-cloud |
| 1 | Diretor Sistema GHL | glm-5.1-cloud |
| 2 | Diretor Tráfego | glm-5.1-cloud |
| 3 | Diretor Inteligência de Mercado | deepseek-v4-pro-cloud |
| 4 | Diretor Conteúdo & Funil | kimi-k2.6-cloud |
| 5 | Diretor Comercial | minimax-m2.7-cloud |
| 6 | Diretor Relatórios | deepseek-v4-pro-cloud |

**Why:** Maurício quer reduzir carga cognitiva de operar 5+ ferramentas para "conversar com 1 sistema". Cada Diretor cobre um setor da agência (CRM/bots, mídia paga, espionagem, criação, vendas B2B, performance). CEO Hermes é o único ponto de entrada e devolve resposta consolidada.

**How to apply:** Antes de propor mudança na arquitetura, ler os AGENTS.md atuais. Quando o Maurício pedir nova capacidade, primeiro perguntar se cabe num Diretor existente antes de criar agente novo. Sequência de implementação faseada: Fase 1 (CEO + Sistema GHL + Tráfego), Fase 2 (Inteligência + Conteúdo), Fase 3 (Comercial + Relatórios).

Fallback local de todos: gemma4:e2b na VPS Hostinger.
