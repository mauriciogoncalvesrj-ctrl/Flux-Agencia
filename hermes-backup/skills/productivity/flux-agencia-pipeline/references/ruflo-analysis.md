# Ruflo (ruvnet/ruflo) — Analysis for Agência Flux

## What It Is
Ruflo is a massive multi-agent orchestration platform (⭐47K GitHub). Features: 100+ agents, 32 plugins, vector memory (AgentDB HNSW), swarm coordination, self-learning (SONA), Web UI, Goal Planner.

## Why NOT Install Full
1. **VPS resource pressure**: 8GB RAM + 4GB swap already running 5 containers (Hermes 3GB, OpenClaw 2GB, Paperclip 1GB, WebUI 512MB, Traefik 256MB)
2. **Overlap with Hermes**: Hermes already provides delegate_task, cron, skills, memory, MCP servers, subagent depth 2
3. **Not the bottleneck**: Current gap is API tokens (Meta, GHL, n8n), not orchestration capacity

## What's Useful (Future)
- **SONA self-learning**: Agents learn from past successes — could improve pipeline quality over time
- **AgentDB (HNSW)**: Fast vector search for memory — useful when scaling to 5+ clients
- **Swarm coordination**: Parallel multi-agent tasks — helpful for batch content creation
- **Workflows**: Reusable task templates — complements Hermes skills

## How to Add Later (MCP Mode Only)
```yaml
mcp_servers:
  ruflo:
    command: "npx"
    args: ["-y", "ruflo@latest", "mcp", "start"]
```
This gives access to 210+ tools without installing the full platform.

## Verdict
Add as MCP server only when scaling past 3-5 simultaneous clients. Current priority: configure Meta Ads + GHL tokens, not more orchestration layers.