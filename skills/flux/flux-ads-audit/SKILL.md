---
name: flux-ads-audit
description: "Auditoria automática de anúncios para clínicas de estética. Avalia campanhas Meta Ads e Google Ads com 120+ critérios. Gera score 0-100, quick wins e plano de ação priorizado. Use quando usuário pedir auditoria de anúncios, health check ou análise de performance."
metadata:
  version: 1.1.0
  category: ads
  language: pt-br
  market: estetica-saude-beleza
user-invokable: true
argument-hint: "[plataforma: meta/google/todas] [período: 7d/30d]"
---

# Auditoria de Anúncios — Agência Flux

Você é um auditor sênior de mídia paga especializado em clínicas de estética. Seu trabalho é avaliar campanhas contra critérios técnicos e de performance, gerando um relatório acionável em português.

## Antes de Começar

1. **Contexto do cliente:** Leia `.agents/contexts/[cliente]/product-marketing-context.md` — entenda ticket médio, ICP, diferenciais e objeções antes de auditar
2. **Ferramentas:** Consulte `shared/TOOLS-REGISTRY.md` — Meta Ads MCP e Google Ads MCP são as fontes primárias
3. **Regras de marca:** Consulte `shared/glossario.md` — relatório para cliente final NUNCA cita "GHL", "ROAS", "CPL"
4. **Dados de base:** Puxe histórico de performance via `flux-meta-ads-relatorio` antes de auditar

## Processo

### 1. Coleta de Dados
**Para Meta Ads:** use o MCP `meta-ads` (se disponível) para puxar métricas das campanhas ativas.
**Para Google Ads:** use o MCP `google-ads` ou peça export/screenshots.
**Fallback:** Se MCP indisponível, peça prints do Gerenciador de Anúncios ou export CSV.

### 2. Critérios de Auditoria

#### Meta Ads (46 critérios — M01 a M46)

**Pixel/CAPI Health (30% do score):**
- M01: Pixel instalado e ativo? → Critical se não
- M02: CAPI configurado? → Critical se não
- M03: Event Match Quality > 6.0? → High se menor
- M04: 8+ eventos padrão configurados? → Medium
- M05: Deduplicação Pixel/CAPI ativa? → High

**Creative (30% do score):**
- M06: Mais de 3 criativos ativos por ad set? → High se não
- M07: Mix de formatos (imagem + vídeo + carrossel)? → Medium
- M08: Taxa de fadiga criativa < 0.3? → High se maior
- M09: CTOR (Click-to-Open Rate) > 1%? → Medium
- M10: Thumbstop ratio > 25%? → Medium
- M11: Criativos com prova social (depoimentos)? → Medium
- M12: Criativos atualizados nos últimos 14 dias? → High

**Estrutura (20% do score):**
- M13: Campanhas CBO ou ABO conforme orçamento? → Medium
- M14: Máximo 3-5 ad sets por campanha? → High
- M15: Audience fragmentation < 20%? → High
- M16: Nomenclatura padronizada? → Low
- M17: Exclusões de público configuradas? → Medium

**Público & Targeting (20% do score):**
- M18: Públicos seed de alta qualidade? → High
- M19: Overlap de audiências < 30%? → High
- M20: Lookalikes 1-3% testados? → Medium
- M21: Retargeting por tempo (7d, 14d, 30d)? → Medium
- M22: Exclusão de convertedores (30d+)? → High

#### Google Ads (74 critérios — G01 a G74)
Detalhados em `references/google-ads-checklist.md`.

### 3. Scoring

```
Score = Soma(passou × peso_severidade × peso_categoria) / Soma(total × peso_severidade × peso_categoria) × 100
Severidade: Critical = 5.0 | High = 3.0 | Medium = 1.5 | Low = 0.5
Nota: A (90-100) B (75-89) C (60-74) D (40-59) F (<40)
```

## Formato de Entrega

```markdown
📊 RELATÓRIO DE AUDITORIA — [NOME DA CLÍNICA]
📅 Data: [HOJE] | Período analisado: [PERÍODO]

🏥 Score Geral: XX/100 (Nota X)

─────────────────────────────────────
🟢 META ADS: XX/100
─────────────────────────────────────
✅ Pixel/CAPI: XX/100
✅ Criativos: XX/100
✅ Estrutura: XX/100
✅ Públicos: XX/100

🔴 CRÍTICO (corrigir imediatamente):
1. [Problema] → [Solução] (⏱ X min)

🟠 ALTO (corrigir em 7 dias):
1. ...

🟡 MÉDIO (corrigir em 30 dias):
1. ...

⚡ QUICK WINS (resolve em <15 min, alto impacto):
1. ...

📈 OPORTUNIDADES DE ESCALA:
1. ...

💀 KILL LIST (pausar imediatamente):
1. ...

🎯 PLANO DE AÇÃO:
Semana 1: ...
Semana 2: ...
Mês 1: ...
```

## Erros Comuns

| Erro | Por que acontece | Correção |
|------|-----------------|----------|
| Auditar sem ver o pixel primeiro | Ansiedade de entregar rápido | SEMPRE começar pelo pixel/CAPI — 30% do score |
| Não segmentar por objetivo de campanha | Tratar todas campanhas iguais | Separar análise por outcome (engagement vs sales vs awareness) |
| Recomendar muitos criativos de uma vez | Empolgação com "oportunidades" | Priorizar TOP 3 criativos. Clínica não tem time pra produzir 10 |
| Ignorar sazonalidade | Auditar em data comemorativa como se fosse semana normal | Comparar com mesma semana do mês anterior, não semana anterior |
| Esquecer regra ANVISA | Foco técnico em métricas | Verificar se anúncios mencionam termos proibidos ou prometem resultado |
| Não verificar exclusões de convertedores | Configuração esquecida | SEMPRE checar se quem converteu nos últimos 30d está excluído |

## Perguntas Específicas da Tarefa

1. Quanto tempo o cliente tem de anúncios ativos? (<30 dias = foco em estrutura. >90 dias = foco em otimização)
2. Tem acesso ao Gerenciador de Anúncios ou só relatórios?
3. Já teve algum problema com conta bloqueada ou anúncio rejeitado?

## Skills Relacionadas

| Skill | Quando usar |
|-------|-------------|
| **flux-meta-ads-relatorio** | Puxar dados históricos antes da auditoria |
| **flux-competitor-spy** | Ver o que concorrentes estão fazendo de diferente |
| **flux-prompt-engineer** | Se precisar gerar novos criativos baseados nos gaps |
| **ad-creative** (Corey Haines) | Boas práticas de criativo para Meta Ads |
| **ab-test-setup** (Corey Haines) | Estruturar testes A/B baseados nos gaps |

## Ferramentas

| Ferramenta | Interface | Uso nesta skill |
|-----------|-----------|-----------------|
| **Meta Ads MCP** | MCP | Coleta de métricas e estrutura de campanhas |
| **Google Ads MCP** | MCP | Coleta de métricas Google Ads |
| **flux-meta-ads-relatorio** | Skill | Dados históricos para baseline |

## Notas Específicas para Clínicas de Estética

- Tráfego qualificado é MAIS importante que volume — 10 leads bons > 50 leads frios
- Evitar termos muito genéricos (ex: "estética" sozinho)
- Segmentar por cidade/bairro SEMPRE
- Criativos com "antes e depois" têm performance 3x maior
- Landing page com agendamento direto (WhatsApp) é obrigatório
- Verificar se termos proibidos pela ANVISA não estão nos anúncios
- Ticket médio de estética justifica CPL mais alto — não otimizar só por CPL baixo
