# Template Canônico de SKILL.md — Agência Flux

Copiar e preencher este template ao criar qualquer nova skill no domínio `flux/`.

```markdown
---
name: flux-nome-da-skill
description: "O que faz + quando usar + trigger phrases. Mencionar skills relacionadas para scope boundaries. Máximo 1024 caracteres."
version: 1.0.0
metadata:
  hermes:
    tags: [tag1, tag2, tag3]
    related_skills: [skill-relacionada-1, skill-relacionada-2]
---

# Nome da Skill

**You are an expert [role].** Your goal is to [objetivo principal em uma frase].

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. [Categoria de contexto]
- [Pergunta específica]
- [Pergunta específica]

### 2. [Categoria de contexto]
- [Pergunta específica]

---

## [Framework ou Processo Principal]

### Step 1: [Nome da etapa]
[Descrição do que fazer nesta etapa. Usar bullets, código, ou tabelas conforme necessário.]

### Step 2: [Nome da etapa]
[Descrição]

### Step 3: [Nome da etapa]
[Descrição]

---

## Output Format

Definir o formato exato do entregável:

```
[Template do output esperado, com placeholders]
```

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| [Descrição do erro] | [Por que acontece] | [Como corrigir] |
| [Descrição do erro] | [Por que acontece] | [Como corrigir] |

---

## Task-Specific Questions

1. [Pergunta que ajuda a refinar a tarefa]
2. [Pergunta que ajuda a refinar a tarefa]
3. [Pergunta que ajuda a refinar a tarefa]

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| **[nome]** | [para que serve nesta skill] | MCP/CLI/Script | [link para integration guide] |

---

## Related Skills

- **skill-x**: Para [situação específica em que delegar para esta skill]
- **skill-y**: Para [situação específica em que delegar para esta skill]
```

## Instruções de preenchimento

1. **name:** prefixo `flux-`, lowercase, hyphens. Máx 64 chars. Deve bater com nome do diretório.
2. **description:** incluir trigger phrases (ex: "quando usuário mencionar 'X', 'Y', 'Z'"). Mencionar skills relacionadas para scope boundaries. Máx 1024 chars.
3. **version:** começar em 1.0.0. Incrementar MINOR para novas features, PATCH para correções.
4. **tags:** 2-5 tags relevantes para busca e categorização.
5. **related_skills:** skills Flux ou do sistema que esta skill referencia ou delega.

## Checklist de qualidade

- [ ] `name` bate com nome do diretório
- [ ] `description` tem trigger phrases e scope boundaries
- [ ] Primeira seção é "Before Starting" com check de product-marketing-context
- [ ] Framework principal tem passos numerados e claros
- [ ] "Output Format" mostra template exato do entregável
- [ ] "Common Mistakes" tem pelo menos 3 entradas
- [ ] "Tool Integrations" referencia tools do `references/tools-registry.md`
- [ ] "Related Skills" lista skills para delegação
- [ ] SKILL.md está abaixo de 500 linhas (detalhes vão para `references/`)
- [ ] Sem credenciais ou dados sensíveis no texto
