# Flux Meta Ads → GHL Contact Mapping

Last updated: 2026-05-12

## Client mapping

Used by the daily balance check cron (job `744263672cb4`) to send SMS alerts via GHL when Meta Ads coverage drops below 3 days.

| # | GHL Contact Name | GHL Contact ID | Meta Ads Account Name | Meta Ads Account ID |
|---|---|---|---|---|
| 104 | [#104] Motiva – Taciana Terres | `TLERdShLsQMxv59zM9Yw` | CA - Taciana | `act_911737697183748` |
| 141 | #141 Motiva – Alpha Transformadores | `zyGxJmMNtmVauwSV18XH` | Alpha Transformadores | `act_912031229902602` |
| 137 | [#137] Motiva – Proton Transformadores | `ajkGuHbvw1zQYAJ3Nz9i` | Proton Transformadores | `act_392106056202806` |
| 106 | [#106] Motiva – Luana Sampaio | `uJQ9bW3rTXMd4si0eNqZ` | CA - Atual Luana | `act_1073353887241970` |

## GHL SMS format

When sending alerts via `mcp_ghl_send_sms`:

```
ALERTA DE SALDO - {client_name}

Saldo atual: R${saldo:.2f}
Gasto medio/dia: R${media_dia:.2f}
Cobertura: {dias:.1f} dias

O saldo pode acabar em breve. Faca uma recarga!
```

Note: No emojis in SMS (character encoding issues on some carriers). Avoid special characters like ç/ã/é — use plain ASCII fallback ("Faca" not "Faça", "medio" not "médio").

## Rule

SMS is sent **ONLY** when `dias_cobertura = saldo / media_dia < 3.0`.

## Cron job

- **ID**: `744263672cb4`
- **Name**: Flux Meta Ads Balance Check
- **Schedule**: `0 12 * * *` (9 AM BRT)
- **Toolsets**: terminal, file, web (MCP tools available natively)
- **Approach**: Agent-driven cron with native MCP tool access (NOT external script via `hermes tool call` — that CLI subcommand does not exist)
