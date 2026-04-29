---
name: spec-driven-development
description: Write the spec before the code. Use when starting any new feature, module, or non-trivial change. Ensures alignment before implementation begins.
source: addyosmani/agent-skills
imported: 2026-04-29
---

# Spec-Driven Development

## Overview

Write a precise specification before writing code. A spec defines what success looks like, catches misunderstandings early, and prevents scope creep during implementation.

## When to Use

- Starting any new feature
- Building a new module or component
- Any task where requirements feel ambiguous
- Before any implementation that touches multiple files

## The Spec Format

```markdown
## Feature: [Name]

### Problem
What problem does this solve? For whom?

### Success Criteria
- [ ] Criterion 1 (testable, specific)
- [ ] Criterion 2
- [ ] Criterion 3

### Out of Scope
- Thing we are NOT doing
- Another thing excluded

### Implementation Plan
1. Step 1 (one increment)
2. Step 2
3. Step 3

### Open Questions
- Question that needs answering before/during implementation
```

## Rules

- **Spec before code** — never start implementing without a written spec
- **Testable criteria** — each success criterion must be verifiable
- **Explicit out-of-scope** — prevents scope creep during implementation
- **Open questions first** — resolve unknowns before coding, not during

## Red Flags

- Starting to code before spec is written
- Success criteria that are vague ("should work well")
- No out-of-scope section
- Spec written after implementation

---
*Source: addyosmani/agent-skills — imported 2026-04-29*
