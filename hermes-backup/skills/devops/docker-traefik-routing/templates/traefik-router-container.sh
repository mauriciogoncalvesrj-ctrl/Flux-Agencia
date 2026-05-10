#!/usr/bin/env bash
# Traefik Router Container Template
# Usage: fill in the variables and run.
# This creates a minimal container whose only purpose is to hold Traefik labels
# that route traffic to an EXISTING service (useful when docker-compose is managed).

ROUTER_NAME="${ROUTER_NAME:-somosflux-router}"
TRAEFIK_NETWORK="${TRAEFIK_NETWORK:-proxy}"
DOMAIN="${DOMAIN:-service.somosflux.com.br}"
ROUTER_ID="${ROUTER_ID:-service-somosflux}"
SVC_ID="${SVC_ID:-service-somosflux}"
TARGET_URL="${TARGET_URL:-http://target-container:8080}"

docker run -d --name "$ROUTER_NAME" --network "$TRAEFIK_NETWORK" \
  --restart unless-stopped \
  -l "traefik.enable=true" \
  -l "traefik.docker.network=$TRAEFIK_NETWORK" \
  -l "traefik.http.routers.${ROUTER_ID}.entrypoints=websecure" \
  -l "traefik.http.routers.${ROUTER_ID}.rule=Host(\`${DOMAIN}\`)" \
  -l "traefik.http.routers.${ROUTER_ID}.tls.certresolver=letsencrypt" \
  -l "traefik.http.routers.${ROUTER_ID}.service=${SVC_ID}" \
  -l "traefik.http.services.${SVC_ID}.loadbalancer.server.url=${TARGET_URL}" \
  busybox sleep infinity

echo "Router container '$ROUTER_NAME' created."
echo "Test with: curl -sk https://${DOMAIN}/"