---
name: ghl-conversation-audit
description: "Audit AI bot conversations in GoHighLevel (GHL) CRM to identify performance gaps, script failures, persona inconsistencies, and engagement problems. Produces actionable remediation plans for chatbot optimization. Applies to any GHL WhatsApp/SMS automation (Stevo, native GHL bot, third-party integrations)."
version: 1.0.0
metadata:
  hermes:
    tags: [ghl, crm, bot-audit, conversation-analysis, ai-assessment, flux-agency]
    related_skills:
      - flux-orchestrator
      - ghl-mcp-server
      - flux-social-estetica
---

# GHL Conversation Audit — AI Bot Performance Review

**Purpose:** Systematically audit AI-generated conversations in GHL to find gaps, script failures, and optimization opportunities. Transform raw CRM conversation data into an actionable remediation report.

**When to use:**
- User asks to "audit bot conversations", "review AI messages", "find errors in attendimento", or analyze lead follow-up quality in GHL.
- Monthly/quarterly bot health checks for any AI-powered WhatsApp/SMS automation.
- Post-campaign debrief: assess whether the AI handled leads from a specific ad campaign.

**Pre-requisites:**
- GHL MCP server configured (`mcp_ghl_*` tools available).
- Knowledge of the bot's identity flags (e.g., `from: "stevo"`, `userId: "f2nFx5eiTyIjGqg7nVph"`).
- Location ID and conversation provider ID (WhatsApp integration).

---

## Methodology: 7-Step Audit Pipeline

### Step 1: Scope Definition
Define what to audit:
- **Tag filter:** e.g., `metaads`, `meta ads whatsapp` (or no filter for all).
- **Time window:** last 30/60 days.
- **Conversation depth:** fetch full `messages` array per conversation (not just summaries).
- **Sample size:** aim for 7–15 conversations (~50–100 messages) for statistical relevance.

### Step 2: Fetch Contacts
```
mcp_ghl_search_contacts(query="<tag>", limit=50)
```
Collect `contactId`, `phone`, `tags`, `fullName`.

### Step 3: Fetch Conversations
```
mcp_ghl_search_conversations(contactId="<id>", limit=50)
```
Each entry gives `conversationId`, `lastMessageBody`, `lastMessageDirection`.

### Step 4: Fetch Full Message History
```
mcp_ghl_get_conversation(conversationId="<id>", limit=50)
```
This returns the `messages[]` array with full metadata:
- `direction` (`inbound` / `outbound`)
- `source` (`api` = automation vs `app` = system activity)
- `from` (`stevo` / `Flux` / lead phone number)
- `userId` (AI bot user ID)
- `status` (`delivered`, `failed`, `read`)
- `body` (message text)
- `dateAdded` (timestamp)
- `error` (failure reason if any)
- `attachments` (audio, video, images)

### Step 5: Attribution Matrix (AI vs Human)

Use these heuristics to classify every message:

| Signal | Meaning | Confidence |
|--------|---------|------------|
| `source: "api"` + `direction: "outbound"` | Bot/automation message | HIGH |
| `from: "stevo"` | Bot service (STEVO app) | HIGH |
| `userId: "f2nFx5eiTyIjGqg7nVph"` | Known bot user ID | HIGH |
| `source: "app"` + `from: "Flux"` | System activity (opp created/updated) | MEDIUM — NOT a conversation message |
| `direction: "inbound"` + phone number in `from` | Lead human response | HIGH |
| Timing regularity (e.g., every 7 days at 13:03) | Bot schedule pattern | MEDIUM |

**System messages (`TYPE_ACTIVITY_OPPORTUNITY`, `source: "app"`) must be excluded from conversation quality analysis** — they are GHL workflow events, not dialogue.

### Step 6: Gap Analysis — 10 Failure Categories

For each conversation, score against these categories. A finding in ANY category flags the conversation.

#### Category A — Communication Failures
1. **Audio/Video Ignored:** Lead sends audio/video; bot responds with generic text ignoring the media.
   - *Detection:* `attachments` present on inbound + generic script response outbound.
   - *Example:* Lead sends audio; bot: *"Não consegui ouvir, como posso te chamar?"*

2. **Failed Delivery:** Outbound messages with `status: "failed"` or `error` field.
   - *Metric:* Calculate failure rate: `failed / total_outbound`.
   - *Action threshold:* > 5% failure rate = critical issue.

3. **Auto-Reply Misinterpretation:** Bot treats out-of-office/absence auto-replies as human engagement.
   - *Keywords to detect:* `"Não estamos disponíveis"`, `"Fora do escritório"`, `"Responderemos assim que possível"`

#### Category B — Intelligence Failures
4. **Script Linearity (Context Blindness):** Bot ignores lead's answer and continues the qualification script.
   - *Example:* Lead says *"Não tenho clínica"*; bot asks: *"Você é dona ou gestora da clínica?"*
   - *Severity:* CRITICAL — destroys trust.

5. **ICP Non-Detection:** Bot fails to recognize that lead is outside the target persona and should be disqualified/closing gracefully.
   - *Signals:* "Não tenho clínica", "Sou aluno", "Trabalho em outra área", student, competitor, job-seeker.
   - *Expected behavior:* Polite redirect or close, not continued qualification.

6. **Persona Inconsistency:** Same conversation switches persona names or tone.
   - *Examples:* "Maria" → "Sofia" → "Mauricio" within one thread.
   - *Expected behavior:* One fixed persona per lead, or generic brand persona.

#### Category C — Engagement Failures
7. **Broken Abandonment Promise:** Bot sends "this is my last message" but continues following up.
   - *Detection:* Count "última mensagem" phrases; check if any follow-up occurred afterward.
   - *Impact:* Reputational damage, spam classification.

8. **Predictable Timing:** Follow-ups at identical intervals (e.g., exactly every 7 days at 13:03).
   - *Detection:* Calculate delta between outbound timestamps; flag if variance < 30 minutes.
   - *Fix:* Randomize delay between 5–9 days, and time of day between 9h–18h.

9. **Weak/No CTA:** Qualification questions without a concrete next step.
   - *Example:* Asks "How much do you bill?" but never offers a call/demo/material.
   - *Expected:* After any qualifying answer, immediately propose: *"Quer agendar uma call de 15 min para eu mostrar?"*

10. **Creative/Ad Mismatch:** Bot ignores the ad/creative the lead clicked on.
    - *Detection:* Analyze `ctwaPayload` / `Source URL` in first inbound message; compare to bot's opening script.
    - *Expected:* Reference the ad's hook in the first response: *"Você viu que respondemos leads em 30 segundos? Quer saber como?"*

### Step 7: Remediation Report

Structure the output as:

```
## 📊 Audit Summary — [Bot Name] @ [Date]
- Conversations audited: X
- Messages analyzed: Y
- Lead response rate: Z%
- Delivery failure rate: W%

## 🚨 Critical Gaps (P1)
[Categories A+B with examples and counts]

## ⚠️ Medium Gaps (P2)
[Categories C with examples and counts]

## 🛠 Recommended Actions Table
| Priority | Action | Impact | Owner |

## 💡 Insight Chave
[One-paragraph strategic takeaway]
```

---

## Pitfalls

| Pitfall | Why it happens | Prevention |
|---------|----------------|------------|
| Confusing system activity with conversation | `Opportunity updated` messages appear in timeline | Always filter by `type !== 28` or `source !== "app"` for dialogue analysis |
| Trusting `lastMessageBody` only | It hides the full flow | Always fetch `messages[]` via `mcp_ghl_get_conversation` |
| Not checking `error` field | Failed messages look like delivered ones | Always include `status` and `error` in the analysis loop |
| Treating all outbound as bot | Manual messages from humans also appear outbound | Cross-reference `userId` against known bot IDs; manual messages may have `source: "manual"` |
| Small sample = false confidence | Analyzing 2 conversations is not representative | Minimum 7 conversations or 50 messages before drawing trends |

---

## Verification Script

After applying fixes, re-audit the same conversations:
1. Re-fetch conversations.
2. Check if previously flagged failures reoccur.
3. Measure: response rate uplift, failure rate reduction, persona consistency score.

---

## Related Files
- `references/borgatte-stevo-audit-2026-05-14.md` — Real case study with evidence from 7 conversations, all 10 gap categories demonstrated.
