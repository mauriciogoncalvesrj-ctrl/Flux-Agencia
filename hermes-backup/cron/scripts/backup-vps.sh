#!/bin/bash
# Flux VPS Daily Backup
# Backs up: Paperclip DB, Hermes config, OpenClaw config, Container specs
set -e

BACKUP_DIR="/opt/data/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting VPS backup..."

# 1. Paperclip PostgreSQL dump
echo "  → Paperclip DB..."
docker exec paperclip-tjjz-paperclip-1 sh -c 'PGPASSWORD=paperclip pg_dump -h localhost -p 54329 -U paperclip paperclip' 2>/dev/null | gzip > "$BACKUP_DIR/paperclip-db-${DATE}.sql.gz"

# 2. Hermes Agent config + env
echo "  → Hermes config..."
cp /opt/data/config.yaml "$BACKUP_DIR/config-${DATE}.yaml"
cp /opt/data/.env "$BACKUP_DIR/env-${DATE}"

# 3. OpenClaw config
echo "  → OpenClaw config..."
docker cp openclaw-4vbk-openclaw-1:/data/.openclaw/openclaw.json "$BACKUP_DIR/openclaw-${DATE}.json" 2>/dev/null || true

# 4. Container specs (for recreation)
echo "  → Container specs..."
docker inspect hermes-flux paperclip-tjjz-paperclip-1 openclaw-4vbk-openclaw-1 flux-traefik hermes-webui > "$BACKUP_DIR/containers-${DATE}.json"

# 5. Cleanup old backups (7 days)
echo "  → Cleanup..."
find "$BACKUP_DIR" -name "*.gz" -mtime +${RETENTION_DAYS} -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "*.json" -mtime +${RETENTION_DAYS} -delete 2>/dev/null || true
find "$BACKUP_DIR" -name "*.yaml" -mtime +${RETENTION_DAYS} -delete 2>/dev/null || true

BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo "[$(date)] Backup complete! Size: $BACKUP_SIZE"