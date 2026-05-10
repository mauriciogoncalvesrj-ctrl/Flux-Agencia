# OpenClaw Provider 404 Fix (2026-05-09)

## Problem

OpenClaw container showed repeated errors:

```
FailoverError: The provider returned an HTML error page instead of an API response.
This usually means a CDN or gateway (e.g. Cloudflare) blocked the request.
model-fallback/decision: decision=candidate_failed requested=ollama/deepseek-v4-pro
reason=model_not_found next=ollama/glm-5.1
```

Every request to `ollama/*` models returned 404 HTML pages, then `ollama/glm-5.1` also failed, and only `opencode-go/kimi-k2.6` succeeded via fallback. This added 10-30s latency per request.

## Root Cause

Provider `ollama` and `opencode-go` had the **same baseUrl** (`https://opencode.ai/zen/go/v1`) but the `ollama/` prefix caused OpenClaw to route requests differently, resulting in 404 HTML error pages from the CDN/gateway.

## Fix

1. **Disable redundant `ollama` plugin** (same URL as `opencode-go`):
   ```json
   "plugins": { "entries": { "ollama": { "enabled": false } } }
   ```

2. **Update primary model and fallbacks** to use `opencode-go/*` prefix:
   ```json
   "model": {
     "primary": "opencode-go/kimi-k2.6",
     "fallbacks": [
       "opencode-go/deepseek-v4-pro",
       "opencode-go/glm-5.1",
       "opencode-go/minimax-m2.7"
     ]
   }
   ```

3. **Restart container**: `docker restart openclaw-4vbk-openclaw-1`

## Verification

```bash
docker logs openclaw-4vbk-openclaw-1 --tail 15 2>&1 | grep "model"
# Should show: [gateway] agent model: opencode-go/kimi-k2.6
# No more "HTML error page" or "model_not_found" errors
```

## Note

Container was also found killed (SIGTERM from a failed Telegram plugin enablement attempt). Simply `docker start` resolved that.