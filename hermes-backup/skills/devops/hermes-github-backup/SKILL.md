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
| GITHUB_TOKEN não encontrado | Adicione `GITHUB_TOKEN=seu_token` em `/opt/data/.env` |
| "nada a commitar" | Normal — nenhuma mudança desde o último backup |
| Repo não existe | Verifique que o repo `Flux-Agencia` existe no GitHub |
