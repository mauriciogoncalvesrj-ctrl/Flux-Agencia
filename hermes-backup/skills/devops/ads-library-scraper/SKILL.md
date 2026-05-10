---
name: ads-library-scraper
description: Scrape Meta Ads Library (and other ad transparency tools) using Camofox stealth browser to build a competitive ad database for aesthetic clinics. Collects ad copy, images, CTAs, formats, and performance indicators. Uses Camofox MCP tools (46 tools) for anti-detection browsing.
triggers:
  - scrape ads
  - ads library
  - competitor ads
  - ad intelligence
  - competitive ads
  - meta ads library
  - biblioteca de anúncios
  - anúncios concorrentes
---

# Ads Library Scraper — Competitive Ad Intelligence

## Overview

Uses Camofox (stealth browser with Cloudflare/bot bypass) to scrape ad transparency databases and build a competitive intelligence database for Agência Flux's aesthetic clinic clients.

## Architecture

```
Camofox Browser (port 9377)
    │
    ├── browse Meta Ads Library
    ├── browse Google Ads Transparency
    ├── browse TikTok Ads Library
    ├── extract structured data (copy, CTA, format)
    ├── screenshot ads for reference
    │
    └── Save to /opt/data/ads-intelligence/
        ├── YYYY-MM-DD/
        │   ├── clinic-name/
        │   │   ├── metadata.json (structured data)
        │   │   ├── screenshots/
        │   │   └── transcripts/
```

## Camofox MCP Tools Available (46 total)

Key tools for ad scraping:

| Tool | Purpose |
|------|---------|
| `camofox_create_tab` | Open new browser tab |
| `camofox_navigate` | Navigate to URL |
| `camofox_snapshot` | Get accessibility tree (90% smaller than HTML) |
| `camofox_screenshot` | Capture screenshot of page/element |
| `camofox_click` | Click element by ref |
| `camofox_type` | Type text into input fields |
| `camofox_scroll` | Scroll page down/up |
| `camofox_extract` | Extract structured data with JSON Schema |
| `camofox_import_cookies` | Import authenticated session cookies |
| `camofox_list_tabs` | List all open tabs |
| `camofox_close_tab` | Close a tab |

### Search Macros (built-in)

| Macro | Site |
|-------|------|
| `@google_search` | Google search |
| `@youtube_search` | YouTube search |
| `@reddit_subreddit` | Reddit subreddit |

## Scraping Targets

### 1. Meta Ads Library (Primary)

**URL:** `https://www.facebook.com/ads/library/`

**Search terms for aesthetic clinics:**
- "harmonização facial"
- "peeling químico"
- "botox clínica"
- "preenchimento labial"
- "estética clínica"
- "dermapen"
- "criolipólise"
- "radiofrequência"

**Extract per ad:**
- Ad copy (headline, body text, CTA)
- Creative type (image, video, carousel)
- Page name and URL
- Start date and active status
- Screenshot of the creative
- Link destination URL

### 2. Google Ads Transparency

**URL:** `https://adstransparency.google.com/`

**Search by:** Advertiser name or URL

### 3. TikTok Ads Library

**URL:** `https://library.tiktok.com/ads/`

## Scraping Workflow

### Step 1: Create Session

```
Create tab with userId="flux" and sessionKey="ads-library"
Navigate to https://www.facebook.com/ads/library/
```

### Step 2: Search and Filter

```
Type search term (e.g., "harmonização facial")
Apply filters: Country=Brasil, Category=Todos, Active ads only
```

### Step 3: Extract Ad Data

```
For each ad card:
  1. Click on ad card
  2. Take screenshot
  3. Extract structured data via camofox_extract
  4. Save metadata + screenshot path
  5. Close ad detail
  6. Scroll to next ad
```

### Step 4: Save to Database

```
Save to /opt/data/ads-intelligence/YYYY-MM-DD/clinic-name/
  - metadata.json (all extracted data)
  - screenshot-ad-N.png
  - summary.md (human-readable summary)
```

## Data Structure (metadata.json)

```json
{
  "scrape_date": "2026-05-10",
  "source": "meta_ads_library",
  "search_term": "harmonização facial",
  "country": "BR",
  "ads": [
    {
      "ad_id": "123456789",
      "page_name": "Clínica Exemplo",
      "page_url": "https://facebook.com/clinicaexemplo",
      "headline": "Harmonização Facial - Resultado Natural",
      "body_text": "Agende sua avaliação...",
      "cta_type": "Agende Agora",
      "creative_type": "carousel",
      "creative_count": 4,
      "destination_url": "https://clinicaexemplo.com.br/whatsapp",
      "start_date": "2026-04-15",
      "is_active": true,
      "screenshot_path": "screenshots/ad-123456789.png",
      "tags": ["harmonização", "facial", "natural", "carousel", "whatsapp-cta"]
    }
  ]
}
```

## Tags Classification

**Procedure tags:** harmonização, botox, preenchimento, peeling, dermapen, criolipólise, radiofrequência, microagulhamento, rinomodelação, skinbooster

**Format tags:** carousel, single-image, video, stories, reel

**CTA tags:** agende, whatsapp, saiba-mais, ligar, comprar

**Emotion tags:** antes-depois, depoimento, promoção, urgência, resultado

## Cron Job (Future)

Weekly scrape of top competitors:
- Monday 8:00 UTC — full competitor scan
- Save results to /opt/data/ads-intelligence/
- Generate summary report for pipeline

## Pitfalls

- Meta Ads Library has anti-scraping measures — Camofox bypasses most
- Rate limiting: add 3-5 second delays between page navigations
- Some ads require login to see full details — use cookie import
- TikTok Ads Library changes DOM frequently — may need selector updates
- Never scrape personal data or medical records — only public ad creative
- Keep screenshots organized by date for trend analysis
- The Camofox API requires `userId` and `sessionKey` for all tab operations
- Use `userId="flux"` and `sessionKey="default"` for our sessions