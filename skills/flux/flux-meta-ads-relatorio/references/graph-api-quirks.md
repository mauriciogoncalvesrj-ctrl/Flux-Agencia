# Graph API Quirks & Pitfalls — Meta Ads

## API Endpoints

### Account-level insights
```
GET /act_{id}/insights?time_range={"since":"2026-05-04","until":"2026-05-10"}&fields=impressions,reach,clicks,spend,ctr,actions,cost_per_action_type&level=account
```

### Ad-level insights (for TOP 5)
```
GET /act_{id}/insights?time_range={"since":"2026-05-04","until":"2026-05-10"}&fields=ad_name,ad_id,campaign_name,impressions,spend,ctr,actions,cost_per_action_type&level=ad&limit=50
```

### Campaign-level insights (for unit splitting)
```
GET /act_{id}/insights?time_range=...&fields=campaign_name,campaign_id,objective,impressions,reach,clicks,spend,ctr,actions,cost_per_action_type&level=campaign&limit=20
```

### Instagram permalink (3 chained calls)
1. `GET /{ad_id}?fields=creative{id}`
2. `GET /{creative_id}?fields=effective_instagram_media_id`
3. `GET /{media_id}?fields=permalink`
- If any step returns empty, omit the link.

### Account balance (real spending power)
```
GET /act_{id}?fields=funding_source_details,spend_cap,amount_spent,currency
```
- `funding_source_details.type == 1` → Credit card (no prepaid balance)
- `funding_source_details.type == 20` → Prepaid balance
- Extract from `display_string` with regex `R\$\s*([\d.,]+)`

## Conversation Metrics (Critical Distinction)

The `actions[]` array in insights responses contains multiple messaging metrics. **Use the right one:**

| Campo | O que conta | Quando usar |
|-------|------------|-------------|
| `onsite_conversion.total_messaging_connection` | Todas as conexões de messaging (inclui respostas automáticas, saudações, etc.) | Métrica genérica "mensagens" |
| `onsite_conversion.messaging_conversation_started_7d` | Conversas **reais** iniciadas em até 7 dias | **CPA de conversa** — é o que o cliente enxerga como "conversa" |
| `onsite_conversion.messaging_first_reply` | Primeiras respostas do negócio | Taxa de resposta do atendimento |
| `onsite_conversion.messaging_user_depth_3_message_send` | Conversas com 3+ mensagens do usuário | Engajamento profundo |

Para relatórios de performance de anúncios, o CPA mais relevante é: `spend / messaging_conversation_started_7d`.

**Extrair do JSON de actions:**
```python
conv_7d = next((a["value"] for a in actions if a["action_type"] == "onsite_conversion.messaging_conversation_started_7d"), 0)
```

## MCP `date_preset` — Valid Values

The `date_preset` parameter ONLY accepts these exact enum values:
- `today`, `yesterday`
- `this_week`, `last_week`
- `this_month`, `last_month`
- `this_quarter`, `last_quarter`
- `this_year`, `last_year`
- `lifetime`

❌ `last_30d` — NOT valid. Causes: `Input validation error: Invalid enum value`
✅ `last_month` — works as ~30 days alternative
✅ `time_range` with explicit dates — more flexible, more reliable

## MCP Server Resilience

The Meta Ads MCP server has rate limits. Pattern when it fails:

1. **Symptom**: `MCP server 'meta-ads' is unreachable after 3 consecutive failures`
2. **Root cause**: Rate limit or transient connection issue — not a server crash
3. **Recovery pattern**:
   - **Do NOT retry** the same tool immediately (error says "Auto-retry in ~N seconds")
   - Use `mcp_meta_ads_list_resources` as a **health probe** — it uses a different endpoint and often succeeds even when `get_insights` is throttled
   - Wait 5-60 seconds for auto-recovery
   - When server returns, prefer `time_range` over `date_preset` (different code path, more stable)
4. **Prevention**: 
   - Don't fire 8+ `get_insights` calls in parallel — batch into groups of 3-4
   - Stagger calls by 1-2 seconds between batches
   - If doing ad-level reports with many ads, query in sequential batches

## Pitfalls

1. **NEVER use `engagement_rate_unified`** — not a valid field for insights API. Compute manually: `page_engagement / impressions * 100`.

2. **NEVER double-append access_token** — if using a URL builder that already includes `?access_token=`, don't add `&access_token=` again. Causes OAuthException.

3. **time_range must be URL-encoded** — use `urllib.parse.urlencode({"time_range": json.dumps({"since": "...", "until": "..."})})`, not manual string concatenation.

4. **`balance` field from get_ad_accounts is misleading** — it's the accounting balance, not the actual spending power. Always use `funding_source_details.display_string`.

5. **Instagram permalinks require 3 API calls** — ad → creative → media_id → permalink. Each can return empty.

6. **OUTCOME_SALES accounts (e.g. KORP NUTRA)** have messaging_conversions = 0. Skip "Mensagem" lines when `msgs == 0`.

7. **Unit splitting requires campaign-level insights** — the script needs `level=campaign` with `campaign_name` field to detect unit tags like `[JUNDIAI]` and `[CAJAMAR]`.

8. **Shared campaigns** (e.g., "Cajamar e Jundiaí") are split 50/50 across the tagged units. This is a simplification — if the user wants exact attribution, campaign-level ad attribution would be needed.

9. **Formatting: always Brazilian** — `1.234,56` for numbers, `R$ 1.234,56` for currency, `0,56%` for percentages. The `fmt_brl()` and `fmt_int()` helpers handle this.

10. **`date_preset="last_30d"` fails validation** — only accepts fixed enum values (see table above). Use `last_month` or `time_range` with explicit dates instead.

11. **MCP server becomes unreachable mid-report** — rate limit after 3+ failed calls. Probe with `list_resources`, wait 5-60s, then retry with staggered batches of 3-4 calls max.