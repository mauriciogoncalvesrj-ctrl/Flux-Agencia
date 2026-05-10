# Meta Ads MCP — Setup Reference

## Quick Setup Options

### Option A: Local (Recommended for Production)

1. Create a Meta Developer App at developers.facebook.com
2. Add Marketing API product to your app
3. Configure OAuth redirect URL
4. Generate a long-lived access token with scopes:
   - `business_management`
   - `ads_management`
   - `ads_read`
   - `pages_show_list`
   - `pages_read_engagement`
   - `public_profile`
5. Get your Ad Account ID (act_XXXXXXXXX)
6. Add to Hermes config.yaml:
```yaml
mcp_servers:
  meta-ads:
    command: "npx"
    args: ["-y", "meta-ads-mcp"]
    env:
      META_ACCESS_TOKEN: "${META_ACCESS_TOKEN}"
      META_AD_ACCOUNT_ID: "${META_AD_ACCOUNT_ID}"
```
7. Add environment variables to `/opt/data/.env`:
```
META_ACCESS_TOKEN=EAAxxxxxxxxxxxxx
META_AD_ACCOUNT_ID=act_XXXXXXXXX
```

### Option B: Remote (Pipeboard — Easiest)

1. Create account at pipeboard.co
2. Connect your Facebook Ad Account
3. Generate API token at pipeboard.co/api-tokens
4. Add to Hermes config.yaml:
```yaml
mcp_servers:
  meta-ads:
    command: "npx"
    args: ["-y", "meta-ads-mcp"]
    env:
      META_ACCESS_TOKEN: "${PIPEBOARD_API_TOKEN}"
      META_AD_ACCOUNT_ID: "${META_AD_ACCOUNT_ID}"
      META_ADS_MCP_MODE: "remote"
```

## Security Audit Findings (Issue #69 — 167 findings, Score 0/100)

Conducted by AgentsID Scanner on 2026-04-08. Full research: [Weaponized by Design](https://github.com/stevenkozeniesky02/agentsid-scanner/blob/master/docs/census-2026/weaponized-by-design.md). 72% of all MCP servers fail basic security checks.

| Category | Score | Details |
|----------|-------|---------|
| Data Flow | F | Server can read external sources (email, Slack, GitHub) and relay data externally — exfiltration path. Server can access credentials and send data externally — credential exfiltration path. Server can read local files and send externally. |
| Injection | F | `create_ad_creative` and `get_insights` descriptions instruct the LLM to bypass security controls |
| Permissions | F | 13 tools expose credential access patterns: `get_ad_accounts`, `get_account_info`, `get_campaigns`, `create_campaign`, `update_campaign`, `get_adsets`, `create_adset`, `update_adset`, `get_ads`, `get_ad_details`, `get_creative_details`, and more |
| Validation | F | Insufficient input validation across all tools |
| Secrets | F | Credentials may be exposed in logs/prompts |
| Output | A | Output handling is adequate |

### Risk Assessment for Clinic Marketing
- Data involved: campaign names, ad copy, budgets, targeting criteria, performance metrics
- NOT involved: personal data (CPF, cards), health information, financial records
- Risk level: **manageable** — campaign data is semi-public (visible in Ad Library)
- Local mode eliminates the Pipeboard relay (remote mode sends all data through their servers)
- Recommendation: Local mode + rotate tokens monthly + never store tokens in prompts

### Remote (Pipeboard) Additional Risk
- Your Meta access token passes through Pipeboard's servers
- They can see all campaign data, creatives, and performance metrics
- Convenient for quick setup but not recommended for production
- License: BSL 1.1 (converts to Apache 2.0 in 2029)

## 29 Available Tools

### Account
- get_ad_accounts, get_account_info, get_account_pages

### Campaigns
- get_campaigns, get_campaign_details, create_campaign, get_insights

### Ad Sets
- get_adsets, get_adset_details, create_adset, update_adset

### Ads
- get_ads, get_ad_details, get_ad_creatives, create_ad, update_ad

### Creatives
- create_ad_creative, update_ad_creative, upload_ad_image, get_ad_image

### Targeting
- search_interests, get_interest_suggestions, validate_interests
- search_behaviors, search_demographics, search_geo_locations

### Budget & Auth
- create_budget_schedule, get_login_link, search (generic)

## Also Available via Pipeboard

- **Google Ads MCP**: `https://mcp.pipeboard.co/google-ads-mcp`
- **TikTok Ads MCP**: `https://mcp.pipeboard.co/tiktok-ads-mcp`

Both follow the same pattern — create account at pipeboard.co, connect ad accounts, generate API token.