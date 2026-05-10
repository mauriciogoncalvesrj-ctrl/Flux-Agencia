# Session Reference: Evening Recurrence (2026-05-08)

## Context

Same Hostinger VPS from the afternoon session. Auto-healing monitor (`traefik-network-fix`) was created and scheduled every 5 minutes.

## Problem Recurred

`https://hermes.somosflux.com.br/` again returned **502 Bad Gateway**, approximately 5 hours after the original fix.

## Diagnosis

```bash
# 502 confirmed from outside
curl -s -o /dev/null -w "%{http_code}" https://hermes.somosflux.com.br/   # -> 502

# hermes-flux missing proxy network AGAIN
docker inspect hermes-flux --format='{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'
# -> hermes-agent-84im_default   (MISSING: proxy)

# Other services unaffected — still on both networks
# openclaw-4vbk-openclaw-1: hermes-net proxy
# paperclip-tjjz-paperclip-1: hermes-net proxy

# Container had been recreated ~2 hours earlier
docker inspect hermes-flux --format='{{.State.StartedAt}}'
# -> 2026-05-08T19:XX:XXZ (started ~2h before diagnosis)
```

## Key Finding

The Hostinger panel recreated the `hermes-flux` container between the afternoon and evening sessions. The auto-healing monitor would have caught this within 5 minutes, but the user tested during the gap window.

## Fix Applied

```bash
docker network connect proxy hermes-flux
```

All domains verified:
- `hermes.somosflux.com.br` -> 200 ✅
- `openclaw.somosflux.com.br` -> 200 ✅
- `paperclip.somosflux.com.br` -> 200 ✅

## Auto-Healing Monitor Status

The cronjob `traefik-network-fix` was confirmed present and functional. The script at `/opt/data/scripts/fix-traefik-network.sh` logs to `/opt/data/logs/network-fix.log`.

## Lesson

Even with a 5-minute polling monitor, there is a small window of unavailability after container recreation. For stricter SLAs, consider:
- Reducing interval to 1 minute
- Or using a Docker event watcher (reacts instantly to container start events)

## Pre-Diagnosis Workflow Correction

The assistant initially began diagnosing from scratch. The user corrected: *"olha os ultimas memorias, pois foram feitas modificações ja"* (check the latest memories, modifications were already made).

This confirmed the fix should always start with `session_search` when the user reports a recurring issue on a previously configured domain.
