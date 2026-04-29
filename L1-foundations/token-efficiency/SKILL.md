---
name: token-efficiency
description: Reduces token consumption in Claude.ai sessions with MCP connectors. Use at the start of every session and when planning multi-step tasks. Especially relevant for long Odoo development sessions, file operations on Hetzner, and GitHub MCP workflows.
source: custom — Astronomitaly/fabrizio-marra
created: 2026-04-29
---

# Token Efficiency

## Overview

Token efficiency in Claude.ai is fundamentally different from Claude Code.
There are no subagents, no model routing, no parallel execution.
The only levers available are: **what goes into context**, **when it goes in**, and **how much of it**.

This skill documents patterns learned from real sessions managing Odoo 19 modules,
Hetzner server operations, and GitHub MCP workflows.

---

## The Core Principle

**Load context just-in-time, not up-front.**

Every tool call, file read, and search result consumes context window.
Context consumed early in a session is still present at the end — it never leaves.
The goal is to load only what is needed, exactly when it is needed.

---

## Rule 1 — Never load a full file when you need only part of it

```
# BAD: loads entire 500-line file
read_file('/opt/odoo19/custom/addons/ODOO19_DEV_NOTES.md')

# GOOD: loads only the relevant section
read_file('/opt/odoo19/custom/addons/ODOO19_DEV_NOTES.md', start_line=1, end_line=80)
```

Use `start_line` / `end_line` parameters on every `read_file` call unless
the full file is genuinely needed. Prefer `search_addon_code` to locate
the relevant section first, then read only those lines.

---

## Rule 2 — Use search before read

```
# BAD: read full file to find one function
read_file('models/guide.py')  # 800 lines

# GOOD: find the function first, then read only those lines
search_addon_code('def _compute_status', addon_name='astro_guide')  # returns line numbers
read_file('models/guide.py', start_line=142, end_line=165)           # 23 lines
```

`search_addon_code` returns line numbers. Use them.

---

## Rule 3 — One tool call per question

Do not make exploratory tool calls "just to check".
Every tool result enters the context window permanently.

```
# BAD: 3 exploratory calls to understand the situation
list_addon_files('astro_guide')
read_file('__manifest__.py')
read_file('models/__init__.py')

# GOOD: one targeted call based on what you actually need
read_file('__manifest__.py', start_line=1, end_line=20)  # just the manifest header
```

---

## Rule 4 — Prefer str_replace_file over write_file for small changes

```
# BAD: reads entire file, rewrites entire file (2x file size in context)
read_file('views/guide_views.xml')   # 300 lines in context
write_file('views/guide_views.xml')  # 300 lines again

# GOOD: only the changed string enters context
str_replace_file(path, old_str='<tree>', new_str='<list>')  # 2 lines
```

`str_replace_file` is the right tool for surgical changes.
`write_file` only when restructuring the entire file.

---

## Rule 5 — Load devnotes once per session, not per task

ODOO19_DEV_NOTES.md is ~500 lines. Load it once at session start,
read only the relevant section. Do not reload it for each sub-task.

If a session is short and focused (e.g. fix one XML view), skip devnotes entirely
and load only the specific section needed via `search_addon_code`.

---

## Rule 6 — GitHub MCP: fetch only the file you need

```
# BAD: list directory to discover, then fetch each file
get_file_contents(owner, repo, path='skills/odoo-19.0/')          # directory listing
get_file_contents(owner, repo, path='skills/odoo-19.0/SKILL.md')  # then the file

# GOOD: fetch the file directly if you know the path
get_file_contents(owner, repo, path='skills/odoo-19.0/SKILL.md')  # one call
```

Skill files in skills-universal have predictable paths.
Use them directly — do not browse.

---

## Rule 7 — Avoid redundant project_knowledge_search

`project_knowledge_search` adds results to context.
Do not search for things that are:
- Already in context from this session
- Obviously known (Odoo syntax, Python basics)
- Available faster via a direct server read

Search project knowledge only when the answer might be in a SOA or pipeline doc
that is NOT on the server.

---

## Rule 8 — Prefer psql queries over ORM reads for data exploration

```
# BAD: execute_method returns full record dicts — verbose
execute_method('astro.guide', 'search_read', [[['active','=',True]]], {})

# GOOD: SQL returns only the columns you need
run_psql('SELECT id, name, state FROM astro_guide WHERE active=true LIMIT 5')
```

`run_psql` returns compact tabular output. Much less context than ORM dicts.

---

## Rule 9 — Plan the task before executing tool calls

Before making any tool call, state the plan:
```
Task: add field x_notes to astro.guide
Plan:
  1. read manifest to check current version (5 lines)
  2. read models/guide.py lines 1-30 to check existing fields
  3. str_replace to add field
  4. str_replace manifest version bump
  5. button_immediate_upgrade
Estimated tool calls: 5
```

This prevents exploratory calls and keeps the session focused.

---

## Rule 10 — Close long sessions proactively

Context window fills up silently. Signs that a session is getting expensive:
- Tool results are getting truncated
- Responses reference things from much earlier in the conversation
- Simple questions get slow responses

When this happens: save state to server (`write_file` session notes),
open a new chat, load only what the next task needs.

The session file pattern:
```
write_file('/opt/odoo19/custom/addons/SESSION_[topic]_[date].md', ...)
```

---

## Rule 11 — Batch GitHub pushes

```
# BAD: one push_files call per file (multiple round trips, more context)
push_files(..., files=[{path: 'file1.md', content: '...'}])
push_files(..., files=[{path: 'file2.md', content: '...'}])

# GOOD: all files in one push_files call
push_files(..., files=[
  {path: 'file1.md', content: '...'},
  {path: 'file2.md', content: '...'},
  {path: 'file3.md', content: '...'}
])
```

Each MCP call has overhead. Batch wherever possible.

---

## Rule 12 — Use exec_python_file for multi-step DB operations

Instead of multiple `execute_method` calls for related DB operations,
write a single Python script that does everything in one transaction:

```python
# /tmp/fix_guides.py — runs as one exec_python_file call
for guide in env['astro.guide'].search([('state', '=', 'draft')]):
    guide.write({'x_notes': 'migrated'})
env.cr.commit()
```

One tool call instead of N. Output saved to /tmp/result.json.

---

## Rule 13 — Skip skills loading for simple/known tasks

Skills auto-scan costs ~100 tokens per skill per session.
Do not load skill content for tasks where the answer is already known.

```
# Skills NOT needed for:
- Fixing a typo in XML
- Adding a single field with a known pattern
- Checking a log file
- Running a simple SQL query

# Skills NEEDED for:
- Designing a new module architecture
- Building a portal page (needs frontend-ui + odoo-19 + security)
- Writing a migration script (needs odoo-19/migration + debugging)
```

---

## Rule 14 — Compress session notes before saving

When saving session state to the server, write decisions and outcomes only —
not the full conversation transcript.

```
# BAD session note: full chat export (50KB)
# GOOD session note:
## Session [date] — astro_guide portal fix
## Decision: use str_replace not write_file for template updates
## Done: fixed portal_profile_templates.xml line 142
## Next: test with fabryalliance@gmail.com account
## Pending: bump version to 19.0.5.11.0
```

4-6 lines is enough to resume a session.

---

## Rule 15 — One module per chat

Each chat session should touch exactly one module.
Cross-module work multiplies context: two modules' files, two manifests,
two sets of devnotes sections, two test accounts.

If a feature requires changes to two modules:
- Chat A: module 1 changes → backup → deploy → verify
- Chat B: module 2 changes → backup → deploy → verify

---

## Quick Reference Checklist

Before starting a task:
- [ ] Do I know exactly which file/lines I need? → use start_line/end_line
- [ ] Can I use search instead of read? → use search_addon_code first
- [ ] Can I batch multiple changes in one script? → write exec_python_file
- [ ] Can I batch multiple file pushes? → one push_files call
- [ ] Is this task simple enough to skip skill loading? → skip if yes
- [ ] Is this session getting long? → save state and open new chat

---

## Token Cost Reference (approximate, claude.ai)

| Operation | Approx tokens added to context |
|---|---|
| read_file (500 lines) | ~3,000 |
| read_file (50 lines) | ~300 |
| search_addon_code result | ~200 |
| run_psql result (5 rows) | ~100 |
| execute_method search_read (10 records) | ~800 |
| push_files (3 files) | ~200 (just confirmation) |
| project_knowledge_search (5 results) | ~1,500 |
| skill SKILL.md load (medium) | ~800 |
| GitHub get_file_contents (medium file) | ~2,000 |

**Target per session:** keep total context under 30,000 tokens for responsive, focused work.

---
*Source: custom — built from Astronomitaly/fabrizio-marra real session patterns*
*Created: 2026-04-29 — update when new patterns emerge*
