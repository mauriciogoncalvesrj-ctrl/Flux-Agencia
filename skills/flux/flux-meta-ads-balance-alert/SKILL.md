---
name: flux-meta-ads-balance-alert
description: Sistema de alerta diário de saldo de contas Meta Ads. Consulta saldo real via Graph API, calcula dias restantes de gasto, e gera alertas consolidados + individuais por cliente. Executado diariamente às 9h Brasília (12h UTC).
category: flux
---

# Alerta Diário de Saldo — Meta Ads

## Antes de Começar

1. **Contexto do cliente:** Leia `.agents/contexts/[cliente]/product-marketing-context.md` para nome de exibição correto
2. **Ferramentas:** Graph API direta (`funding_source_details`) + MCP Meta Ads. Token em `/opt/data/.env`
3. **Regras de marca:** Consulte `shared/glossario.md` — mensagem para cliente: "saldo da sua conta de anúncios" não "account balance"

## Objetivo
Monitorar diariamente o saldo das contas de anúncios do Meta Ads, alertar quando o saldo cobre menos de 3 dias de gasto, e fornecer templates prontos para comunicação com clientes.

## Contas monitoradas (13 contas)
As contas são consultadas dinamicamente via MCP `mcp_meta_ads_get_ad_accounts` ou via Graph API direta.

## Arquitetura

### Fonte do saldo real
O campo `balance` do MCP `get_ad_accounts` é **saldo contábil, não o saldo disponível real**.

Usar endpoint direto da Graph API:
```
GET https://graph.facebook.com/v22.0/{act_id}?fields=funding_source_details,spend_cap,amount_spent,currency&access_token={TOKEN}
```

- `funding_source_details.type == 1` → Cartão de crédito (sem limite pré-pago)
- `funding_source_details.type == 20` → Saldo pré-pago (extrair valor de `display_string` com regex `R\$\s*([\d.,]+)`)

### Cálculo de gasto recente
```
GET https://graph.facebook.com/v22.0/{act_id}/insights?date_preset=last_7d&fields=spend&access_token={TOKEN}
```
- `media_dia = spend_7d / 7`
- `dias_restantes = saldo / media_dia`

### Listagem de campanhas ativas (para orçamento diário)
```
GET https://graph.facebook.com/v22.0/{act_id}/campaigns?fields=name,status,daily_budget&limit=50&access_token={TOKEN}
```
Filtrar `status == "ACTIVE"` e somar `daily_budget / 100`.

### Token
Localizado em `/opt/data/.env` na variável `META_ACCESS_TOKEN`.

## Thresholds de alerta
- 🚨 **Crítico**: dias_restantes < 3 → alerta vermelho
- ⚠️ **Atenção**: dias_restantes < 5 → alerta amarelo
- ✅ **OK**: dias_restantes >= 5

## Formato de saída

### Formato 1: Resumo Consolidado
Mensagem única com todas as contas ativas, ordenadas por criticidade.

```
📢 META ADS — ALERTA DE SALDOS
{DATA}

🏢 {NOME}
💰 Saldo: R$ {VALOR}
📊 Gasto 7d: R$ {VALOR} | Média/dia: R$ {VALOR}
⏱️ Saldo cobre: ~{N} dias {EMOJI}

... (repetir para cada conta ativa)

🚨 CONTAS CRÍTICAS:
• {NOME} — {DIAS} dias restantes
```

### Formato 2: Individual por Cliente
Para cada conta com dias_restantes < 3, enviar mensagem separada com template:

```
📢 META ADS — ALERTA DE SALDO

Olá! Passando para te avisar que o saldo da conta de anúncios **{NOME_CONTA}** está em **R$ {VALOR}**, o que cobre apenas **{N} dias** de anúncios.

Para manter a performance e evitar pausas, o ideal é atualizar o saldo o quanto antes.

Qualquer coisa, estou por aqui! 😊
```

## Cross-references
- `flux-meta-ads-relatorio` — weekly/monthly reporting skill using same Graph API. See its `references/graph-api-quirks.md` for detailed API field validity notes.
- Both skills share `/opt/data/.env` token and the `DISPLAY_NAMES` account map.

## Fluxo de execução
1. Obter token do `/opt/data/.env`
2. Listar todas as contas via MCP ou Graph API
3. Para cada conta, consultar:
   - Saldo real (`funding_source_details`)
   - Gasto últimos 7 dias (`insights?date_preset=last_7d`)
   - Campanhas ativas e orçamento diário
4. Filtrar contas com `spend_7d > 0` (ativas)
5. Calcular `dias_restantes` para cada uma
6. Gerar e enviar **resumo consolidado** como resposta principal
7. Para cada conta com `dias_restantes < 3`, enviar **alerta individual** via `send_message` para o Telegram
