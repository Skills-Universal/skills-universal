---
name: planning-and-task-breakdown
description: Break complex tasks into executable steps. Use when a feature or change feels large, unclear, or risky. Use before starting any multi-day or multi-file implementation.
source: addyosmani/agent-skills
imported: 2026-04-29
---

# Planning and Task Breakdown

## Overview

Decompose complex work into clear, ordered, independently executable tasks. Good planning prevents thrashing, makes progress visible, and keeps increments small.

## When to Use

- Feature takes more than a few hours
- Multiple files or systems involved
- Unclear where to start
- Risk of getting lost mid-implementation

## The Breakdown Process

1. **State the goal** — one sentence, what does done look like?
2. **Identify dependencies** — what must exist before each step?
3. **Order by risk** — tackle the riskiest/most uncertain piece first
4. **Size each task** — each task = one increment (< 100 lines, testable alone)
5. **Name the unknowns** — list open questions explicitly

## Task Format

```markdown
### Task N: [Name]
- **Input:** what exists before this task
- **Output:** what exists after this task
- **Test:** how to verify this task is complete
- **Risk:** what could go wrong
```

## Red Flags

- Tasks that can't be tested independently
- Tasks larger than half a day of work
- No ordering (all tasks feel parallel)
- Missing the "how to verify" step

---
*Source: addyosmani/agent-skills — imported 2026-04-29*
