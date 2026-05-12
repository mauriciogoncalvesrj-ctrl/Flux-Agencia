---
name: flux-meta-ads-relatorio
description: Gera relatório semanal (segundas 9:10) e mensal (dia 1º 9:10) de campanhas Meta Ads por cliente. Inclui métricas gerais + TOP 5 criativos com links do Instagram. Formato pronto para copiar/colar.
category: flux
triggers:
  - cron semanal (segundas 9:10 BRT)
  - cron mensal (dia 1º 9:10 BRT)
  - comando manual
---

# Relatório Semanal/Mensal — Meta Ads

## ⚠️ Pitfalls

1. **NEVER use `engagement_rate_unified` as a field** — it's not valid for the insights API. Use `page_engagement / impressions * 100` to compute engagement rate manually.
2. **NEVER use a `curl()` helper that appends `access_token` to a URL that already contains it** — causes `OAuthException`. Use the `api()` pattern from the script: build params dict, url-encode them, then append `&access_token=` only once.
3. **Account `balance` field is misleading** — always use `funding_source_details.display_string` via Graph API direct call for the real spending power.
4. **`time_range` must be URL-encoded** — use `urllib.parse.urlencode({"time_range": json.dumps({...})})` not manual string construction.
5. **Instagram permalinks require 3 chained API calls**: `ad_id → creative.id → effective_instagram_media_id → permalink`. If any step returns empty, omit the link.
6. **Some accounts (e.g. KORP NUTRA) use OUTCOME_SALES** — they won't have messaging metrics. Skip “Mensagem” lines when `msgs == 0`.
7. **Cartão de crédito accounts (type=1)** have no prepaid balance — display “💳 Cartão de crédito” instead of a number.

## Cron Jobs

| Job | Schedule | ID |
|---|---|---|
| Semanal (segundas 9:10 BRT) | `10 12 * * 1` | `dec95f276e29` |
| Mensal (dia 1º 9:10 BRT) | `10 12 1 * *` | `606f71c16a63` |

Both deliver to `telegram:1212203404`.

## Script

The main script is at `scripts/gerar-relatorio.py`. Run with `--semanal` or `--mensal`. Outputs JSON with an array of reports. See `references/graph-api-quirks.md` for API details and pitfalls.

## Related Skills

- `flux-meta-ads-balance-alert` — daily balance alert (uses same Graph API token and account list)

## Formato do Relatório

```
Olá [NOME CLIENTE]! Segue abaixo relatório das campanhas do META ADS

Período: [DD/MM/AAAA] até [DD/MM/AAAA]

Impressões: [valor]
Alcance: [valor]
Taxa de Interação: [valor]%
Cliques: [valor]
Mensagem: [valor]
Custo por mensagem: R$ [valor]
Valor investido: R$ [valor]

Ranking TOP 5 Criativos:
🏆 1. [AD_NAME]
Mensagens: [N] | CPA: R$ [valor] | CTR: [valor]%
🔗 [Instagram_permalink]

🥈 2. [AD_NAME]
...
```

## Contas Monitoradas

| ID | Nome | Tipo |
|---|---|---|
| act_912031229902602 | Alpha Transformadores | B2B/Indústria |
| act_3572634436284536 | C01 - Alpha Transformadores | Subconta |
| act_392106056202806 | Proton Transformadores | B2B/Indústria |
| act_1073353887241970 | CA - Atual Luana | Clínica Estética |
| act_1308631537809149 | CA - Borgatteprincipal | Clínica Estética |
| act_911737697183748 | CA - Taciana | Clínica Estética |
| act_5182254948472799 | CA - Thabata Camargo | Clínica Estética |
| act_802273699351886 | KORP NUTRA | E-commerce |
| act_1415550266416617 | CA-01 Flux | Interna |
| act_26835555129380153 | CA - Larissa Manso | Clínica Estética |
| act_153133192304265 | Gabi Gonçalves | Clínica Estética |
| act_1755778031574400 | CA - TACIANA BKP | Backup |
| act_1095489361869934 | CA - Medecine | Clínica Estética |

**Nomes de exibição para clientes:**
- Alpha Transformadores → ALPHA TRANSFORMADORES
- Proton Transformadores → PROTON TRANSFORMADORES
- CA - Atual Luana → Luana Sampaio (nome da cliente, não nome da conta)
- CA - Borgatteprincipal → BORGATTE
- CA - Taciana → TACIANA
- CA - Thabata Camargo → THABATA CAMARGO
- KORP NUTRA → KORP NUTRA

## Métricas e Fontes (Graph API v22.0)

### Resumo da conta
- **Endpoint**: `GET /act_{id}/insights?time_range=...&fields=impressions,reach,clicks,spend,ctr,actions,cost_per_action_type&level=account`
- **Impressões**: `impressions`
- **Alcance**: `reach`
- **Cliques**: `clicks`
- **CTR**: `ctr` (%)
- **Valor investido**: `spend`
- **Mensagens**: `onsite_conversion.total_messaging_connection` dentro de `actions[]`
- **Custo por mensagem**: `onsite_conversion.total_messaging_connection` dentro de `cost_per_action_type[]`
- **Taxa de Interação**: `page_engagement / impressions * 100` (calculada)

### TOP 5 Criativos
- **Endpoint**: `GET /act_{id}/insights?time_range=...&fields=ad_name,ad_id,impressions,spend,ctr,actions,cost_per_action_type&level=ad&limit=20`
- Ordenar por `onsite_conversion.total_messaging_connection` DESC (manual)
- **Mensagens**: `onsite_conversion.total_messaging_connection`
- **CPA**: `spend / mensagens`
- **CTR**: `ctr` (%)

### Link do Instagram
- Obter `creative.id` via `GET /{ad_id}?fields=creative`
- Obter `effective_instagram_media_id` via `GET /{creative_id}?fields=effective_instagram_media_id`
- Obter `permalink` via `GET /{media_id}?fields=permalink`
- Se não houver link, omitir a linha

### Saldo da conta
- **Endpoint**: `GET /act_{id}?fields=funding_source_details,spend_cap,amount_spent`
- `funding_source_details.type == 1` → Cartão de crédito (sem saldo pré-pago)
- `funding_source_details.type == 20` → Saldo pré-pago (extrair de `display_string`)
- Extrair valor com regex `R\$\s*([\d.,]+)` do campo `display_string`

## Lógica de Execução

### Semanal (toda segunda 9:10 BRT = 12:10 UTC)
- Período: últimos 7 dias
- Só gera relatório para contas com `spend > 0` no período
- Formato: um relatório por conta, enviado separadamente

### Mensal (dia 1º 9:10 BRT = 12:10 UTC)
- Período: mês anterior completo (01/mm/aaaa até 30 ou 31/mm/aaaa)
- Gera relatório para TODAS as contas com `spend > 0` no período
- Inclui saldo atual + dias restantes

### Splits por Unidade (contas com múltiplas unidades)

Algumas contas gerenciam mais de uma unidade/clínica na mesma conta de anúncios. O script detecta automaticamente a unidade pelo nome da campanha e gera relatórios **separados por unidade**.

**Configuração atual (UNIT_SPLIT no script):**
```python
UNIT_SPLIT = {
    "act_1073353887241970": {  # Luana Sampaio
        "units": [
            {"name": "Jundiaí", "match": r"\[JUNDIA[IÍ]\]"},
            {"name": "Cajamar", "match": r"\[CAJAMAR\]"},
        ],
        "shared_match": r"Cajamar e Jundia[iíí]",
        "shared_split": ["Jundiaí", "Cajamar"],  # split 50/50
    },
}
```

- Campanhas com `[JUNDIAI]` ou `[JUNDIAÍ]` no nome → relatório Jundiaí
- Campanhas com `[CAJAMAR]` no nome → relatório Cajamar
- Campanhas com "Cajamar e Jundiaí" no nome → divididas 50/50 entre as duas unidades
- Cada unidade recebe seu próprio relatório com métricas e TOP 5 separados
- Saída: "Olá Luana Sampaio — UNIDADE JUNDIAÍ!" e "Olá Luana Sampaio — UNIDADE CAJAMAR!"

**Pitfall:** Ao adicionar uma nova conta com unidades, adicione a config em `UNIT_SPLIT` no script. Sem isso, a conta gera relatório único (sem split).

**Pitfall:** O nome de exibição no greeting usa o `DISPLAY_NAMES` dict — não o nome da unidade. Para Luana Sampaio, o greeting é "Olá Luana Sampaio — UNIDADE JUNDIAÍ!".

### Considerações por tipo de conta
- **OUTCOME_ENGAGEMENT**: Mensagens como KPI principal
- **OUTCOME_AWARENESS**: Alcance e impressões como KPI principal
- **OUTCOME_SALES**: Conversões/compras como KPI principal
- Se múltiplas campanhas com objetivos diferentes, segregar o relatório por objetivo

## Formatação Brasileira
- Números: 1.234,56 (ponto para milhar, vírgula para decimal)
- Moeda: R$ 1.234,56
- Porcentagem: 0,56%

## Geração de PDF Profissional

Quando o usuário pedir relatórios em PDF, usar **Puppeteer (Node.js)** — `fpdf2`/`reportlab` Python não estão disponíveis no container.

### Passos
1. Criar HTML profissional com design caprichado (ver `templates/relatorio-template.html` para referência)
2. Renderizar com `scripts/render_pdf.js`:
   ```
   node /opt/data/skills/flux/flux-meta-ads-relatorio/scripts/render_pdf.js <input.html> <output.pdf>
   ```
3. Enviar o PDF via `MEDIA:/path/to/file.pdf`

### Design Patterns
- **Capa**: gradiente temático por cliente, nome, período, métricas resumidas, `page-break-after: always`
- **Métricas**: grid de cards com `.metrics-grid` (CSS Grid auto-fit)
- **Ranking**: tabela com badges (🏆🥈🥉) e links Instagram
- **Insights**: box com borda lateral colorida (`.insight-box`)
- **Rodapé**: nome da agência, data de geração
- **Cores por identidade**: Alpha (roxo/azul), Proton PROMO (laranja), Proton Advantage+ (verde)
- **Font**: Inter (Google Fonts CDN) — funciona offline com fallback sans-serif
- **Print CSS**: `-webkit-print-color-adjust: exact` + `print-color-adjust: exact`

### Pitfalls
- Puppeteer precisa de `--no-sandbox --disable-setuid-sandbox` no container
- Google Fonts CDN: se sem internet, fallback para system sans-serif (aceitável)
- Links Instagram devem ser `<a>` reais no HTML para aparecerem no PDF
- Proton tem 2 conjuntos ativos → gerar PDFs **separados** por conjunto (PROMO MAIO e Advantage+)

## Token
Localizado em `/opt/data/.env` na variável `META_ACCESS_TOKEN`.