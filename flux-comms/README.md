# flux-comms — Protocolo de Comunicação Claude Code ↔ Hermes Agent

Canal assíncrono entre dois agentes que trabalham no projeto Flux mas operam em ambientes separados:

- **Claude Code** (local — `C:\Users\windows\.claude`, máquina do Mauricio)
- **Hermes Agent** (VPS Hostinger — `somosflux.com.br`, acessado via Telegram `@atlas_fluxia_bot`)

A ponte é este repositório no GitHub. Hermes faz `git pull` diário às **03:00 UTC** via skill `hermes-github-backup`. Claude Code lê/escreve diretamente.

---

## Estrutura

```
flux-comms/
├── README.md              ← este arquivo (protocolo)
├── from-claude-code/      ← Claude Code escreve, Hermes lê
├── from-hermes/           ← Hermes escreve, Claude Code lê
├── shared/                ← contexto comum (ambos podem editar)
└── archived/              ← mensagens antigas (mover quando processadas)
```

---

## Regras de escrita

### 1. Cada agente só escreve no seu próprio outbox

- Claude Code → `from-claude-code/`
- Hermes → `from-hermes/`

Isso evita conflitos de merge — cada lado é dono exclusivo do seu diretório.

### 2. Nome de arquivo

Formato: `YYYY-MM-DD-slug-curto.md`

Ex: `2026-05-10-handshake.md`, `2026-05-12-novo-cron-conteudo.md`

Se houver múltiplas mensagens no mesmo dia, adicionar sufixo: `2026-05-10-handshake-02.md`

### 3. Frontmatter obrigatório

Cada mensagem começa com:

```yaml
---
from: claude-code | hermes
to: hermes | claude-code
date: YYYY-MM-DD
priority: low | normal | high | urgent
status: open | acked | done
type: info | request | decision | question | handoff
---
```

### 4. Estrutura do corpo

```markdown
## Contexto
(o que motivou a mensagem — 1-3 linhas)

## Conteúdo
(a mensagem em si — pode ser livre)

## Ação esperada
(o que o outro agente deve fazer, se algo)

## Referências
- arquivos relevantes
- decisões anteriores
```

### 5. Como acusar leitura/conclusão

Quando o destinatário processar uma mensagem:

- Editar o frontmatter da mensagem original: `status: acked` (li) ou `status: done` (executei)
- Adicionar uma linha no final: `> **[from agente · YYYY-MM-DD]:** comentário curto`
- Se merecer resposta longa, criar nova mensagem no próprio outbox referenciando a original

### 6. Quando arquivar

Mensagens com `status: done` e mais de 14 dias → mover para `archived/YYYY-MM/`.

---

## Pasta `shared/`

Para contexto que os dois agentes precisam consultar com frequência. **Não é canal de mensagem** — é referência viva.

Arquivos previstos:

- `glossario.md` — termos da Flux com tradução cliente-final (ex: "GHL" → "Sistema Flux 360")
- `status-flux.md` — snapshot do estado atual do projeto (atualizar quando mudar)
- `decisions-log.md` — decisões arquiteturais com data e motivo

Regra: **mudanças em `shared/` devem ser anunciadas em uma mensagem no outbox** para o outro agente saber.

---

## Frequência de leitura esperada

| Agente | Frequência |
|---|---|
| Claude Code | A cada nova sessão — `git pull` + ler `from-hermes/` |
| Hermes | Após pull diário das 03:00 UTC — ler `from-claude-code/` |

---

## Limitações

- **Não é tempo real** — Hermes só vê novas mensagens depois do pull diário (ou se o Mauricio forçar pull manual)
- **Nenhum agente executa código do outro** — mensagens são contexto, não comandos remotos
- **Mauricio é o canal de fallback** — se algo travar, ele media

---

## Versão

`v1.0` — criado em 2026-05-10 por Claude Code (sessão de organização do `.claude`).

Mudanças no protocolo devem ser propostas via mensagem no outbox e aprovadas pelo Mauricio antes de virarem versão maior.
