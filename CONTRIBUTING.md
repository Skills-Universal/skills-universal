# Contributing to Skills Universal

## How skills are organized

Each skill lives in its own folder:
```
L[N]-[layer]/[skill-name]/
  SKILL.md       — Main skill file (required)
  examples/      — Examples and case studies (optional)
  references/    — Reference material (optional)
```

## SKILL.md format

```markdown
---
title: Skill Name
description: One-line description for auto-detection
triggers: [keyword1, keyword2, keyword3]
layer: L1|L2|L3|L4
source: original-repo/name or Custom
updated: YYYY-MM-DD
---

## When to use this skill
...

## Core principles
...

## Patterns & examples
...

## Anti-patterns to avoid
...
```

## Importing from external repos

When importing a skill from an external repo (addyosmani, unclecatvn, etc.):
1. Copy the SKILL.md content
2. Add frontmatter with source attribution
3. Add any practical notes from real-world usage
4. Commit with message: `feat: import [skill-name] from [source]`

## Updating skills

Skills can be updated from any Claude chat via GitHub MCP.
Always add a note at the bottom: `*Updated: YYYY-MM-DD — [what changed]*`
