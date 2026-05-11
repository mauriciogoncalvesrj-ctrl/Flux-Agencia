# Fine-Grained PAT Triage — Evidência da Sessão

## Problema

Usuário criou token `github_pat_11BWI...` (fine-grained PAT).
As chamadas `git push` e `PUT /repos/:owner/:repo/contents/:path` retornavam HTTP 403:

```json
{"message":"Resource not accessible by personal access token","status":"403"}
```

## Diagnóstico

### Passo 1: Verificar token scopes
```bash
curl -sI -H "Authorization: Bearer $TOKEN" https://api.github.com/user | grep X-OAuth-Scopes
# Resultado: X-OAuth-Scopes: none
```
Fine-grained PATs NÃO usam OAuth scopes — o header vem vazio. Isso é normal.

### Passo 2: Verificar permissões do repo
```python
GET /repos/mauriciogoncalvesrj-ctrl/Flux-Agencia
# Response:
{
  "permissions": {
    "admin": true,
    "maintain": true,
    "push": true,    # ← ISSO É AS PERMISSÕES DO USUÁRIO, NÃO DO TOKEN!
    "triage": true,
    "pull": true
  }
}
```

**ARMADILHA**: O objeto `permissions` na resposta da API reflete as permissões do **usuário autenticado**, não do **token**. Um fine-grained PAT pode ter menos permissões que o usuário.

### Passo 3: Testar escrita real
```python
PUT /repos/mauriciogoncalvesrj-ctrl/Flux-Agencia/contents/README.md
# Response: HTTP 403 "Resource not accessible by personal access token"
```

## Causa raiz

Fine-grained PATs exigem configurar **duas coisas** separadamente:
1. **Repository access**: selecionar quais repositórios o token pode acessar
2. **Contents: Read and write**: permissão específica para ler E escrever arquivos

Por padrão, `Contents` vem como **Read-only**. O usuário precisa mudar manualmente.

## Solução aplicada

O usuário criou um **Classic PAT** (`ghp_XXwF...`) com scope `repo`.
Funcionou imediatamente — sem precisar configurar permissões por recurso.

## Lição

**Sempre recomendar Classic PAT primeiro.** O caminho mais curto para o usuário:
1. https://github.com/settings/tokens → Generate new token (classic)
2. Marcar `repo` ✓
3. Copiar token que começa com `ghp_`

Só usar fine-grained se o usuário precisar de escopos muito específicos.
