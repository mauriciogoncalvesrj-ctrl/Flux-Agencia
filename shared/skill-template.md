# SKILL.md Template — Flux Skills Padronizado

> Template para novas skills Flux. Baseado no padrão Corey Haines, adaptado para PT-BR e contexto de agência.
>
> Usar este template AO CRIAR ou REFATORAR qualquer skill Flux.

---

```markdown
---
name: flux-nome-da-skill
description: "[Descrição da skill em uma frase — quando ativar e o que faz]"
metadata:
  version: 1.0.0
  category: "[ads | crm | content | seo | analytics | strategy | creative | ops]"
  language: pt-br
  market: estetica-saude-beleza
---

# [Nome da Skill]

Você é um especialista em [área] para clínicas de estética, saúde e beleza no mercado brasileiro.
[Tua função e responsabilidade — 2-3 frases.]

## Antes de Começar

1. **Contexto do cliente:** Leia `.agents/contexts/[cliente]/product-marketing-context.md` para entender produto, audiência e posicionamento
2. **Ferramentas disponíveis:** Consulte `shared/TOOLS-REGISTRY.md` para ver quais MCPs/APIs/scripts estão ativos
3. **Regras de marca:** Consulte `shared/glossario.md` — NUNCA cite "GHL" ou "GoHighLevel" em material de cliente. Use "Sistema Flux 360"
4. **Decisões de arquitetura:** Consulte `shared/decisions-log.md` para alinhamento estratégico

## Processo / Framework

### Passo 1: [Nome do passo]
[O que fazer, como fazer, perguntas-chave.]

### Passo 2: [Nome do passo]
[O que fazer, como fazer.]

### Passo 3: [Nome do passo]
[O que fazer, como fazer.]

## Formato de Entrega

[Template ou estrutura exata do output esperado.]

```markdown
# [Título do entregável]

## [Seção 1]
[Conteúdo]

## [Seção 2]
[Conteúdo]
```

## Erros Comuns

| Erro | Por que acontece | Correção |
|------|-----------------|----------|
| [Erro comum 1] | [Motivo] | [Como corrigir] |
| [Erro comum 2] | [Motivo] | [Como corrigir] |
| [Erro comum 3] | [Motivo] | [Como corrigir] |

## Perguntas Específicas da Tarefa

Antes de começar, pergunte ao usuário se não souber:
1. [Pergunta 1]
2. [Pergunta 2]
3. [Pergunta 3]

## Skills Relacionadas

| Skill | Quando usar |
|-------|-------------|
| [skill-relacionada-1] | [Quando delegar para esta skill] |
| [skill-relacionada-2] | [Quando delegar para esta skill] |

## Ferramentas

| Ferramenta | Interface | Uso nesta skill |
|-----------|-----------|-----------------|
| [Ferramenta 1] | [MCP/CLI/API] | [Como usar] |
| [Ferramenta 2] | [MCP/CLI/API] | [Como usar] |

---

> **Referência:** `shared/TOOLS-REGISTRY.md` para catálogo completo de ferramentas.
```

---

## Instruções de Uso

1. Copiar este template para `skills/flux/flux-nome-da-skill/SKILL.md`
2. Preencher todas as seções — não pular "Erros Comuns" nem "Skills Relacionadas"
3. Se a skill tiver referências longas, mover para `references/`
4. Se a skill tiver scripts/assets, colocar em `scripts/` ou `assets/`
5. Adicionar a skill ao `VERSIONS.md`
6. Rodar `skillscan` antes de publicar

---

## Checklist de Qualidade

- [ ] Frontmatter com name, description, version, category
- [ ] Seção "Antes de Começar" referencia product-marketing-context.md
- [ ] Seção "Erros Comuns" tem pelo menos 2 erros documentados
- [ ] Seção "Formato de Entrega" tem template de output
- [ ] Seção "Skills Relacionadas" referencia skills que existem
- [ ] Seção "Ferramentas" lista ferramentas reais do TOOLS-REGISTRY.md
- [ ] Linguagem consistente em pt-br
- [ ] Termos técnicos substituídos conforme glossario.md para material de cliente
