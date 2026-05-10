#!/usr/bin/env bash
# VPS Gap Analysis — Full Infrastructure Audit
# Scans 7 areas: system resources, Docker, network, security, services, backups, disk.
# Run: bash vps-gap-analysis.sh
# Designed for Hostinger VPS Docker Compose Catalog environments.

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
ORANGE='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "=========================================="
echo "       VPS GAP ANALYSIS — FULL AUDIT      "
echo "=========================================="
echo ""

# ── 1. SYSTEM RESOURCES ──
echo "═══ 1. SYSTEM RESOURCES ═══"
echo "--- CPU ---"
echo "CPUs: $(nproc)"
cat /proc/cpuinfo | grep "model name" | head -1
echo "--- Load Average ---"
uptime
echo "--- RAM ---"
free -h
echo ""
SWAP_TOTAL=$(awk '/SwapTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo "0")
if [ "$SWAP_TOTAL" = "0" ] || [ -z "$SWAP_TOTAL" ]; then
  echo -e "${RED}⚠ CRITICAL: ZERO SWAP CONFIGURED${NC} — OOM kills likely under memory pressure"
else
  echo "Swap: $(($SWAP_TOTAL / 1024)) MB"
fi
echo "--- Disk ---"
df -h / 2>/dev/null
echo ""

# ── 2. DOCKER ──
echo "═══ 2. DOCKER CONTAINERS ═══"
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}' 2>/dev/null || echo "Docker not available"
echo ""
echo "--- Container Resource Usage ---"
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}' 2>/dev/null || echo "Docker stats unavailable"
echo ""
echo "--- Restart Policies & Memory Limits ---"
for c in $(docker ps -q 2>/dev/null); do
  name=$(docker inspect --format '{{.Name}}' "$c" 2>/dev/null)
  rp=$(docker inspect --format '{{.HostConfig.RestartPolicy.Name}}' "$c" 2>/dev/null)
  mem=$(docker inspect --format '{{.HostConfig.Memory}}' "$c" 2>/dev/null)
  cpus=$(docker inspect --format '{{.HostConfig.NanoCpus}}' "$c" 2>/dev/null)
  if [ "$mem" = "0" ] || [ -z "$mem" ]; then
    mem_flag="${RED}NO LIMIT${NC}"
  else
    mem_flag="${GREEN}$(($mem / 1048576))MB${NC}"
  fi
  if [ "$cpus" = "0" ] || [ -z "$cpus" ]; then
    cpu_flag="${YELLOW}NO LIMIT${NC}"
  else
    cpu_flag="${GREEN}$((cpus / 1000000000)) CPUs${NC}"
  fi
  echo "$name: restart=$rp, memory=$mem_flag, cpus=$cpu_flag"
done
echo ""
echo "--- Restart Counts ---"
for c in $(docker ps -aq 2>/dev/null); do
  name=$(docker inspect --format '{{.Name}}' "$c" 2>/dev/null)
  rc=$(docker inspect --format '{{.RestartCount}}' "$c" 2>/dev/null)
  started=$(docker inspect --format '{{.State.StartedAt}}' "$c" 2>/dev/null)
  if [ "$rc" -gt 0 ] 2>/dev/null; then
    echo -e "${YELLOW}$name: RestartCount=$rc (started: $started)${NC}"
  else
    echo "$name: RestartCount=0 (started: $started)"
  fi
done
echo ""

# ── 3. NETWORK ──
echo "═══ 3. NETWORK ═══"
echo "--- Listening Ports ---"
ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null || echo "ss/netstat unavailable"
echo ""
echo "--- DNS ---"
cat /etc/resolv.conf 2>/dev/null
echo ""
echo "--- Docker Networks ---"
docker network ls --format 'table {{.Name}}\t{{.Driver}}\t{{.Scope}}' 2>/dev/null || echo "Docker networks unavailable"
echo ""

# ── 4. SECURITY ──
echo "═══ 4. SECURITY ═══"
echo "--- Exposed Ports (0.0.0.0) ---"
ss -tlnp 2>/dev/null | grep "0.0.0.0" || echo "No ports bound to 0.0.0.0 (or ss unavailable)"
echo ""
echo "--- Firewall Status ---"
ufw status 2>/dev/null || echo "UFW not available (may need host access)"
echo ""
echo "--- Hardcoded Passwords in Docker Compose ---"
for f in $(find /opt /data /docker -name "docker-compose*.yml" -o -name "compose*.yml" 2>/dev/null | head -20); do
  matches=$(grep -icE "(PASSWORD|SECRET|TOKEN|API_KEY)=" "$f" 2>/dev/null || echo "0")
  if [ "$matches" -gt 0 ]; then
    echo -e "${YELLOW}⚠ $f: $matches potential hardcoded secret(s)${NC}"
  fi
done
echo ""

# ── 5. SERVICES ──
echo "═══ 5. SERVICE HEALTH ═══"
echo "--- OpenClaw Version ---"
docker exec openclaw-4vbk-openclaw-1 cat /data/.openclaw/version 2>/dev/null || echo "Version file not found"
echo "OpenClaw Image Date:"
docker inspect openclaw-4vbk-openclaw-1 --format '{{.Created}}' 2>/dev/null || echo "Container not found"
echo ""
echo "--- OpenClaw Plugin Errors ---"
docker logs openclaw-4vbk-openclaw-1 2>&1 | grep -i "plugin.*failed\|plugin.*error\|validation" | tail -5 2>/dev/null || echo "No plugin errors found"
echo ""
echo "--- OpenClaw DNS Errors ---"
docker logs openclaw-4vbk-openclaw-1 2>&1 | grep -i "ENOTFOUND\|DNS lookup" | tail -5 2>/dev/null || echo "No DNS errors found"
echo ""
echo "--- Hermes Vision Provider ---"
docker logs hermes-flux 2>&1 | grep -i "vision.*provider\|No LLM provider configured for task=vision" | tail -3 2>/dev/null || echo "No vision errors found"
echo ""
echo "--- Hermes Gateway Errors ---"
docker logs hermes-flux 2>&1 | grep -iE "RuntimeError|BadRequest|503|overloaded" | tail -5 2>/dev/null || echo "No gateway errors found"
echo ""

# ── 6. BACKUPS ──
echo "═══ 6. BACKUPS & RESILIENCE ═══"
echo "--- Crontab ---"
crontab -l 2>/dev/null || echo "No crontab configured"
echo ""
echo "--- Systemd Timers ---"
systemctl list-timers 2>/dev/null || echo "systemctl not available in container"
echo ""
echo "--- Docker Volumes (potential data loss if no backup) ---"
docker volume ls -q 2>/dev/null | while read v; do
  used_by=$(docker ps -a --filter volume="$v" --format '{{.Names}}' | tr '\n' ', ')
  echo "$v | Used by: ${used_by:-NONE}"
done
echo ""

# ── 7. DISK & CLEANUP ──
echo "═══ 7. DISK & CLEANUP ═══"
echo "--- Docker Images ---"
docker images --format 'table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}' 2>/dev/null || echo "Docker images unavailable"
echo ""
echo "--- Dangling Images ---"
dangling=$(docker images -f "dangling=true" -q 2>/dev/null | wc -l)
if [ "$dangling" -gt 0 ] 2>/dev/null; then
  dangling_size=$(docker images -f "dangling=true" --format '{{.Size}}' 2>/dev/null | head -1)
  echo -e "${YELLOW}⚠ $dangling dangling image(s) found ($dangling_size) — run 'docker image prune -f' to reclaim${NC}"
else
  echo "No dangling images"
fi
echo ""
echo "--- Docker System Disk Usage ---"
docker system df 2>/dev/null || echo "Docker system df unavailable"
echo ""
echo "--- Stopped Containers ---"
stopped=$(docker ps -a --filter "status=exited" -q 2>/dev/null | wc -l)
if [ "$stopped" -gt 0 ] 2>/dev/null; then
  echo -e "${YELLOW}⚠ $stopped stopped container(s) found${NC}"
  docker ps -a --filter "status=exited" --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}' 2>/dev/null
else
  echo "No stopped containers"
fi
echo ""

echo "=========================================="
echo "           END OF GAP ANALYSIS           "
echo "=========================================="
echo ""
echo "Priority fixes:"
[ "$SWAP_TOTAL" = "0" ] && echo -e "  ${RED}1. CREATE SWAP (4GB minimum)${NC}"
echo -e "  ${RED}2. SET CONTAINER MEMORY LIMITS${NC}"
echo -e "  ${YELLOW}3. UPDATE OUTDATED IMAGES${NC}"
echo -e "  ${YELLOW}4. CONFIGURE BACKUPS${NC}"
echo -e "  ${YELLOW}5. FIX VISION PROVIDER / DNS / PLUGINS${NC}"
echo -e "  ${GREEN}6. CLEAN DANGLING IMAGES & UNUSED RESOURCES${NC}"