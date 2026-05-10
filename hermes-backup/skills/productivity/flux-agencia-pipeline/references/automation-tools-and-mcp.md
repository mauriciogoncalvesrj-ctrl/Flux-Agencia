# Automation Tools & MCP Integration Roadmap

## MCP Servers (Configured in Hermes)

### meta-ads (pipeboard-co/meta-ads-mcp ⭐881)
- **29 tools**: campaign CRUD, ad sets, creatives, image upload, insights, targeting (interests, behaviors, demographics, geolocations), budget schedules
- **Local mode**: `npx -y meta-ads-mcp` with env `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID`
- **Remote mode**: `https://mcp.pipeboard.co/meta-ads-mcp` with Pipeboard API token
- **Security**: Audit score 0/100 (Issue #69). Use local mode for production. Campaign data is low-sensitivity but rotate tokens regularly.
- **Also supports**: Google Ads MCP (`mcp.pipeboard.co/google-ads-mcp`) and TikTok Ads MCP (`mcp.pipeboard.co/tiktok-ads-mcp`)
- **Setup**: Create Meta Developer App → OAuth → long-lived token; OR use Pipeboard for zero-config

### GHL / GoHighLevel (mastanley13/GoHighLevel-MCP ⭐163)
- **163+ tools**: contacts, pipelines, opportunities, automations, conversations, tags, custom fields
- **Local mode**: `npx -y gohighlevel-mcp` with env `GHL_API_KEY`
- **Setup**: Generate API key in GHL sub-account settings

### n8n (leonardsellem/n8n-mcp-server ⭐1618)
- **Orchestrator**: Create, edit, execute automated workflows
- **Use cases**: approval pipelines, auto-posting, webhook management, multi-step automation
- **Local mode**: `npx -y n8n-mcp-server` with env `N8N_API_URL` and `N8N_API_KEY`
- **Setup**: Install n8n on VPS first, then configure MCP

## Additional MCP Servers (Not Yet Configured)

### google-meta-ads-ga4 (irinabuht12-oss ⭐928)
- Combined Google Ads + Meta Ads + Google Analytics
- Good for cross-platform reporting

### ig-mcp (jlbadano ⭐125)
- Instagram Business account management
- Media publishing, insights, comments

## Image & Video Generation Stack

### AI Image Generation
- **FLUX.1-dev** via fal.ai API — best quality for clinic imagery (recommended)
- **ComfyUI** (self-hosted) — full control, requires GPU
- **Stability AI API** — pay-per-use, good for production without self-hosting
- **Ideogram API** — strong at text-in-image (quote cards, promotional graphics)
- **Bannerbear API** — carousel-first, brand templates, scale-friendly (recommended for carousels)

### Video Generation
- **Replicate** (AnimateDiff, CogVideoX) — short clips for Reels
- **Runway ML Gen-3** — best quality, credits-based
- **CapCut Enterprise API** — trending templates, auto-captioning

### Auto-Posting
- **Meta Graph API** (direct) — Instagram Business posts, carousels
- **Buffer API** — scheduling across platforms
- **Hootsuite API** — enterprise-grade, robust

## Integration Priority Roadmap

1. **IMMEDIATE**: Configure META_ACCESS_TOKEN and META_AD_ACCOUNT_ID → activate meta-ads MCP
2. **WEEK 1**: Configure GHL_API_KEY → activate GHL MCP
3. **WEEK 2**: Install n8n on VPS → orchestrate workflows
4. **MONTH 1**: Set up image generation pipeline (Bannerbear or custom Pillow)
5. **MONTH 2**: Configure auto-posting via Meta Graph API or Buffer