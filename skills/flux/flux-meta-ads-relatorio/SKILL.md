---
name: flux-meta-ads-relatorio
description: "Gera relatório semanal (segundas 9:10 BRT) e mensal (dia 1º 9:10 BRT) de campanhas Meta Ads por cliente. Inclui métricas gerais + TOP 5 criativos com links do Instagram. Usa mcp_meta_ads_get_insights, mcp_meta_ads_get_campaign_performance e Graph API para saldo. Formato pronto para copiar/colar no WhatsApp do cliente."
version: 1.0.0
metadata:
  hermes:
    tags: [flux, meta-ads, relatorio, semanal, mensal, criativos]
    related_skills: [flux-agency-standards, flux-meta-ads-balance-alert, flux-ads-audit]
---

# Relatório Semanal/Mensal — Meta Ads

**You are an expert Meta Ads analyst for Agência Flux.** Your goal is to generate polished, client-ready reports with accurate metrics, clean formatting, and actionable insights — never misleading data or broken links.

## Before Starting

**Check for product marketing context first:**
Read `/opt/data/skills/flux/contexts/{cliente}.md` before generating reports. Use that context for display names, brand voice, and goals. Only ask for information not already covered by the context file.

Gather this context (ask if not provided):
- Which client(s) need reports
- Report type: `semanal` (last 7 days) or `mensal` (previous full month)
- Token location (default: `/opt/data/.env` → `META_ACCESS_TOKEN`)
- Any account-specific overrides (split units, custom KPIs)

---

## Fluxo de Execução

### Step 1: Determinar período

- **Semanal (toda segunda 9:10 BRT = 12:10 UTC):** últimos 7 dias. Só gera relatório para contas com `spend > 0` no período.
- **Mensal (dia 1º 9:10 BRT = 12:10 UTC):** mês anterior completo (01/mm/aaaa até 30 ou 31/mm/aaaa). Gera relatório para TODAS as contas com `spend > 0` no período. Inclui saldo atual + dias restantes.

### Step 2: Coletar métricas da conta

**Endpoint**: `GET /act_{id}/insights?time_range=...&fields=impressions,reach,clicks,spend,ctr,actions,cost_per_action_type&level=account`

| Métrica | Campo Graph API |
|---------|----------------|
| Impressões | `impressions` |
| Alcance | `reach` |
| Cliques | `clicks` |
| CTR | `ctr` (%) |
| Valor investido | `spend` |
| Mensagens | `onsite_conversion.total_messaging_connection` (dentro de `actions[]`) |
| Custo por mensagem | `onsite_conversion.total_messaging_connection` (dentro de `cost_per_action_type[]`) |
| Taxa de Interação | `page_engagement / impressions * 100` (calculada manualmente) |

### Step 3: Coletar TOP 5 criativos

**Endpoint**: `GET /act_{id}/insights?time_range=...&fields=ad_name,ad_id,impressions,spend,ctr,actions,cost_per_action_type&level=ad&limit=20`

- Ordenar por `onsite_conversion.total_messaging_connection` DESC (manual)
- Mensagens: `onsite_conversion.total_messaging_connection`
- CPA: `spend / mensagens`
- CTR: `ctr` (%)

### Step 4: Resolver links do Instagram

3 API calls encadeadas:
1. `GET /{ad_id}?fields=creative` → obtém `creative.id`
2. `GET /{creative_id}?fields=effective_instagram_media_id` → obtém `effective_instagram_media_id`
3. `GET /{media_id}?fields=permalink` → obtém `permalink`

Se qualquer step retornar vazio, omitir a linha de link.

### Step 5: Obter saldo da conta (apenas relatório mensal)

**Endpoint**: `GET /act_{id}?fields=funding_source_details,spend_cap,amount_spent`

- `funding_source_details.type == 1` → Cartão de crédito (sem saldo pré-pago) → display "💳 Cartão de crédito"
- `funding_source_details.type == 20` → Saldo pré-pago → extrair valor com regex `R\$\s*([\d.,]+)` de `display_string`

### Step 6: Processar splits por unidade

Algumas contas gerenciam múltiplas unidades na mesma conta de anúncios. O script detecta automaticamente a unidade pelo nome da campanha e gera relatórios **separados por unidade**.

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
- Campanhas com `[CAJAMAR]` → relatório Cajamar
- Campanhas com "Cajamar e Jundiaí" → divididas 50/50 entre as duas unidades
- Cada unidade recebe seu próprio relatório com métricas e TOP 5 separados
- O greeting usa `DISPLAY_NAMES` dict, não o nome da unidade. Ex: "Olá Luana Sampaio — UNIDADE JUNDIAÍ!"

### Step 7: Adaptar por objetivo de campanha

- **OUTCOME_ENGAGEMENT**: Mensagens como KPI principal
- **OUTCOME_AWARENESS**: Alcance e impressões como KPI principal
- **OUTCOME_SALES**: Conversões/compras como KPI principal
- Se múltiplas campanhas com objetivos diferentes, segregar o relatório por objetivo

### Step 8: Relatório comparativo por categoria de conjunto (quando solicitado)

Quando o cliente pede comparação entre categorias (ex: "facial vs corporal"), agrupar conjuntos de anúncios pelo marcador no nome:

1. **Identificar categorias** — escanear nomes de ad sets por palavras-chave: `[FACIAL]`, `[CORPORAL]`, `[CORP]`, etc.
2. **Agrupar métricas** — somar impressões, gasto, mensagens por categoria
3. **Calcular CPA ponderado** — `gasto_total / mensagens_total` por categoria
4. **Formato de saída** — tabela por categoria com subtotais, seguida de análise comparativa:
   - Melhor CPA individual
   - Melhor CTR
   - Recomendação de realocação de orçamento (tirar do pior CPA, jogar no melhor)
5. **Excluir conjuntos de awareness** da comparação de CPA — eles não otimizam pra mensagem, CPA alto é esperado. Listá-los separados como "Outros".

---

## Output Format

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

### Formatação Brasileira
- Números: 1.234,56 (ponto para milhar, vírgula para decimal)
- Moeda: R$ 1.234,56
- Porcentagem: 0,56%

### Geração de PDF (quando solicitado)

Usar **Puppeteer (Node.js)** — `fpdf2`/`reportlab` Python não estão disponíveis no container.

1. Criar HTML profissional (ver `templates/relatorio-template.html`)
2. Renderizar com `node /opt/data/skills/flux/flux-meta-ads-relatorio/scripts/render_pdf.js <input.html> <output.pdf>`
3. Enviar via `MEDIA:/path/to/file.pdf`

**Design patterns para PDF:**
- Capa: gradiente temático, nome, período, métricas resumidas, `page-break-after: always`
- Métricas: grid de cards com `.metrics-grid` (CSS Grid auto-fit)
- Ranking: tabela com badges (🏆🥈🥉) e links Instagram
- Insights: box com borda lateral colorida (`.insight-box`)
- Rodapé: nome da agência, data de geração
- Font: Inter (Google Fonts CDN) — fallback sans-serif
- Print CSS: `-webkit-print-color-adjust: exact` + `print-color-adjust: exact`
- Proton tem 2 conjuntos ativos → gerar PDFs **separados** (PROMO MAIO e Advantage+)

---

## Common Mistakes

| Erro | Causa | Correção |
|------|-------|----------|
| `engagement_rate_unified` usado como field | Não é válido para a Insights API | Calcular manualmente: `page_engagement / impressions * 100` |
| `date_preset="last_30d"` causa erro de validação | `date_preset` só aceita valores fixos (`today`, `yesterday`, `this_week`, `last_week`, `this_month`, `last_month`, `this_quarter`, `last_quarter`, `this_year`, `last_year`, `lifetime`) | Usar `last_month` para ~30 dias, ou `time_range` com datas explícitas para períodos customizados |
| MCP Meta Ads fica "unreachable" durante queries em lote | Servidor MCP tem rate limit — 3 falhas consecutivas bloqueiam o endpoint | Usar `mcp_meta_ads_list_resources` como health check (rota alternativa); aguardar 5-60s para auto-recovery; alternar para `time_range` em vez de `date_preset` se precisar contornar |
| `OAuthException` ao chamar Graph API | `curl()` helper duplica `access_token` na URL | Usar padrão `api()`: build params dict, url-encode, append `&access_token=` uma única vez |
| Saldo errado exibido no relatório | `balance` do MCP é saldo contábil, não disponível | Usar `funding_source_details.display_string` via Graph API direta |
| `time_range` causa erro 400 | Não foi URL-encoded | Usar `urllib.parse.urlencode({"time_range": json.dumps({...})})`, nunca string manual |
| Links Instagram quebrados ou ausentes | Uma das 3 chamadas retornou vazio | Verificar cada step da chain (`ad_id → creative.id → effective_instagram_media_id → permalink`); omitir se qualquer step falhar |
| "Mensagem" aparece zerada em conta de vendas | Contas OUTCOME_SALES não têm métricas de messaging | Pular linhas de "Mensagem" quando `msgs == 0` |
| Saldo pré-pago mostra número errado | `funding_source_details.type == 1` (cartão) não tem `display_string` | Exibir "💳 Cartão de crédito" para type=1; só extrair valor de type=20 |
| Relatório de conta nova sai sem split de unidades | Config `UNIT_SPLIT` não foi atualizada no script | Adicionar entrada em `UNIT_SPLIT` antes de gerar relatório da conta |
| Emojis quebram envio via `curl` no terminal | Security scanner bloqueia variation selectors | Usar Python `subprocess` + `json.dumps(payload)` para postar no Telegram |
| PDF não renderiza gradientes | Puppeteer em container não aplica cores por padrão | Flags `--no-sandbox --disable-setuid-sandbox` + CSS `print-color-adjust: exact` |
| Métrica de "conversas" usa campo errado | `onsite_conversion.total_messaging_connection` conta conexões automáticas, não conversas reais | Para "conversas iniciadas" (o que o cliente enxerga), usar `onsite_conversion.messaging_conversation_started_7d` dentro de `actions[]`; CPA de conversa = `spend / messaging_conversation_started_7d` |

---

## Task-Specific Questions

1. O cliente tem arquivo de contexto em `contexts/`? Se não, quais display names e objetivos usar?
2. Relatório semanal ou mensal? (afeta período, inclusão de saldo, e threshold de spend)
3. Alguma conta com split de unidade que precisa de config nova no `UNIT_SPLIT`?
4. Quais contas tiveram `spend == 0` no período e devem ser puladas?
5. Cliente prefere texto WhatsApp ou PDF profissional?
6. Para relatório mensal: há alguma conta com saldo crítico (< 3 dias) que precisa de alerta extra?

---

## Tool Integrations

| Ferramenta | Uso | Método | Guide |
|------------|-----|--------|-------|
| `mcp_meta_ads_get_insights` | Métricas gerais da conta (impressões, alcance, cliques, spend) | MCP | `/opt/data/skills/flux/flux-meta-ads-relatorio/references/graph-api-quirks.md` |
| `mcp_meta_ads_get_campaign_performance` | Performance de campanhas e criativos (TOP 5) | MCP | `/opt/data/skills/flux/flux-meta-ads-relatorio/references/graph-api-quirks.md` |
| Graph API (direta) | Saldo real (`funding_source_details`) + links Instagram (3-step chain) | HTTP + token de `/opt/data/.env` | Ver seção "Métricas e Fontes" acima |
| `scripts/gerar-relatorio.py` | Automação completa: coleta métricas, TOP 5, links, formatação | CLI (`--semanal`/`--mensal`) | `/opt/data/skills/flux/flux-meta-ads-relatorio/scripts/gerar-relatorio.py` |
| `scripts/render_pdf.js` | Conversão HTML → PDF profissional via Puppeteer | CLI: `node render_pdf.js <in.html> <out.pdf>` | `/opt/data/skills/flux/flux-meta-ads-relatorio/scripts/render_pdf.js` |
| Cron (Hermes) | Agendamento: semanal `dec95f276e29`, mensal `606f71c16a63` | Cron jobs do Hermes Agent | Ambos entregam em `telegram:1212203404` |

---

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
- CA - Atual Luana → Luana Sampaio
- CA - Borgatteprincipal → BORGATTE
- CA - Taciana → TACIANA
- CA - Thabata Camargo → THABATA CAMARGO
- KORP NUTRA → KORP NUTRA

---

## Related Skills

- **flux-agency-standards**: Template canônico, tools registry e product-marketing-context — base para todas as skills Flux
- **flux-meta-ads-balance-alert**: Alerta diário de saldo — compartilha token, lista de contas e `DISPLAY_NAMES`. Se relatório mensal detectar saldo crítico, delegar o alerta para esta skill
- **flux-ads-audit**: Auditoria completa de anúncios — complementa o relatório com análise qualitativa de criativos e targeting
