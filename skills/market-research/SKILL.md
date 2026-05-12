---
name: market-research
description: "Deep market research and competitive intelligence for Flux Agency. Maps competitors (direct and indirect), analyzes successful cases, identifies software ecosystems, builds buyer personas, and generates ready-to-use campaigns. Use when the user says research market, competitor mapping, market analysis, niche research, espionage, or wants to understand a specific industry for Flux's positioning."
user-invokable: true
---

<!-- Updated: 2026-05-12 | v1.0 -->

# Market Research for Flux Agency

## Objective
Map a market niche deeply to identify:
1. Direct competitors (agencies, traffic managers)
2. Indirect competitors (mentorships, consultancies, courses)
3. Success cases (real clients with public data)
4. Software/tool ecosystem
5. Buyer persona (demographics, pains, desires, buying layers)
6. Market gaps and opportunities for Flux
7. Ready-to-use campaign concepts

## Process

### Phase 1: Intelligence Gathering
1. **Web search** for top agencies/players in the niche
2. **Meta Ad Library** analysis (if accessible)
3. **Google Ads Transparency Center** (if accessible)
4. **Competitor website** analysis (promises, pricing, positioning)
5. **Case study** collection from agency blogs/portfolios

### Phase 2: Ecosystem Mapping
1. Map mentorships and courses (indirect competitors)
2. Map software/CRMs/tools used by the target audience
3. Identify influencers/thought leaders in the niche

### Phase 3: Persona Building
1. Demographics (age, gender, profession, revenue, city size)
2. Top 10 pains
3. Top 7 desires
4. Buying ecosystem (5 layers of purchase)

### Phase 4: Gap Analysis
1. What NO competitor offers (Flux opportunity)
2. Pricing gaps (mentorships expensive but don't execute; agencies cheap but don't automate)
3. Positioning gaps (no one speaks as "owner to owner")
4. Content gaps (no one offers structured free diagnosis)

### Phase 5: Campaign Creation
1. Central concept
2. 5 copy angles
3. Carousel script (8-10 slides)
4. Reel script (30s)
5. WhatsApp follow-up sequence
6. Weekly content matrix

### Phase 6: Documentation
1. Generate report using template: `docs/pesquisas/template-pesquisa.md`
2. Save with naming: `YYYY-MM-DD-CODE-topic.md`
3. Update `docs/pesquisas/README.md` index
4. Commit to GitHub

## Output Structure

Each research generates:
- `docs/pesquisas/YYYY-MM-DD-CODE-topic.md` (full report)
- Campaign concepts ready for production
- Content matrix for 30 days
- Persona card
- Competitor comparison table

## Data Sources

| Source | What You Can Find | How to Access |
|--------|------------------|---------------|
| Google Search | Agency rankings, cases, mentorships | `WebSearch` tool |
| Meta Ad Library | Active ads from competitors | https://www.facebook.com/ads/library |
| Agency Websites | Pricing, positioning, services | `WebFetch` tool |
| Case Blogs | ROAS, investment, results | Search "case clinica estetica marketing" |
| Software Sites | CRM pricing, features | Search "CRM clinica estetica WhatsApp" |

## Competitive Analysis Framework

For each competitor, document:
- **Positioning:** How they describe themselves
- **Promise:** What result they guarantee
- **Price:** Management fee + ad spend recommendation
- **Format:** Service, mentorship, course, software
- **Weakness:** What they DON'T offer (Flux opportunity)
- **Content:** What they post (if Instagram is public)

## Persona Template

```markdown
### Profile
- Age:
- Gender:
- Profession:
- Monthly revenue:
- City size:

### Top 10 Pains
1.
2.
...

### Top 7 Desires
1.
2.
...

### Buying Ecosystem (5 layers)
| Layer | Solutions | Typical Price |
|---|---|---|
| 1. Education | Courses, certifications | R$ 1-5k |
| 2. Mentorship | Business coaching | R$ 2-15k |
| 3. Traffic | Ad agencies | R$ 1-5k/mo |
| 4. Software | CRM, automation | R$ 100-400/mo |
| 5. Automation | Bots, funnels | R$ 500-2k/mo |
```

## Campaign Template

```markdown
### Campaign: [Name]
**Concept:**
**Angles:**
1. 
2. 
3. 
4. 
5. 

**Carousel Script:**
- Slide 1: Hook
- Slide 2-7: Content
- Slide 8: CTA

**Reel Script (30s):**
- 0-3s: Hook
- 3-10s: Problem
- 10-20s: Proof
- 20-30s: CTA

**WhatsApp Sequence:**
1. [Immediate] 
2. [24h later] 
3. [48h later] 
```

## Brand Rules (CRITICAL)
- NEVER mention "GHL", "GoHighLevel", "HighLevel", "Conversation AI" in client-facing materials
- Replace with: "Sistema Flux 360", "nosso sistema", "atendimento automatizado Flux"
- Position Flux as premium: R$ 1,500-6,500/month recurring
- Speak as "owner to owner", not "agency to client"
- Every post must trigger one of three reactions:
  1. "This is happening to me."
  2. "They understand exactly my clinic's problem."
  3. "I need to talk to this agency."

## References
- Research template: `docs/pesquisas/template-pesquisa.md`
- Research index: `docs/pesquisas/README.md`
- Example completed research: `docs/pesquisas/2026-05-12-b2b-estetica-flux.md`
