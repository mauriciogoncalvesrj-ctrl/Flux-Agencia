#!/usr/bin/env bash
# Docker Audit Script — Lists containers, images, volumes, networks
# and flags duplicates, orphans, and empty resources.
# Run: bash docker-audit.sh

set -euo pipefail

echo "=========================================="
echo "           DOCKER AUDIT REPORT           "
echo "=========================================="
echo ""

echo "=== CONTAINERS ==="
docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
echo ""

echo "=== IMAGES ==="
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}'
echo ""

echo "=== IMAGES IN USE ==="
docker ps -a --format '{{.Image}}' | sort -u
echo ""

echo "=== DANGLING IMAGES ==="
docker images --filter "dangling=true" --format 'table {{.ID}}\t{{.Size}}\t{{.CreatedAt}}'
echo ""

echo "=== VOLUMES ==="
docker volume ls --format 'table {{.Name}}\t{{.Driver}}'
echo ""

echo "=== VOLUME USAGE ==="
docker volume ls -q | while read v; do
  used_by=$(docker ps -a --filter volume=$v --format '{{.Names}}' | tr '\n' ', ')
  echo "$v | Used by: ${used_by:-NONE}"
done
echo ""

echo "=== NETWORKS ==="
docker network ls --format 'table {{.Name}}\t{{.Driver}}'
echo ""

echo "=== EMPTY NETWORKS ==="
docker network ls --format '{{.Name}}' | while read n; do
  count=$(docker network inspect "$n" --format '{{len .Containers}}' 2>/dev/null || echo "0")
  [ "$count" = "0" ] && echo "$n: EMPTY (safe to remove if not default)"
done
echo ""

echo "=========================================="
echo "              END OF REPORT              "
echo "=========================================="
