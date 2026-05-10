#!/bin/bash
# Fix Traefik network connectivity for Hermes Agent services
# Runs inside hermes-flux container (has docker.sock access)
# Created: 2026-05-08

LOG_FILE="/opt/data/logs/network-fix.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check if hermes-flux is connected to 'proxy' network
HERMES_NETWORKS=$(docker inspect hermes-flux --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' 2>/dev/null)

if echo "$HERMES_NETWORKS" | grep -qw "proxy"; then
    log "OK - hermes-flux already connected to 'proxy' network"
else
    log "ALERT - hermes-flux NOT connected to 'proxy' network. Networks found: $HERMES_NETWORKS"
    docker network connect proxy hermes-flux 2>/dev/null
    if [ $? -eq 0 ]; then
        log "FIXED - hermes-flux reconnected to 'proxy' network"
    else
        log "ERROR - failed to reconnect hermes-flux to 'proxy' network"
    fi
fi

# Verify all critical services are on proxy network
for container in openclaw-4vbk-openclaw-1 paperclip-tjjz-paperclip-1; do
    NETWORKS=$(docker inspect "$container" --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' 2>/dev/null)
    if ! echo "$NETWORKS" | grep -qw "proxy"; then
        log "ALERT - $container NOT on 'proxy' network. Reconnecting..."
        docker network connect proxy "$container" 2>/dev/null
        if [ $? -eq 0 ]; then
            log "FIXED - $container reconnected to 'proxy' network"
        else
            log "ERROR - failed to reconnect $container"
        fi
    fi
done

# Quick health check via Traefik's network
HEALTH=$(docker run --rm --network proxy busybox wget -qO- --timeout=5 http://hermes-flux:9119 2>/dev/null | head -1)
if echo "$HEALTH" | grep -q "doctype\|html"; then
    log "HEALTH - hermes dashboard responds OK via proxy network"
else
    log "WARNING - hermes dashboard NOT responding via proxy network (502 likely)"
fi
