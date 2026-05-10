# Kanban Programmatic Access via SQLite

> When the `hermes kanban` CLI is not available inside a container (e.g. Docker), interact directly with `kanban.db` via Python/SQLite.

## When You Need This

- Running inside a Docker container where the `hermes` binary is not installed
- The `kanban_*` toolset is gated to worker processes (`HERMES_KANBAN_TASK` env var)
- You need to create tasks, read status, or build dashboards from a script
- Building an external orchestrator that manages the kanban board

## Schema

The kanban database lives at `~/.hermes/kanban.db` (or `$HERMES_HOME/kanban.db`).

### Key Tables

| Table | Purpose |
|-------|---------|
| `tasks` | Main task records |
| `task_links` | Parent/child relationships |
| `task_comments` | Comment threads |
| `task_events` | Audit log |
| `task_runs` | Worker execution records |
| `kanban_notify_subs` | Gateway notification subscriptions |

### tasks Table Schema

```sql
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,
  title TEXT,
  body TEXT,
  assignee TEXT,
  status TEXT,          -- 'todo', 'ready', 'running', 'blocked', 'done', 'archived'
  priority INTEGER,     -- 1 = highest, 5 = lowest
  created_by TEXT,
  created_at INTEGER,   -- Unix timestamp
  started_at INTEGER,
  completed_at INTEGER,
  workspace_kind TEXT,  -- 'scratch', 'dir:/path', 'worktree'
  workspace_path TEXT,
  claim_lock TEXT,
  claim_expires INTEGER,
  tenant TEXT,          -- Namespace isolation
  result TEXT,
  idempotency_key TEXT,
  consecutive_failures INTEGER,
  worker_pid INTEGER,
  last_failure_error TEXT,
  max_runtime_seconds INTEGER,
  last_heartbeat_at INTEGER,
  current_run_id INTEGER,
  workflow_template_id TEXT,
  current_step_key TEXT,
  skills TEXT,          -- JSON array of skill names
  max_retries INTEGER
);
```

**Critical status values:**
- `todo` — Created, not yet ready for dispatch
- `ready` — Eligible for dispatcher pickup
- `running` — Claimed by a worker process
- `blocked` — Waiting for human input or parent completion
- `done` — Completed successfully
- `archived` — Soft-deleted

## Creating a Task

```python
import sqlite3
import json
import uuid
import time

KANBAN_DB = '/opt/data/kanban.db'  # or ~/.hermes/kanban.db
TENANT = 'flux-agencia'

conn = sqlite3.connect(KANBAN_DB)
cursor = conn.cursor()

task_id = f"flux-{uuid.uuid4().hex[:8]}"
now = int(time.time())

cursor.execute('''
    INSERT INTO tasks (
        id, title, body, assignee, status, priority,
        created_by, created_at, tenant, skills, max_runtime_seconds
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    task_id,
    '🚀 Campanha Meta Ads - Cliente X',
    'Criar estrutura de campanha Meta Ads...',
    'flux-trafego',           # Profile name
    'todo',                    # Initial status
    1,                         # Priority (1 = highest)
    'hermes-orchestrator',     # Created by
    now,
    TENANT,
    json.dumps(['flux-agencia-trafego']),  # Skills as JSON array
    1800                       # Max runtime in seconds
))

conn.commit()
conn.close()

print(f"Created task: {task_id}")
```

## Querying Tasks

### List all tasks in a tenant

```python
cursor.execute('''
    SELECT id, title, assignee, status, priority, created_at
    FROM tasks
    WHERE tenant = ?
    ORDER BY 
        CASE status 
            WHEN 'ready' THEN 1 
            WHEN 'running' THEN 2 
            WHEN 'todo' THEN 3 
            WHEN 'blocked' THEN 4 
            WHEN 'done' THEN 5 
            ELSE 6 
        END,
        priority ASC,
        created_at DESC
''', (TENANT,))
```

### Status summary by assignee

```python
cursor.execute('''
    SELECT assignee, status, COUNT(*) 
    FROM tasks 
    WHERE tenant = ?
    GROUP BY assignee, status
''', (TENANT,))
```

### Next task to execute

```python
cursor.execute('''
    SELECT id, title, assignee, body
    FROM tasks
    WHERE tenant = ? AND status IN ('ready', 'todo', 'running')
    ORDER BY priority ASC, created_at DESC
    LIMIT 1
''', (TENANT,))
```

## Updating Task Status

```python
# Mark as running
cursor.execute(
    "UPDATE tasks SET status = 'running', started_at = ? WHERE id = ?",
    (int(time.time()), task_id)
)

# Mark as done
cursor.execute(
    "UPDATE tasks SET status = 'done', completed_at = ? WHERE id = ?",
    (int(time.time()), task_id)
)

# Block for human input
cursor.execute(
    "UPDATE tasks SET status = 'blocked' WHERE id = ?",
    (task_id,)
)

conn.commit()
```

## Linking Tasks (Dependencies)

```python
# Create parent-child link
cursor.execute('''
    INSERT INTO task_links (parent_id, child_id, link_type)
    VALUES (?, ?, 'depends_on')
''', (parent_task_id, child_task_id))
```

When a parent task reaches `done`, children with `status = 'todo'` and all parents `done` auto-promote to `ready` (handled by the dispatcher, not automatic in raw SQL).

## Adding Comments

```python
cursor.execute('''
    INSERT INTO task_comments (task_id, author, body, created_at)
    VALUES (?, ?, ?, ?)
''', (task_id, 'hermes-orchestrator', 'Task started', int(time.time())))
```

## Pitfalls

- **Tenant isolation:** Always filter by `tenant`. Tasks without a tenant default to the global namespace and may leak across workspaces.
- **Status values:** The dispatcher uses specific strings (`ready`, `running`, `todo`, `blocked`, `done`, `archived`). Using other strings breaks dispatch.
- **Skills column:** Must be valid JSON array. Empty list: `'[]'`. Invalid JSON breaks skill loading.
- **No foreign key enforcement:** SQLite pragma must be set explicitly if you want FK checks on `task_links`.
- **Claim locking:** The `claim_lock` and `claim_expires` fields are used by the dispatcher for atomic claim. Don't manually set these unless you know the dispatcher won't conflict.

## Full Orchestrator Example

A complete Python script that wraps these patterns:

```python
#!/usr/bin/env python3
import sqlite3, json, uuid, time, argparse

KANBAN_DB = '/opt/data/kanban.db'
TENANT = 'flux-agencia'

def create_task(title, assignee, body='', priority=2, skills=None):
    conn = sqlite3.connect(KANBAN_DB)
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    conn.execute('''INSERT INTO tasks (...)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (task_id, title, body, assignee, 'todo', priority,
         'orchestrator', int(time.time()), TENANT,
         json.dumps(skills or []), 1800))
    conn.commit()
    conn.close()
    return task_id

def list_tasks():
    conn = sqlite3.connect(KANBAN_DB)
    rows = conn.execute(
        "SELECT id, title, assignee, status, priority FROM tasks WHERE tenant = ? ORDER BY priority",
        (TENANT,)
    ).fetchall()
    conn.close()
    return rows

# ... etc
```

## CLI Equivalent (when available)

When the `hermes` binary is available, prefer the CLI:

```bash
hermes kanban create "Title" --assignee flux-trafego --tenant flux-agencia
hermes kanban list --tenant flux-agencia
hermes kanban complete <id> --summary "Done" --metadata '{"result": "ok"}'
```

Use the SQLite approach only when the CLI is inaccessible.
