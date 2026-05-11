---
name: hermes-github-backup
description: "Backup automático diário da configuração do Hermes Agent para o GitHub."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [backup, github, devops, cron]
    related_skills: [github-auth]
---

# Hermes Agent GitHub Backup

Faz backup automático da configuração completa do Hermes Agent para um repositório GitHub, excluindo segredos e arquivos sensíveis.

## O que é backupeado

| Diretório/Arquivo | Conteúdo |
|-------------------|----------|
| `config.yaml` | Configuração principal do agente |
| `SOUL.md` | Documento de personalidade |
| `skills/` | Todas as skills instaladas (SKILL.md + suporte) |
| `cron/` | Cron jobs (jobs.json + scripts) |
| `profiles/` | Perfis dos agentes Flux |
| `memories/` | Memória persistente |
| `scripts/` | Scripts personalizados |
| `kanban/` | Boards Kanban |
| `.skills_prompt_snapshot.json` | Snapshot de skills |
| `plugins.json` | Lista de plugins instalados |

## O que NUNCA é backupeado

- `.env` e arquivos com tokens/senhas
- `auth.json` (tokens OAuth)
- `sessions/` (histórico de conversas, ~40MB)
- `logs/`, `cache/`, `node_modules/`
- Código fonte (`hermes-agent/`, `hermes/`)

## Setup inicial

### 1. Token GitHub

Precisa de um token GitHub com permissão de ESCRITA. Dois caminhos:

**Opção A — Classic PAT (recomendado):**
1. Acesse https://github.com/settings/tokens
2. Generate new token (classic)
3. Escopos: `repo` (obrigatório)
4. Cole o token no `.env`: `GITHUB_TOKEN=ghp_xxx`

**Opção B — Fine-grained PAT:**
1. Acesse https://github.com/settings/tokens?type=beta
2. New fine-grained token
3. Repository access: selecione o repo de backup
4. Permissions: **Contents: Read and write**
5. Cole o token no `.env`

### 2. Repositório

O backup usa o repositório `Flux-Agencia` na pasta `hermes-backup/`.

**Para documentação de referência (opcional):**
Se quiser manter um manifesto legível (como `HERMES_MANIFEST.md`) no repo raiz, veja o procedimento em `references/api-direct-upload.md` — permite commitar vĩa API REST sem precisar do git CLI instalado.

### 3. Configurar cron

```bash
# Cron diário à meia-noite
hermes cron create "0 0 * * *" --name "hermes-github-backup"
```

## Script de backup

Local: `/opt/data/hermes-backup-repo/hermes-backup/backup.py`

Execução manual:
```bash
python3 /opt/data/hermes-backup-repo/hermes-backup/backup.py
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `git push` 403 | Token não tem permissão de escrita — recrie com scope `repo` (classic) ou `Contents: R/W` (fine-grained) |
| `git push` 403 com fine-grained PAT | Além de `Contents: Read and write`, verifique em "Repository access" que o repositório-alvo está selecionado. Fine-grained PATs exigem seleção explícita de repositório. |
| Token Classic vs Fine-grained | **Prefira Classic PAT** com scope `repo` — é 1 clique e funciona. Fine-grained PATs exigem configuração separada de "Repository access" + "Contents: Read and write". O token Classic começa com `ghp_`, o fine-grained com `github_pat_`. |
| GITHUB_TOKEN não encontrado | Adicione `GITHUB_TOKEN=seu_token` em `/opt/data/.env` |
| Token expirado | Renove em https://github.com/settings/tokens. Classic PATs expiram em 90 dias por padrão. |
| "nada a commitar" | Normal — nenhuma mudança desde o último backup |
| Repo não existe | Verifique que o repo de backup existe no GitHub |
| HOME path mismatch no Docker | O script já usa token-in-URL (`git remote set-url origin https://user:token@...`) para evitar problemas com credential store em containers |
| Script não encontra `/opt/data/.env` | Cron jobs executam com `HERMES_HOME=/opt/data`. O script tenta ambos `/opt/data/.env` e `~/.hermes/.env` como fallback |
| Histórico muito grande (sessions) | Sessions NUNCA vão pro backup — o `.gitignore` bloqueia `sessions/` e `*.jsonl` |

## Suporte

- **Pesquisa de skills nos marketplaces**: `references/skills-marketplace-research.md` — catálogo dos melhores repos de skills de marketing e design encontrados no clawhub.ai, skills.sh e GitHub (pesquisa 2026-05-10). Lista skills instaladas e recomendadas para a Agência Flux.
- **Script de backup**: `scripts/backup.py` — script completo. Copiar para `~/.hermes/scripts/hermes-backup.py` para uso com cron `no_agent=true`. IMPORTANTE: o script lê `GITHUB_TOKEN` de `/opt/data/.env` (HERMES_HOME), não de `~/.hermes/.env`.
- **Template .gitignore**: `templates/.gitignore` — usar como base ao configurar novo repo de backup. Já exclui .env, tokens, sessions, logs, cache.
- **Diagnóstico de token 403**: skill `github-auth` → `references/fine-grained-pat-triage.md` — evidência concreta da sessão onde fine-grained PAT falhou e Classic PAT resolveu.
