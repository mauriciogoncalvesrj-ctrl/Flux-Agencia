---
name: flux-config-audit
description: "Metodologia para auditar o estado real da configuração da Agência Flux — cruzar memória, histórico de sessões, skills e configs para verificar o que foi implementado vs o que ficou pendente. Use quando o usuário pedir 'verifica o que foi feito e o que falta', 'status das pendências' ou similar."
version: 1.0.0
metadata:
  hermes:
    tags: [flux-agency, audit, configuration, methodology]
    related_skills:
      - flux-model-routing
      - flux-orchestrator
---

# Flux Config Audit — Verificação de Pendências

## Quando Usar

Quando o usuário pedir:
- "Verifica o que foi feito e o que falta"
- "Status das mudanças pendentes"
- "O que precisa ser atualizado ainda?"
- Qualquer request que envolva conferir estado real vs planejado de skills, perfis ou configs

## Metodologia em 4 Passos

### Passo 1: Extrair Pendências da Memória

Leia a memória persistente em busca de entradas marcadas como `PENDÊNCIA`, `falta`, `precisa de patch`, `ainda não foi feito`, ou qualquer item com ❌/🔴.

Palavras-chave para buscar na memória:
- "PENDÊNCIA"
- "precisa de patch"
- "ainda não"
- "não funciona"
- "skill_manage não encontra"

### Passo 2: Carregar Skills Mencionadas

Para cada skill pendente, use `skill_view(name)` para verificar o estado atual:

- ✅ **Versão** — está a versão esperada?
- ✅ **Seções** — a seção prometida (ex: "Common Pitfalls") existe?
- ✅ **Arquivos de referência** — os arquivos mencionados existem? Use `skill_view(name, file_path)` para confirmar
- ✅ **Conteúdo técnico** — o bug/workaround descrito na pendência está documentado?

### Passo 3: Verificar Configs Reais (se terminal disponível)

Se tiver acesso ao terminal, confira o estado real dos arquivos:

```bash
# Perfis Hermes
cat /opt/data/profiles/*/config.yaml

# Config principal
cat /opt/data/config.yaml

# Skills versionadas
head -5 /opt/data/skills/flux/*/SKILL.md
```

Cruce o que está nos configs com o que está documentado nos skills. Discrepância = pendência.

### Passo 4: Sintetizar Relatório

Apresentar no formato:

```
## Status das Pendências

### 1. [Skill/Config] — [🟢/🟡/🔴]
- ✅ Item concluído: ...
- ❌ Item pendente: ...

### 2. [Próximo] — [🟢/🟡/🔴]
...
```

---

## Common Issues Encontradas

### skill_manage não acha skills flux/
Skills na categoria `flux/` (ex: `flux-model-routing`, `flux-orchestrator`) não são encontradas por `skill_manage(action='patch'/'edit'/'write_file')`. Apenas `create` funciona para essa categoria.

**Workaround:** Usar terminal para editar diretamente `/opt/data/skills/flux/<skill-name>/SKILL.md`.

### Config desatualizada vs skill desatualizada
Às vezes o config.yaml ou profile configs já foram corrigidos, mas o SKILL.md correspondente não foi atualizado para refletir as mudanças. Verificar ambos.

---

## Related Skills

- **flux-model-routing**: Model routing intelligence — verificar se reflete o estado real dos profiles
- **flux-orchestrator**: Meta-skill de orquestração — comum ter pending patches sobre pitfalls
- **flux-copy-estetica**: Verificar se workaround de vision_analyze está documentado
