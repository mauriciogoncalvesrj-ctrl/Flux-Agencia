# Meta Ads MCP Server — Setup & Security Reference

> Research date: 2026-05-09

## Overview

The **pipeboard-co/meta-ads-mcp** (⭐881) is the most popular MCP server for managing Facebook/Instagram Ads programmatically. It provides 29 tools for campaign creation, management, insights, targeting, and creative upload.

**GitHub**: https://github.com/pipeboard-co/meta-ads-mcp  
**NPM package**: `meta-ads-mcp`  
**License**: BSL 1.1 (becomes Apache 2.0 on 2029-01-01)  
**License holder**: ARTELL SOLUÇÕES TECNOLÓGICAS LTDA (Brazil)

## Two Setup Paths

### Path A: Remote MCP via Pipeboard (Easiest)

No local setup required. Authenticate through Pipeboard's cloud service.

```yaml
# Hermes config.yaml
mcp_servers:
  meta-ads:
    url: "https://mcp.pipeboard.co/meta-ads-mcp"
    headers:
      Authorization: "Bearer YOUR_PIPEBOARD_TOKEN"
    timeout: 120
```

Steps:
1. Create account at https://pipeboard.co
2. Connect Facebook Ads account
3. Generate API token at https://pipeboard.co/api-tokens
4. Add to Hermes config as HTTP MCP server

Also available: Google Ads (`google-ads-mcp`) and TikTok Ads (`tiktok-ads-mcp`).

### Path B: Local Installation (Most Secure)

Runs on your own infrastructure. Tokens stay local. Requires Meta Developer App.

```yaml
# Hermes config.yaml
mcp_servers:
  meta-ads:
    command: "npx"
    args: ["-y", "meta-ads-mcp"]
    env:
      META_ACCESS_TOKEN: "${META_ACCESS_TOKEN}"
      META_AD_ACCOUNT_ID: "${META_AD_ACCOUNT_ID}"
    timeout: 120
    connect_timeout: 60
```

Requires:
- Meta Developer App with Marketing API permissions
- `META_ACCESS_TOKEN` — long-lived token from OAuth flow
- `META_AD_ACCOUNT_ID` — format: `act_XXXXXXXXX`

## Available Tools (29)

### Account Management
- `mcp_meta_ads_get_ad_accounts` — List accessible ad accounts
- `mcp_meta_ads_get_account_info` — Get account details
- `mcp_meta_ads_get_account_pages` — List pages for an account

### Campaigns
- `mcp_meta_ads_get_campaigns` — List campaigns with filtering
- `mcp_meta_ads_get_campaign_details` — Campaign details
- `mcp_meta_ads_create_campaign` — Create new campaign (objectives: OUTCOME_AWARENESS, OUTCOME_TRAFFIC, OUTCOME_ENGAGEMENT, OUTCOME_LEADS, OUTCOME_SALES, OUTCOME_APP_PROMOTION)

### Ad Sets
- `mcp_meta_ads_get_adsets` — List ad sets
- `mcp_meta_ads_get_adset_details` — Ad set details
- `mcp_meta_ads_create_adset` — Create ad set with targeting, budget, schedule
- `mcp_meta_ads_update_adset` — Update targeting, budget, frequency caps, status

### Ads & Creatives
- `mcp_meta_ads_get_ads` — List ads
- `mcp_meta_ads_get_ad_details` — Ad details
- `mcp_meta_ads_create_ad` — Create ad with existing creative
- `mcp_meta_ads_update_ad` — Update ad status, bid amount
- `mcp_meta_ads_get_ad_creatives` — Get creative details
- `mcp_meta_ads_create_ad_creative` — Create new creative (supports dynamic creative with multiple headlines/descriptions for A/B testing)
- `mcp_meta_ads_update_ad_creative` — Update creative content
- `mcp_meta_ads_upload_ad_image` — Upload image for use in creatives
- `mcp_meta_ads_get_ad_image` — Download and visualize ad image

### Insights & Analytics
- `mcp_meta_ads_get_insights` — Performance metrics for campaigns/ad sets/ads
  - Supports breakdown by age, gender, country
  - Supports attribution windows (1d_click, 7d_click, etc.)
  - Levels: ad, adset, campaign, account

### Targeting
- `mcp_meta_ads_search_interests` — Search interest targeting by keyword
- `mcp_meta_ads_get_interest_suggestions` — Get suggestions based on existing interests
- `mcp_meta_ads_validate_interests` — Validate interest names/IDs
- `mcp_meta_ads_search_behaviors` — Get behavior targeting options
- `mcp_meta_ads_search_demographics` — Get demographic targeting options
- `mcp_meta_ads_search_geo_locations` — Search geographic targeting

### Budget & Scheduling
- `mcp_meta_ads_create_budget_schedule` — Schedule budget changes (absolute or multiplier)
- `mcp_meta_ads_get_login_link` — Get Meta auth login link

### Search
- `mcp_meta_ads_search` — Generic search across accounts, campaigns, ads, pages

## Security Assessment (2026-05-09)

### Issue: Security Audit Score 0/100 (Issue #69)

An external automated scan (AgentsID Scanner) found 167 findings:
- **Critical**: Data exfiltration paths (server can relay data externally, access credentials and send externally)
- **Critical**: Injection bypass in `create_ad_creative` and `get_insights` tool descriptions
- **High**: 13 tools expose credential access patterns
- **Categories**: data-flow: F, injection: F, permissions: F, validation: F, secrets: F, output: A

### Implications for Agência Flux Use

**Low-risk for our use case** because:
- We manage ad campaigns (public data), not sensitive personal/financial data
- Meta Ads tokens are scoped to ad accounts only, not full Facebook access
- Auth scope: `business_management, public_profile, pages_show_list, pages_read_engagement`

**Still recommended: Local installation** (Path B) to keep tokens on our VPS rather than passing through a third-party cloud service.

### Risk Mitigation
- Use long-lived tokens with minimum required permissions
- Rotate tokens regularly
- Monitor token usage in Meta Business Manager
- Consider creating a dedicated Meta System User (not personal account) for API access