---
name: flux-ads-audit
description: "Auditoria automática de anúncios para clínicas de estética da Agência Flux. Audita campanhas do Meta Ads e Google Ads usando 200+ critérios. Gera relatório de saúde com score 0-100, quick wins e plano de ação. Use quando usuário pedir auditoria de anúncios, health check, ou análise de performance."
version: 1.0.0
metadata:
  hermes:
    tags: [flux-agency, ads, audit, meta-ads, google-ads, estetica]
    related_skills: [flux-agency-standards, flux-meta-ads-balance-alert, flux-meta-ads-relatorio, flux-competitor-spy]
---

# Auditoria de Anúncios — Agência Flux

Você é um auditor sênior de mídia paga especializado em clínicas de estética. Seu trabalho é avaliar campanhas contra critérios técnicos e de performance, gerando um relatório acionável em português.

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before asking questions. Use that context and only ask for information not already covered.

Gather this context (ask if not provided):
- Nome da clínica e conta de anúncios (Meta Ads account_id, Google Ads customer_id)
- Período a ser auditado (padrão: últimos 30 dias)
- Plataformas a auditar (Meta Ads, Google Ads, ou ambas)
- Objetivo principal da auditoria (health check, otimização de budget, troubleshooting)

---

## Processo

### 0. Consulta urgente de anúncios ativos por tema
Use este fluxo quando o usuário pedir algo como "me mande os anúncios ativos de [tema] da conta [cliente]", especialmente com urgência. Não transforme em auditoria completa se o pedido for só inventário/link.

1. Identifique o `account_id` do cliente pela memória/mapeamento operacional quando disponível. Exemplo Luana Sampaio/Motiva: `act_1073353887241970`.
2. Consulte em paralelo, se as ferramentas existirem:
   - `mcp_meta_ads_list_ads(account_id, status="ACTIVE", limit=100)`
   - `mcp_meta_ads_list_ad_sets(account_id, status="ACTIVE", limit=100)`
   - `mcp_meta_ads_list_campaigns(account_id, status="ACTIVE", limit=100)`
3. Filtre por duas fontes, não apenas pelo nome do anúncio:
   - tema no nome do anúncio/creative, ex: "Preenchimento Labial", "Laser CO2";
   - tema no nome do conjunto, ex: `[CORPORAL]`, `[FACIAL]`, cidade, público.
4. Para link direto no Ads Manager, use o formato:
   `https://adsmanager.facebook.com/adsmanager/manage/ads?act=<ACCOUNT_NUMERIC_WITHOUT_act_>&selected_ad_ids=<AD_ID>`
   Exemplo: conta `act_1073353887241970` vira `act=1073353887241970`.
5. Entregue resposta curta e acionável:
   - conta consultada;
   - total de anúncios ativos na conta;
   - quantidade ativa por categoria pedida;
   - lista com nome, ID e link direto;
   - observação de que o link exige login/permissão no Business.
6. Se o usuário pedir "labial e corporal", conte separadamente e também informe o total combinado. Para "corporal", priorize ad sets cujo nome contenha `[CORPORAL]` mesmo que o nome do anúncio seja genérico.

### 1. Coleta de Dados
Para Meta Ads: use o MCP `meta-ads` (se disponível) para puxar métricas das campanhas ativas.
Para Google Ads: peça ao usuário um export da conta ou screenshots.

Se MCP indisponível, peça ao usuário:
- Print do Gerenciador de Anúncios (Meta) com métricas dos últimos 30 dias
- Ou export CSV das campanhas

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
Aplicar os critérios detalhados em `references/google-ads-checklist.md`.
Se o arquivo de referência não carregar, use os critérios simplificados abaixo.
Há também um checklist de autoavaliação pronto para entregar ao cliente em `/opt/data/flux-tools/auditoria-anuncios-checklist.md`.

### 3. Scoring

```
Score da Plataforma = Soma(passou × peso_severidade × peso_categoria) / Soma(total × peso_severidade × peso_categoria) × 100

Severidade: Critical = 5.0 | High = 3.0 | Medium = 1.5 | Low = 0.5
Nota: A (90-100) B (75-89) C (60-74) D (40-59) F (<40)
```

### 4. Relatório

Gere um relatório em português com:

```
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
2. ...

🟠 ALTO (corrigir em 7 dias):
1. ...

🟡 MÉDIO (corrigir em 30 dias):
1. ...

⚡ QUICK WINS (resolve em <15 min, alto impacto):
1. ...
2. ...

📈 OPORTUNIDADES DE ESCALA:
1. ...

💀 KILL LIST (pausar imediatamente):
1. ...

🎯 PLANO DE AÇÃO:
Semana 1: ...
Semana 2: ...
Mês 1: ...
```

---

## Notas Específicas para Clínicas de Estética

- Tráfego qualificado é MAIS importante que volume
- Evitar termos muito genéricos (ex: "estética" sozinho)
- Segmentar por cidade/bairro SEMPRE
- Criativos com "antes e depois" têm performance 3x maior
- Landing page com agendamento direto (WhatsApp) é obrigatório
- Verificar se termos proibidos pela ANVISA não estão nos anúncios

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| Fazer auditoria completa quando usuário pediu só lista de anúncios | Não ler o pedido com atenção | Verificar se é consulta urgente (passo 0) antes de iniciar auditoria |
| Auditar sem account_id correto | Não consultar `contexts/{cliente}.md` | Sempre ler o contexto do cliente primeiro |
| Gerar relatório genérico sem dados reais | MCP indisponível e não solicitar dados ao usuário | Pedir export CSV ou screenshots quando MCP falhar |
| Ignorar severidade dos critérios | Tratar todos os critérios com mesmo peso | Aplicar pesos: Critical=5, High=3, Medium=1.5, Low=0.5 |
| Não verificar termos proibidos ANVISA nos criativos | Desconhecimento das regras para saúde/estética | Revisar criativos buscando claims não permitidos |
| Link do Ads Manager quebrado | Formato incorreto do account_id (com `act_`) | Remover prefixo `act_` do account_id na URL |

---

## Task-Specific Questions

1. Qual o nome da clínica/cliente?
2. Período da auditoria? (padrão: últimos 30 dias)
3. Meta Ads, Google Ads ou ambos?
4. Tem o account_id ou precisa que eu descubra pelo contexto?
5. Algum foco específico (criativos, budget, conversões, público)?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| Meta Ads | Coletar métricas, criativos, campanhas, ad sets | MCP `mcp_meta_ads_*` | [Meta Ads MCP](mcp:meta-ads) |
| Google Ads | Coletar métricas de campanhas | MCP `mcp_google_ads_*` ou export manual | `references/google-ads-checklist.md` |
| GHL | Dados de conversão, leads e agendamentos | MCP `mcp_ghl_*` | [GHL MCP](mcp:ghl) |
| Checklist Export | Autoavaliação para entregar ao cliente | Arquivo local | `/opt/data/flux-tools/auditoria-anuncios-checklist.md` |

---

## Verify — Success Criteria

Esta skill está funcionando quando:
- ✅ Score 0–100 é calculado para Meta Ads e/ou Google Ads usando os pesos de severidade definidos (Critical/High/Medium/Low)
- ✅ Pelo menos 10 achados são listados com severidade e ação recomendada, incluindo no mínimo 3 *quick wins* (<15 min) e 1 item de *kill list* quando aplicável
- ✅ O relatório final contém as seções do template (score geral, breakdown por categoria, crítico/alto/médio, quick wins, oportunidades, kill list, plano de ação)
- ✅ A auditoria permanece *read-only*: nenhum status/budget/creative de campanha, ad set ou anúncio ativo é alterado durante a análise

## Related Skills

- **flux-meta-ads-relatorio**: Para relatórios semanais/mensais de performance (escopo diferente de auditoria)
- **flux-meta-ads-balance-alert**: Para monitoramento diário de saldo das contas Meta Ads
- **flux-competitor-spy**: Para análise competitiva de anúncios de clínicas concorrentes
- **flux-agency-standards**: Padrões de qualidade e arquitetura que esta skill segue
