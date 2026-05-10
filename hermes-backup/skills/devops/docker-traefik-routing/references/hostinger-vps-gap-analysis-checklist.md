# Hostinger VPS Gap Analysis Checklist

Systematic diagnostic checklist for Docker-based VPS deployments. Run each section and compile findings into a prioritized report (Critical / High / Medium / Low).

## 1. System Resources

```bash
# CPU & load
nproc; uptime

# RAM & swap
free -h; swapon --show

# Disk
df -h / /data; df -i /

# OOM check (run on host via privileged container)
docker run --rm --privileged --pid=host -v /:/host alpine sh -c 'dmesg | grep -i oom | tail -10'
```

**Red flags:**
- Zero swap with multiple Docker services → OOM Kill risk
- Disk usage >85% → immediate cleanup needed
- Load average > nproc × 2 → CPU saturation

## 2. Docker Containers

```bash
# Status
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"

# Resource usage
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Memory limits (should be set!)
docker inspect --format '{{.Name}}: restart={{.HostConfig.RestartPolicy.Name}}, memory={{.HostConfig.Memory}}, cpus={{.HostConfig.NanoCpus}}' $(docker ps -aq)

# Restart counts
docker inspect --format '{{.Name}}: RestartCount={{.RestartCount}}, StartedAt={{.State.StartedAt}}' $(docker ps -aq)

# Dangling images
docker images -f "dangling=true"; docker system df
```

**Red flags:**
- `memory=0` on any container → no limit, can consume all RAM
- `RestartCount > 0` → investigate crash cause
- Dangling images → wasted disk space

## 3. Network & DNS

```bash
# Check DNS resolution inside each container
docker exec <container> cat /etc/resolv.conf
docker exec <container> curl -sI --connect-timeout 5 https://expected-api-endpoint.com

# Test from host
docker run --rm --privileged --pid=host alpine sh -c 'nslookup api.someservice.com 8.8.8.8'
```

**Red flags:**
- `NXDOMAIN` → provider endpoint is dead, needs URL change
- DNS timeout → Docker DNS misconfigured

## 4. Security

```bash
# Secrets in env vars (redacted)
docker exec <container> env | grep -iE "(API_KEY|SECRET|TOKEN|PASSWORD)" | sed 's/=.*/=<REDACTED>/'

# Ports exposed to 0.0.0.0
docker port <container>
ss -tlnp | grep "0.0.0.0"
```

**Red flags:**
- Passwords in docker-compose.yml comments or env vars in plaintext
- Sensitive ports exposed publicly

## 5. Service Configurations

For each service (Hermes, OpenClaw, Paperclip, WebUI, Traefik):
- Check config file for misconfigurations
- Check logs for errors: `docker logs <container> 2>&1 | grep -iE "(error|fail|crash|dns|timeout)" | tail -20`
- Check version vs latest release
- Check provider endpoints are reachable

## 6. Backups & Resilience

```bash
# Docker volumes
docker volume ls

# Scheduled backups
crontab -l; systemctl list-timers

# Data directories
du -sh /docker/* /opt/data/* 2>/dev/null | sort -rh | head -10
```

**Red flags:**
- Zero crontabs or timers → no automated backups
- Single volume with no backup policy
- Docker compose files have no `restart: unless-stopped`

## Fix Priority

1. **Critical:** Swap + memory limits (prevent OOM Kill)
2. **Critical:** Dead DNS endpoints (service-breaking)
3. **High:** Security exposures (passwords in plaintext)
4. **High:** Stale versions with known vulnerabilities
5. **Medium:** Missing backups
6. **Low:** Resource optimization, cleanup