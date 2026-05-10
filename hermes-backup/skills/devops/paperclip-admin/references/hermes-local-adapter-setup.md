# Hermes Agent Installation Inside Paperclip Container

When the `hermes_local` adapter is used, Paperclip spawns `hermes chat -q "..."` as a child process. If the Hermes CLI is not installed inside the Paperclip container, the adapter fails with:
- `detect-model` returns `null`
- Agent stays in `status: "error"` with `lastRunStatus: "failed"` and `error: "Adapter failed"`
- Log shows: `Hermes CLI "hermes" not found in PATH`

## Full Installation Workflow

### 1. Install Python 3 and pip

The Paperclip container is Debian 13 (Trixie) with Node.js. Python is NOT included.

```bash
# Run as root — the node user can't use apt
docker exec -u root paperclip-tjjz-paperclip-1 apt-get update -qq
docker exec -u root paperclip-tjjz-paperclip-1 apt-get install -y -qq python3 python3-pip
```

### 2. Copy Hermes venv from host

The Hermes Agent on the host has a virtual environment at `/opt/hermes/.venv/` (~844MB). Copy it into the container:

```bash
# Create target directory
docker exec -u root paperclip-tjjz-paperclip-1 mkdir -p /opt/hermes
docker exec -u root paperclip-tjjz-paperclip-1 chown node:node /opt/hermes

# Copy the venv (this takes a minute for 844MB)
docker cp /opt/hermes/.venv paperclip-tjjz-paperclip-1:/opt/hermes/.venv
```

### 3. Copy Hermes Python modules

```bash
# Core Python packages (directories)
for dir in hermes_cli agent providers tools cron gateway plugins tui_gateway ui-tui web acp_adapter acp_registry; do
  if [ -d "/opt/hermes/$dir" ]; then
    docker cp /opt/hermes/$dir paperclip-tjjz-paperclip-1:/opt/hermes/$dir
  fi
done

# Top-level Python files
for f in cli.py run_agent.py hermes_state.py hermes_constants.py hermes_logging.py hermes_time.py utils.py mcp_serve.py model_tools.py toolsets.py toolset_distributions.py batch_runner.py rl_cli.py trajectory_compressor.py mini_swe_runner.py providers.py; do
  if [ -f "/opt/hermes/$f" ]; then
    docker cp /opt/hermes/$f paperclip-tjjz-paperclip-1:/opt/hermes/$f
  fi
done
```

### 4. Fix the entry point symlink

The copied `/opt/hermes/hermes` wrapper uses `#!/usr/bin/env python3` which finds system Python (missing dependencies). The venv has a proper entry point at `/opt/hermes/.venv/bin/hermes` that uses the venv Python.

```bash
docker exec -u root paperclip-tjjz-paperclip-1 ln -sf /opt/hermes/.venv/bin/hermes /usr/local/bin/hermes
```

### 5. Copy config and secrets

```bash
# Create .hermes directory in the container user's HOME
# Paperclip container HOME is /paperclip (not /home/node)
docker exec -u root paperclip-tjjz-paperclip-1 mkdir -p /paperclip/.hermes
docker cp /opt/data/config.yaml paperclip-tjjz-paperclip-1:/paperclip/.hermes/config.yaml
docker cp /opt/data/.env paperclip-tjjz-paperclip-1:/paperclip/.hermes/.env
docker exec -u root paperclip-tjjz-paperclip-1 chown -R node:node /paperclip/.hermes
docker exec -u root paperclip-tjjz-paperclip-1 chmod 644 /paperclip/.hermes/.env
```

**Pitfall:** `docker cp` preserves the original UID/GID from the host file. The `.env` file may end up owned by `10000:10000` instead of `node:node`, causing "Permission denied" when Hermes tries to read it. Always `chown` and `chmod` after copying.

### 6. Verify installation

```bash
# Should show version info
docker exec paperclip-tjjz-paperclip-1 hermes --version
# Expected: Hermes Agent v0.13.0 (2026.5.7) ...

# Check config is readable
docker exec paperclip-tjjz-paperclip-1 hermes config show

# Test a simple chat (confirms API keys work)
docker exec paperclip-tjjz-paperclip-1 timeout 30 hermes chat -q "Say hello" -Q --yolo
```

## Notes

- All changes are **temporary** — lost when the container is recreated (Hostinger "Atualizar" button)
- The `hermes_local` adapter spawns `hermes chat -q "<prompt>" -Q -m <model> --provider <provider>`
- Provider resolution: explicit config → detected from ~/.hermes/config.yaml → inferred from model name → "auto"
- When provider resolves to "auto", no `--provider` flag is passed, and Hermes uses its config default
- The adapter inherits `process.env` from the Paperclip Node process, plus any `env` keys from adapterConfig

## API Key Configuration

If the `.env` file has permission issues, add the API key directly to the agent's adapter config:

```bash
curl -s -b "$COOKIE_JAR" -X PATCH \
  "http://localhost:3100/api/agents/<agentId>?companyId=<companyId>" \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3100" \
  -d '{"adapterConfig":{"...other fields...","env":{"OPENCODE_GO_API_KEY":"sk-..."}}}'
```

The `env` field in adapterConfig is merged into the child process environment, so the spawned Hermes CLI gets these variables.
