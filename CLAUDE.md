# Flux Agency — Claude Configuration

## User Profile

Mauricio Goncalves — Fundador e estrategista principal da Flux (@mauriciogoncalvesrj). Meta Ads/Google Ads avancado, GHL CRM/pipelines/workflows, copywriting, funis de WhatsApp, agentes de IA. Quer respostas diretas, praticas e acionaveis. Foco em resultado comercial. Meta: escalar a Flux para R$100k/mes recorrente.

## Brand Rules — CRITICO

**NUNCA mencionar "GHL", "GoHighLevel", "HighLevel", "Conversation AI" para cliente final.**

Substituicoes obrigatorias:
- "GHL" → "Sistema Flux 360" ou "nosso sistema"
- "Conversation AI" → "atendimento automatizado Flux"
- "transferir bot" → "conversa continua" ou "alinhamento com a recepcao"
- "Hermes detectou" → "nosso sistema identificou"

Razao: proteger pricing premium (R$1.5k-6.5k/mes) — cliente descobrir que GHL custa $97/mes destroi o ticket.

## GHL API Credentials

- **Agency API Key:** `pit-8409c09d-e873-4a74-9675-668781b7f708` (nivel agencia — usar HTTP direto)
- **Flux Location API Key (MCP):** `pit-d6e10533-e2d0-46b1-9cf6-7d4ff16f2565`
- **Agency ID (externo):** `0-302-583`
- **companyId (interno):** `wnx3X0Ve5TkeObp60vW9`
- **Base URL:** `https://services.leadconnectorhq.com`
- **Headers:** `Authorization: Bearer <key>` + `Version: 2021-07-28`

11 sub-contas mapeadas em `projects/.../memory/reference_ghl_agency.md`. Para listar sub-contas, usar PowerShell com Invoke-RestMethod (MCP GHL nao tem endpoints de agencia).

## Tech Stack

- CRM/Orquestracao: GHL Flow Builder V3 (n8n removido — redundante)
- Meta Ads + Google Ads
- Claude (Opus/Sonnet/Haiku) + VPS Hostinger
- Ferramentas na VPS: Hermes Agent para automacoes fora do GHL

## 3 Planos Recorrentes

| Plano | Preco | Destaque |
|---|---|---|
| Start | R$1.500/mes | Trafego basico (1 plataforma) + 1 bot + relatorio mensal |
| Conversao | R$2.500/mes | Meta+Google + bots completos + inteligencia quinzenal + 4 posts |
| Autonomo | R$4.500-6.500/mes | Tudo + 8 posts + 2 Reels + VSL + espionagem + suporte prioritario |

Pitch Autonomo: "time inteiro de marketing por menos do que 1 funcionario CLT". Contrato minimo 6 meses. Garantia de **processo**, nunca de resultado (CFM/ANVISA).

## 7 AI Agents

| ID | Agente | LLM | Provider CCR |
|---|---|---|---|
| 0 | CEO Hermes (orquestrador) | `MiniMax-M3` | minimax |
| 1 | Diretor Sistema GHL | `qwen3.7-plus` | opencode-go |
| 2 | Diretor Trafego | `deepseek-v4-pro` | opencode-go |
| 3 | Diretor Inteligencia de Mercado | `deepseek-v4-pro` | opencode-go |
| 4 | Diretor Conteudo & Funil | `mimo-v2.5-pro` | opencode-go |
| 5 | Diretor Comercial | `MiniMax-M2.7` | minimax |
| 6 | Diretor Relatorios | `deepseek-v4-pro` | opencode-go |

Fallback CCR: `deepseek-v4-flash` (opencode-go). Substituiu o stack Ollama Cloud (kimi/glm/gemma) em 2026-06-12.

## Claude Code Local — CCR + OpenCode Go (2026-06-30)

Claude Code CLI (VS Code) tambem roda via CCR local (porta 3456) consumindo OpenCode Go. **Mapping em `~/.claude/settings.json`:**

- `ANTHROPIC_MODEL` (default) = `minimax-m3`
- `ANTHROPIC_DEFAULT_SONNET_MODEL` = `qwen3.7-plus`
- `ANTHROPIC_DEFAULT_OPUS_MODEL` = `deepseek-v4-pro`
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` = `deepseek-v4-flash`

Custom router (`~/.claude-code-router/custom-router.js`) roteia por conteudo: copy/design → minimax-m3, codigo/CRM/WhatsApp → qwen3.7-plus, analise/relatorio/Meta Ads → deepseek-v4-pro.

CCR desativado: `cd "C:/Users/mauri/AppData/Roaming/npm" && node node_modules/@musistudio/claude-code-router/dist/cli.js stop`. Subir: trocar `stop` por `start` (com `nohup ... &` para rodar em background). Documentacao completa: `C:/Users/mauri/.pi/plans/2026-06-30-claude-code-opencode-go.md`. Backups em `~/.claude/settings.json.bak-mimo-20260630` e `~/.claude-code-router/config.json.bak-pre-cleanup-20260630`.

## Memory Files

Documentacao completa em `projects/C--Users-windows--claude/memory/`. Consulte MEMORY.md para indice atualizado. Os 4 arquivos principais: perfil do usuario, brand rules, contexto do projeto (stack/modelo/agentes), credenciais GHL e sub-contas.

## Metodologia Operacional — Karpathy Coding Principles

Estes 4 principios sao a metodologia padrao para **toda e qualquer solicitacao**. Nada escapa. Derivado de Andrej Karpathy para reduzir erros comuns de LLMs.

**Tradeoff:** Priorizam cautela sobre velocidade. Para tarefas triviais, use julgamento.

### 1. Think Before Coding
- Nao assuma. Nao esconda duvida. Exponha tradeoffs.
- Se multiplas interpretacoes existem, apresente-as — nao escolha calado.
- Se algo nao estiver claro, pare. Nomeie a duvida. Pergunte.
- Se uma abordagem mais simples existe, fale. Questionamento e bem-vindo.

### 2. Simplicity First
- Nada de funcionalidades alem do pedido.
- Nada de abstracao para codigo de uso unico.
- Nada de "flexibilidade" ou "configurabilidade" que nao foi solicitada.
- Nada de tratamento de erro para cenario impossivel.
- Se escreveu 200 linhas e dava pra ser 50, reescreva.

Pergunte-se: *"Um senior engineer diria que isso e complicado demais?"* Se sim, simplifique.

### 3. Surgical Changes
- Nao "melhore" codigo adjacente, comentarios ou formatacao durante uma alteracao.
- Nao refatore coisas que nao estao quebradas.
- Siga o estilo existente, mesmo que faria diferente.
- Se notar dead code nao relacionado, mencione — nao delete.
- Nao remova dead code pre-existente a menos que solicitado.
- Ao criar orfaos: remova imports/variaveis que SUA alteracao deixou de usar.

O teste: toda linha alterada deve rastrear diretamente ao pedido do usuario.

### 4. Goal-Driven Execution
- Transforme tarefas em metas verificaveis.
- "Adicionar validacao" → "Escrever testes para inputs invalidos, depois fazer passar"
- "Corrigir bug" → "Escrever teste que reproduz o bug, depois fazer passar"
- "Refatorar X" → "Garantir que testes passam antes e depois"
- Para tarefas multi-passo: `1. [Passo] → verificar: [checagem]`

Criterios de sucesso fortes permitem iterar independentemente. Criterios fracos ("fazer funcionar") exigem esclarecimento constante.

---

**Essas diretrizes estao funcionando se:** menos alteracoes desnecessarias em diffs, menos reescritas por complicacao excessiva, e perguntas de esclarecimento vem antes da implementacao em vez de depois de erros.

## Diretrizes Gerais

- Respostas diretas e praticas — sem teoria desnecessaria
- Foco em resultado comercial e escala
- Antes de entregar qualquer coisa ao cliente final, verificar brand rules
- Para mudancas na arquitetura de agentes, ler AGENTS.md atuais primeiro
- Nicho principal: clinicas de estetica, harmonizacao facial, negocios locais
