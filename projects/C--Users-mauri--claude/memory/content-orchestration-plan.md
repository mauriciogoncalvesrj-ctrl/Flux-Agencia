---
name: content-orchestration-plan
description: "Plano de orquestração de conteúdo Flux — 5 setores, agentes, quality gate, vault system"
metadata: 
  node_type: memory
  type: project
  originSessionId: a49deb1e-6df2-49d5-abdb-3960d30d0e0d
---

# Content Orchestration System — Plano Aprovado

## Status: ✅ IMPLEMENTADO — Score 2.25/10 → 8.5/10 (2026-06-27)

## Arquitetura — 5 Setores
1. **Inteligência** — Social listening, concorrentes, tendências (3 sub-agentes)
2. **Estratégia** — Pilares, calendário, território visual (1 agente)
3. **Criação** — Copy + visual + overlay (3 sub-agentes)
4. **Qualidade** — Brand audit + compliance ANVISA/CFM (2 sub-agentes)
5. **Distribuição** — GHL MCP scheduling (1 agente)

## Fluxo
```
PEDIDO → INTELIGÊNCIA → ESTRATÉGIA → CRIAÇÃO → QUALIDADE → DISTRIBUIÇÃO
```

## Skills instaladas (skills.sh)
- social-content, content-strategy, copywriting, ad-creative, marketing-psychology

## Modelos por tarefa
- Inteligência/Qualidade: deepseek-v4-pro
- Estratégia: mimo-v2.5-pro
- Copy/Visual/Distribuição: mimo-v2.5
- Imagem: Fal.ai Schnell ($0.003/img)

## Referências
- SEO Agency in a Box (github.com/z1fex/SEO-AGENCY-IN-A-BOX) — vault system, 75 agentes, quality gates
- skills.sh — 21 marketing skills
- Brand Profile — hooks, paleta, territórios
- DESIGN.md — DNA visual, estrutura obrigatória

## Arquivo do plano completo
`C:\Users\mauri\.claude\plans\content-orchestration-system.md`
