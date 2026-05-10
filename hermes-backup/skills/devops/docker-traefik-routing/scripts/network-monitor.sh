#!/bin/bash
# Generic Docker network monitor for Traefik-managed services
# Run from a container with docker.sock mounted (e.g., Hermes Agent)
#
# Usage: Configure TRAEFIK_NETWORK and SERVICES below, then schedule via cron.
# Logs to /opt/data/logs/network-monitor.log by default.

TRAEFIK_NETWORK="${TRAEFIK_NETWORK:-proxy}"
LOG_FILE="${LOG_FILE:-/opt/data/logs/network-monitor.log}"

# List of container names that MUST be on the Traefik network
# Format: "container_name:health_port"
SERVICES="${SERVICES:-hermes-flux:9119}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# --- Check and reconnect each service ---
IFS=',' read -ra SERVICE_LIST <<< "$SERVICES"
for svc in "${SERVICE_LIST[@]}"; do
    container="${svc%%:*}"
    port="${svc##*:}"

    # Check if container exists
    if ! docker inspect "$container" >/dev/null 2>&1; then
        log "SKIP - container '$container' not found"
        continue
    fi

    # Check networks
    networks=$(docker inspect "$container" --format='{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}' 2>/dev/null)

    if echo "$networks" | grep -qw "$TRAEFIK_NETWORK"; then
        log "OK - $container connected to '$TRAEFIK_NETWORK'"
    else
        log "ALERT - $container NOT on '$TRAEFIK_NETWORK' (networks: $networks). Reconnecting..."
        docker network connect "$TRAEFIK_NETWORK" "$container" 2>/dev/null
        if [ $? -eq 0 ]; then
            log "FIXED - $container reconnected to '$TRAEFIK_NETWORK'"
        else
            log "ERROR - failed to reconnect $container"
            continue
        fi
    fi

    # Health check via Traefik network
    if [ -n "$port" ]; then
        health=$(docker run --rm --network "$TRAEFIK_NETWORK" busybox wget -qO- --timeout=5 "http://$container:$port/" 2>/dev/null | head -1)
        if echo "$health" | grep -qi "doctype\|html\|200"; then
            log "HEALTH - $container:$port responds OK via '$TRAEFIK_NETWORK'"
        else
            log "WARNING - $container:$port NOT responding via '$TRAEFIK_NETWORK'"
        fi
    fi
done
