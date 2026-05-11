# Upload de Arquivos para GitHub via API REST (Sem git CLI)

Quando o Hermes Agent está rodando em um container mínimo ou ambiente que **não tem o `git` instalado**, ainda é possível enviar arquivos para o repositório de backup usando a **API REST de Conteúdos do GitHub**.

## Quando usar

- Container `hermes-flux` não tem `git` CLI
- Hermes WebUI standalone sem privilégios de shell
- Qualquer ambiente onde `git push` falha com `No such file or directory`
- Quando se quer **commitar apenas um arquivo específico** (ex: manifesto) sem sincronizar o repo inteiro

## Pré-requisitos

- `GITHUB_TOKEN` válido no `.env` com permissão `repo` (classic) ou `Contents: Read and write` (fine-grained)
- Python 3.8+ (já presente em todos os containers Hermes)
- `urllib` e `json` (builtin — sem dependências externas)

## Endpoint da API

```
PUT https://api.github.com/repos/{owner}/{repo}/contents/{path}
```

### Headers obrigatórios

```
Authorization: token {GITHUB_TOKEN}
Accept: application/vnd.github.v3+json
User-Agent: Hermes-Backup-Script
Content-Type: application/json
```

### Payload JSON

```json
{
  "message": "docs: atualiza manifesto",
  "content": "base64EncodedContentHere",
  "branch": "main",
  "sha": "existing-sha-here"  // obrigatório apenas para UPDATE, omitir para CREATE
}
```

## Fluxo Completo

### Passo 1 — Verificar se arquivo existe (GET)

```python
import urllib.request, json

url = "https://api.github.com/repos/mauriciogoncalvesrj-ctrl/Flux-Agencia/contents/config/HERMES_MANIFEST.md"
headers = {
    "Authorization": "token ghp_xxx",
    "Accept": "application/vnd.github.v3+json",
}

req = urllib.request.Request(url, headers=headers, method="GET")
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        sha = data.get("sha")  # ← necessário para update
        print(f"Arquivo existe. SHA: {sha[:20]}...")
except urllib.error.HTTPError as e:
    if e.code == 404:
        print("Arquivo não existe — será criado.")
        sha = None
    else:
        raise
```

### Passo 2 — Preparar conteúdo

```python
import base64

with open("HERMES_MANIFEST.md", "r", encoding="utf-8") as f:
    content = f.read()

b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
```

### Passo 3 — Enviar (PUT)

```python
payload = {
    "message": "docs: atualiza manifesto de configuração do Hermes Agent",
    "content": b64,
    "branch": "main",
}
if sha:  # update
    payload["sha"] = sha

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="PUT"
)

with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode())
    commit = data["commit"]["sha"]
    url = data["content"]["html_url"]
    print(f"✅ Commit: {commit[:12]} — {url}")
```

## Otimização — Evitar Commit Desnecessário

O conteúdo da API vem em base64 sem quebras de linha. Antes de fazer PUT:

```python
import base64

# Comparar bytes reais para não criar commit quando nada mudou
try:
    existing_decoded = base64.b64decode(data["content"].replace("\n", "")).decode("utf-8")
    if existing_decoded.strip() == content.strip():
        print("Conteúdo igual. Nenhuma alteração.")
        return  # skip
except Exception:
    pass  # força update se não conseguir decodificar
```

## Script Reutilizável

Ver `scripts/github_api_upload.py` — função `upload_to_github()` que encapsula todo o fluxo:

```python
from github_api_upload import upload_to_github, upload_manifest

# Upload genérico
upload_to_github(
    repo="mauriciogoncalvesrj-ctrl/Flux-Agencia",
    path_on_repo="config/HERMES_MANIFEST.md",
    local_file="/home/hermeswebui/.hermes/config.yaml",
    commit_message="docs: atualiza config",
)

# Upload rápido do manifesto
upload_manifest(
    local_manifest="/home/hermeswebui/.hermes/hermes-backup-repo/hermes-backup/config/HERMES_MANIFEST.md"
)
```

## Pitfalls

| Problema | Causa | Solução |
|---|---|---|
| `HTTP 404` no GET | Arquivo ainda não existe | Tratar como `sha=None` e fazer PUT sem `sha` |
| `HTTP 422` no PUT | SHA incorreta ou branch protegida | Verificar que a SHA veio do GET correto |
| `HTTP 401` | Token inválido ou expirado | Recriar token no GitHub Settings → Developer Settings |
| `HTTP 403` | Token sem permissão de escrita | Usar classic PAT com scope `repo` ou fine-grained com `Contents: R/W` |
| `FileNotFoundError: git` | Ambiente sem CLI git | Este documento — use a API direta |
| Conteúdo base64 truncado | `content` da API tem `\n` quebrando o base64 | Usar `.replace("\\n", "")` antes de `b64decode` |

## Cenários de Uso na Agência Flux

- **Manifesto de configuração**: documento legível que combina `config.yaml`, memória, skills e cron jobs num só README — ideal para referência rápida
- **Backup parcial**: quando só quer salvar a config, não o histórico de sessões
- **Documentação viva**: skills novas ou alterações que precisam aparecer no repo imediatamente
