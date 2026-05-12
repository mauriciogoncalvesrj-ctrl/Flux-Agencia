---
name: Meta Ads — saldo real pré-pago
description: Correção definitiva para alertas/relatórios de saldo Meta Ads: usar funding_source_details.display_string, nunca balance bruto
status: active
updated: 2026-05-12
---

# Meta Ads — saldo real pré-pago

## Regra principal

Para contas pré-pagas do Meta Ads, o campo `balance` retornado por MCP/Graph é saldo contábil/bruto e pode divergir do painel. Não usar `balance` para alertas, relatórios ou SMS de saldo.

## Fonte correta

Consultar a Graph API preservando o prefixo `act_` no ID da conta e extrair o saldo de:

`funding_source_details.display_string`

Se `display_string` não vier ou a consulta falhar, reportar erro. Não fazer fallback para `balance`.

## Script fonte da verdade

- Script: `/opt/data/scripts/meta_ads_real_balance.py`
- Telegram diário: job `1ca2c29ca1d8`, modo script-only/no-agent
- SMS teste: job `744263672cb4`, consome JSON pré-calculado pelo script
- SMS real para clientes: permanece desativado até validação manual

## Saldos reais conferidos em 2026-05-12

- Taciana: R$ 0,00
- Luana: R$ 203,29
- Proton: R$ 1.364,82
- Alpha: R$ 2.108,91

## Cuidados

- Nunca remover o prefixo `act_` antes de consultar a Graph API.
- Não registrar tokens, connection strings, IDs completos de contas ou contatos em arquivos versionados.
- Para documentação pública/compartilhada, usar nomes de clientes e IDs redigidos.
