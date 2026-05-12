"""
github_api_upload.py — Upload de arquivos para GitHub via API REST quando git CLI
não está disponível (containeres mínimos, servidores gerenciados, etc).

Uso via import em scripts agent, ou standalone com PYTHONPATH ajustado.
"""
import json, base64, urllib.request, urllib.error

def read_env_token(path: str = "/home/hermeswebui/.hermes/.env", key: str = "GITHUB_TOKEN") -> str:
    """Lê token de .env local."""
    with open(path) as f:
        for line in f:
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip()
    raise ValueError(f"{key} não encontrado em {path}")


def upload_to_github(
    repo: str,
    path_on_repo: str,
    local_file: str,
    commit_message: str,
    branch: str = "main",
    token: str | None = None,
    env_file: str = "/home/hermeswebui/.hermes/.env",
    dry_run: bool = False,
) -> dict:
    """
    Cria ou atualiza um arquivo no GitHub via API REST de Conteúdos.

    Args:
        repo: formato 'owner/repo' (ex: 'mauriciogoncalvesrj-ctrl/Flux-Agencia')
        path_on_repo: caminho no repo (ex: 'config/HERMES_MANIFEST.md')
        local_file: caminho absoluto/local do arquivo
        commit_message: mensagem do commit
        branch: nome do branch (default: 'main')
        token: token explicito; se None, lê de env_file (key=GITHUB_TOKEN)
        env_file: caminho do .env com GITHUB_TOKEN
        dry_run: se True, apenas imprime o que faria

    Returns:
        dict com 'commit_sha', 'html_url', 'action' (created|updated|unchanged)

    Raises:
        urllib.error.HTTPError em caso de falha na API
        FileNotFoundError se local_file não existe
        ValueError se token não for encontrado
    """
    if token is None:
        token = read_env_token(env_file, "GITHUB_TOKEN")

    # Ler conteúdo
    with open(local_file, "r", encoding="utf-8") as f:
        content_raw = f.read()
    b64_content = base64.b64encode(content_raw.encode("utf-8")).decode("utf-8")

    url = f"https://api.github.com/repos/{repo}/contents/{path_on_repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Hermes-Backup-Script",
        "Content-Type": "application/json",
    }

    # 1. Verificar se arquivo existe (pegar SHA)
    sha = None
    try:
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            sha = data.get("sha")
            existing_b64 = data.get("content", "").replace("\n", "")
            # Comparar bytes decodificados para evitar commit desnecessário
            try:
                existing_raw = base64.b64decode(existing_b64).decode("utf-8")
                if existing_raw.strip() == content_raw.strip():
                    print(f"Conteúdo IGUAL ao existente. Nenhuma alteração em {path_on_repo}.")
                    return {
                        "action": "unchanged",
                        "html_url": data.get("html_url"),
                        "commit_sha": None,
                    }
            except Exception:
                pass  # força update se não conseguir decodificar
    except urllib.error.HTTPError as e:
        if e.code == 404:
            sha = None
        else:
            raise

    if dry_run:
        action = "update" if sha else "create"
        print(f"[DRY RUN] {action}: {local_file} -> {repo}/{path_on_repo} (branch={branch})")
        return {"action": action, "html_url": None, "commit_sha": None}

    # 2. Enviar
    payload = {
        "message": commit_message,
        "content": b64_content,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="PUT"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        response_json = json.loads(resp.read().decode())
        commit_sha = response_json["commit"]["sha"]
        html_url = response_json["content"]["html_url"]
        action = "updated" if sha else "created"
        print(f"✅ {action.upper()}: {path_on_repo} @ {commit_sha[:12]} — {html_url}")
        return {
            "action": action,
            "html_url": html_url,
            "commit_sha": commit_sha,
        }


def upload_manifest(
    local_manifest: str = "/home/hermeswebui/.hermes/hermes-backup-repo/hermes-backup/config/HERMES_MANIFEST.md",
    repo: str = "mauriciogoncalvesrj-ctrl/Flux-Agencia",
    path_on_repo: str = "config/HERMES_MANIFEST.md",
    branch: str = "main",
) -> dict:
    """
    Upload rápido do HERMES_MANIFEST.md para o GitHub.
    Wrapper conveniência — sem precisar lembrar todos os parâmetros.
    """
    return upload_to_github(
        repo=repo,
        path_on_repo=path_on_repo,
        local_file=local_manifest,
        commit_message="docs: atualiza manifesto de configuração do Hermes Agent",
        branch=branch,
    )


if __name__ == "__main__":
    # Teste standalone
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 github_api_upload.py <local_file> [path_on_repo] [repo] [branch]")
        print("  python3 github_api_upload.py /path/to/file.md config/file.md owner/repo main")
        sys.exit(1)

    local = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else local.rsplit("/", 1)[-1]
    repo = sys.argv[3] if len(sys.argv) > 3 else "mauriciogoncalvesrj-ctrl/Flux-Agencia"
    branch = sys.argv[4] if len(sys.argv) > 4 else "main"

    upload_to_github(repo=repo, path_on_repo=path, local_file=local,
                     commit_message="docs: atualiza arquivo via API", branch=branch)
