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