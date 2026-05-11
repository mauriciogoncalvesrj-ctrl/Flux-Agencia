#!/usr/bin/env python3
"""
Hermes Agent Daily Backup Script
Copia configs, skills, cron jobs, profiles e memories para repo Git.
Usado pelo cron job diário à meia-noite (horário de Brasília = 03:00 UTC).

Instalação:
  cp backup.py ~/.hermes/scripts/hermes-backup.py
  chmod +x ~/.hermes/scripts/hermes-backup.py
  hermes cron create "0 3 * * *" --name "Hermes GitHub Backup" --script hermes-backup.py --no-agent

IMPORTANTE: O token GITHUB_TOKEN precisa estar em /opt/data/.env (HERMES_HOME),
NÃO em ~/.hermes/.env. O cron usa HERMES_HOME=/opt/data.
"""

import os
import sys
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path

HERMES_HOME = "/opt/data"
BACKUP_REPO = "/opt/data/hermes-backup-repo"
BACKUP_DIR = os.path.join(BACKUP_REPO, "hermes-backup")

def run(cmd, cwd=BACKUP_REPO):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def copy_file(src, dst_dir):
    if os.path.isfile(src):
        dst = os.path.join(dst_dir, os.path.basename(src))
        shutil.copy2(src, dst)
        return True
    return False

def copy_dir(src, dst, ignore_patterns=None):
    if not os.path.isdir(src):
        return 0
    os.makedirs(dst, exist_ok=True)
    count = 0
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('__pycache__', 'node_modules', '.git')]
        rel_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_path) if rel_path != '.' else dst
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            if any(f.endswith(ext) for ext in ('.env', '.token', '.lock')):
                continue
            if f.startswith('.env') or f == 'auth.json':
                continue
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_dir, f)
            shutil.copy2(src_file, dst_file)
            count += 1
    return count

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Iniciando backup do Hermes Agent...")
    files_copied = 0

    # 1. Config
    config_dir = os.path.join(BACKUP_DIR, "config")
    os.makedirs(config_dir, exist_ok=True)
    for f in ["config.yaml", "SOUL.md"]:
        if copy_file(os.path.join(HERMES_HOME, f), config_dir):
            files_copied += 1

    # 2. Skills
    skills_src = os.path.join(HERMES_HOME, "skills")
    skills_dst = os.path.join(BACKUP_DIR, "skills")
    if os.path.exists(skills_dst):
        shutil.rmtree(skills_dst)
    count = copy_dir(skills_src, skills_dst)
    files_copied += count

    # 3. Cron
    cron_src = os.path.join(HERMES_HOME, "cron")
    cron_dst = os.path.join(BACKUP_DIR, "cron")
    if os.path.exists(cron_dst):
        shutil.rmtree(cron_dst)
    count = copy_dir(cron_src, cron_dst)
    files_copied += count

    # 4. Profiles
    profiles_src = os.path.join(HERMES_HOME, "profiles")
    profiles_dst = os.path.join(BACKUP_DIR, "profiles")
    if os.path.exists(profiles_dst):
        shutil.rmtree(profiles_dst)
    count = copy_dir(profiles_src, profiles_dst)
    files_copied += count

    # 5. Memories
    memories_src = os.path.join(HERMES_HOME, "memories")
    memories_dst = os.path.join(BACKUP_DIR, "memories")
    if os.path.exists(memories_dst):
        shutil.rmtree(memories_dst)
    count = copy_dir(memories_src, memories_dst)
    files_copied += count

    # 6. Scripts
    scripts_src = os.path.join(HERMES_HOME, "scripts")
    scripts_dst = os.path.join(BACKUP_DIR, "scripts")
    if os.path.exists(scripts_dst):
        shutil.rmtree(scripts_dst)
    count = copy_dir(scripts_src, scripts_dst)
    files_copied += count

    # 7. Kanban
    kanban_src = os.path.join(HERMES_HOME, "kanban")
    kanban_dst = os.path.join(BACKUP_DIR, "kanban")
    if os.path.exists(kanban_dst):
        shutil.rmtree(kanban_dst)
    count = copy_dir(kanban_src, kanban_dst)
    files_copied += count

    # 8. Skills snapshot
    if copy_file(os.path.join(HERMES_HOME, ".skills_prompt_snapshot.json"), os.path.join(BACKUP_DIR, "config")):
        files_copied += 1

    # 9. Plugins list
    plugins_dir = os.path.join(HERMES_HOME, "plugins")
    if os.path.isdir(plugins_dir):
        plugins_list = [d for d in os.listdir(plugins_dir) if os.path.isdir(os.path.join(plugins_dir, d))]
        with open(os.path.join(config_dir, "plugins.json"), "w") as f:
            json.dump({"installed_plugins": plugins_list, "backup_date": timestamp}, f, indent=2)
        files_copied += 1

    print(f"[{timestamp}] Total: {files_copied} arquivos copiados")

    # Git operations
    token = None
    env_paths = ["/opt/data/.env", os.path.expanduser("~/.hermes/.env")]
    for ep in env_paths:
        if os.path.isfile(ep):
            with open(ep) as f:
                for line in f:
                    if line.startswith("GITHUB_TOKEN="):
                        token = line.strip().split("=", 1)[1]
                        break
        if token:
            break

    if not token:
        print("❌ GITHUB_TOKEN não encontrado. Pulando push.")
        sys.exit(1)

    remote_url = f"https://mauriciogoncalvesrj-ctrl:{token}@github.com/mauriciogoncalvesrj-ctrl/Flux-Agencia.git"
    subprocess.run(f"git remote set-url origin '{remote_url}'", shell=True, cwd=BACKUP_REPO, capture_output=True)
    subprocess.run('git config user.name "Hermes Agent Backup"', shell=True, cwd=BACKUP_REPO, capture_output=True)
    subprocess.run('git config user.email "mauriciogoncalvesrj@gmail.com"', shell=True, cwd=BACKUP_REPO, capture_output=True)

    code, out, err = run("git add -A hermes-backup/")
    if code != 0:
        print(f"❌ git add falhou: {err}")
        sys.exit(1)

    code, out, err = run("git diff --cached --quiet")
    if code == 0:
        print("📭 Nenhuma mudança. Backup já está atualizado.")
        sys.exit(0)

    commit_msg = f"backup: {datetime.now().strftime('%Y-%m-%d %H:%M')} - {files_copied} arquivos"
    code, out, err = run(f'git commit -m "{commit_msg}"')
    if code != 0:
        print(f"❌ git commit falhou: {err}")
        sys.exit(1)

    code, out, err = run("git push origin main 2>&1")
    if code != 0:
        code2, out2, err2 = run("git push origin master 2>&1")
        if code2 != 0:
            print(f"❌ git push falhou: {err2}")
            sys.exit(1)

    print("🎉 Backup concluído com sucesso!")

if __name__ == "__main__":
    main()
