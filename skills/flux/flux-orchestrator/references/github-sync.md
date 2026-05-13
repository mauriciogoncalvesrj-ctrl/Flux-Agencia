# GitHub Sync — Skills Flux

## Estado Atual (2026-05-13)

```
/opt/data/skills/flux/          ← Skills Flux (NÃO é repo git)
  ├── flux-orchestrator/
  ├── flux-prompt-engineer/
  ├── flux-copy-estetica/
  ├── flux-ads-audit/
  ├── flux-meta-ads-relatorio/
  ├── flux-meta-ads-balance-alert/
  ├── flux-competitor-spy/
  ├── flux-social-estetica/
  ├── flux-toprank-seo/
  ├── flux-landing-page-cro/
  ├── flux-daily-briefing/
  ├── flux-x-monitor/
  └── flux-agency-standards/

/opt/data/Flux-Agencia/          ← Repo git → GitHub
  ├── skills/
  │   └── flux-context.md        ← ÚNICO arquivo de skill no repo
  ├── flux-comms/                ← Protocolo cross-agent
  ├── hermes-backup/             ← Backup da config do Hermes
  └── ...
```

**Problema:** Toda correção/update em skills Flux (`/opt/data/skills/flux/`) fica isolada no VPS. O GitHub (`mauriciogoncalvesrj-ctrl/Flux-Agencia`) não recebe as alterações. Claude Code no Windows só enxerga o que está no GitHub.

## Por que sincronizar

- Claude Code (máquina Windows do Mauricio) acessa skills pelo GitHub
- Sem sync, as duas pontas (Hermes VPS + Claude Code) divergem
- Correções feitas aqui (ex: pipeline 5 portões, checklist, prompts-db) nunca chegam ao outro agente

## Opções de Sincronização

### Opção 1: Copiar para o repo (simples, manual)
```bash
cp -r /opt/data/skills/flux/* /opt/data/Flux-Agencia/skills/
cd /opt/data/Flux-Agencia
git add skills/
git commit -m "sync: flux skills $(date +%Y-%m-%d)"
git push
```
**Prós:** Imediato, sem reconfiguração.
**Contra:** Duas cópias — risco de editar a errada. Precisa ser feito manualmente a cada update.

### Opção 2: Symlink (link simbólico)
```bash
cd /opt/data/Flux-Agencia/skills/
ln -s /opt/data/skills/flux/* .
git add -A
git commit -m "sync: symlink flux skills"
git push
```
**Prós:** Única fonte de verdade (`/opt/data/skills/flux/`), git tracking automático.
**Contra:** Git rastreia o symlink, não o conteúdo. Claude Code ao clonar o repo recebe symlinks quebrados (apontam pra path que não existe no Windows).

### Opção 3: Inicializar /opt/data/skills/ como repo próprio
```bash
cd /opt/data/skills/
git init
git remote add origin https://github.com/mauriciogoncalvesrj-ctrl/Flux-Agencia.git
# OU criar repo separado: flux-skills
```
**Prós:** Git nativo, push/pull normais.
**Contra:** Mais um repo pra gerenciar. Precisa decidir se é repo separado ou branch do Flux-Agencia.

### Opção 4: Script de sync automático (recomendado)
Criar script que copia `/opt/data/skills/flux/` → `/opt/data/Flux-Agencia/skills/flux/` e commita. Rodar via cron ou manualmente após correções.

```bash
#!/bin/bash
# /opt/data/scripts/sync-flux-skills.sh
cp -r /opt/data/skills/flux/* /opt/data/Flux-Agencia/skills/flux/
cd /opt/data/Flux-Agencia
git add skills/flux/
git diff --cached --quiet || git commit -m "sync: flux skills $(date +%Y-%m-%d_%H%M)"
git push
```

## Notas

- **hermes-github-backup** faz backup da config do Hermes (`config.yaml`, `SOUL.md`, skills do agente) para `hermes-backup/` no mesmo repo. NÃO cobre as skills Flux em `/opt/data/skills/flux/`.
- **prompts-db.json** está em `/opt/data/flux-tools/prompts-db.json` — também fora do git. Deve ser incluído no sync.
- Após decidir a opção, atualizar este documento e remover o Common Mistake correspondente do `flux-orchestrator/SKILL.md`.
