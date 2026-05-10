---
name: ruflo
description: Ruflo multi-agent orchestration — swarm coordination, self-learning memory, agent federation, MCP server integration.
version: 1.0.0
author: rUvNet
license: MIT
metadata:
  hermes:
    tags: [agents, orchestration, swarm, mcp, multi-agent, ruflo]
---

# Ruflo — Multi-Agent AI Orchestration

## Overview

Ruflo (formerly Claude Flow) is an open-source multi-agent orchestration platform (⭐47K+) for coordinating AI agents. It provides swarm coordination, self-learning memory, federated comms, and enterprise security.

**GitHub**: https://github.com/ruvnet/ruflo  
**NPM**: `@claude-flow/ruflo`  
**Web UI**: https://flo.ruv.io/  
**Goal Planner**: https://goal.ruv.io/

## Key Capabilities

- 🤖 **100+ Specialized Agents** — coding, testing, security, docs, architecture
- 🐝 **Swarm Coordination** — hierarchical, mesh, adaptive topologies with consensus
- 🧠 **Self-Learning** — SONA neural patterns, ReasoningBank, trajectory learning
- 💾 **Vector Memory** — HNSW-indexed AgentDB (150x-12,500x faster search)
- ⚡ **Background Workers** — 12 auto-triggered workers (audit, optimize, testgaps)
- 🧩 **32 Plugins** — swarm, autopilot, federation, RAG, security, DDD, SPARC
- 🔌 **Multi-Provider** — Claude, GPT, Gemini, Cohere, Ollama with smart routing
- 🛡️ **Security** — AIDefence, CVE-hardened, PII detection, zero-trust federation
- 🌐 **Agent Federation** — cross-machine agent collaboration with mTLS

## Relevant Plugins for Agência Flux

### Marketing-Adjacent Plugins
- **ruflo-intelligence** — Self-learning from successes, useful for optimizing ad campaigns
- **ruflo-goals** — Break big goals into plans and track progress (pipeline automation)
- **ruflo-workflows** — Reusable multi-step task templates (content production pipeline)
- **ruflo-loop-workers** — Schedule background tasks on a timer (cron-like scheduling)
- **ruflo-autopilot** — Let agents run autonomously (hands-off content generation)
- **ruflo-rag-memory** — Smart retrieval for past campaigns, copy, learnings

### Architecture Plugins
- **ruflo-swarm** — Coordinate multiple agents (content + ads + CRM simultaneously)
- **ruflo-federation** — Agents across machines/orgs (team collaboration)
- **ruflo-agentdb** — Fast vector database for agent memory (campaign history)

## Installation

### CLI Install (Full)
```bash
npx ruflo@latest init wizard
```

### As MCP Server (for Hermes integration — RECOMMENDED)
```yaml
mcp_servers:
  ruflo:
    command: "npx"
    args: ["-y", "ruflo@latest", "mcp", "start"]
    timeout: 120
    connect_timeout: 60
```

## Considerations for Our Stack

### Pros
- Massive community (47K stars) — battle-tested
- 210+ MCP tools available immediately
- Self-learning (SONA) could optimize ad campaigns over time
- Swarm coordination = content + ads + CRM agents working in parallel
- Vector memory stores campaign history for pattern matching
- Works with Ollama (our opencode-go provider)

### Cons / Cautions
- **Heavy** — installs 100+ agents, 32 plugins, full daemon
- **Built for Claude Code** — works as MCP but primary UX is Claude/Codex plugin
- **Overlap with Hermes** — we already have delegation, skills, cron jobs, MCP
- **VPS Memory** — our 8GB box with swap would need careful resource management
- **Complexity** — adds significant surface area to an already working system
- **Not marketing-specific** — would need custom agents/skills for our use case

## Integration Path (If We Proceed)

### Recommended: MCP Server Only (2026-05-09 Assessment)

**Do NOT install Ruflo fully** on our current VPS (8GB RAM, 5 containers, memory limits already tight). The full install adds 100+ agents, 32 plugins, a daemon, and significant Node.js overhead. It would push memory beyond available limits.

**DO add as MCP server** to get 210+ tools without the full daemon:

```yaml
mcp_servers:
  ruflo:
    command: "npx"
    args: ["-y", "ruflo@latest", "mcp", "start"]
    timeout: 120
    connect_timeout: 60
```

This gives access to swarm coordination, memory, workflows, and goals **directly through Hermes** without changing our stack.

Useful when scaling to 5+ simultaneous clients. For now, Hermes built-in delegation + skills covers the same ground with less overhead.

### Phase 2: Selective Plugins
Install only marketing-relevant plugins:
```bash
npx ruflo@latest plugins install ruflo-workflows
npx ruflo@latest plugins install ruflo-goals
npx ruflo@latest plugins install ruflo-intelligence
npx ruflo@latest plugins install ruflo-loop-workers
```

### Phase 3: Custom Swarm
Define Flux-specific agents using ruflo swarm with our existing skills

## Key Commands
```bash
# Initialize
npx ruflo@latest init

# Start MCP server
npx ruflo@latest mcp start

# Spawn swarm
npx ruflo@latest swarm init --topology hierarchical
npx ruflo@latest agent spawn --role content-writer

# Memory
npx ruflo@latest memory store --key "campaign:meta" --value "..."
npx ruflo@latest memory search --query "summer campaign"

# Goals
npx ruflo@latest goals create "Launch ad campaign for Clinic X"
```