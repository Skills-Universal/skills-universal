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
name: skill-name
description: One-line description for auto-detection
layer: L1|L2|L3|L4
source: original-repo/name or Custom
imported: YYYY-MM-DD
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

---

## Update policy — NO automatic sync

This repo contains **static copies** of skills imported from external repos.
External repos (addyosmani, unclecatvn, etc.) have NO access here.
Updates to original repos NEVER propagate automatically.

### Consequences

- Our additions and extensions are NEVER overwritten
- We must manually check for upstream improvements if desired
- The `source` and `imported` frontmatter fields tell us exactly what came from where

### When to check for upstream updates

Only when:
- A skill is producing wrong results on a known pattern
- The upstream repo announces a major revision
- We start a new major project that depends heavily on that skill

### How to update an imported skill

1. Read the current version from the original repo via GitHub MCP
2. Compare with our version
3. Apply only the parts that improve our usage
4. Keep our custom extensions (marked with `## Astronomitaly notes` or similar)
5. Update `imported` date in frontmatter
6. Commit with message: `feat: update [skill-name] from [source] — [what changed]`

---

## Extending imported skills

When adding our own knowledge to an imported skill, ALWAYS use a dedicated
section clearly marked as custom — never mix with imported content:

```markdown
---
source: addyosmani/agent-skills
imported: 2026-04-29
---

# [Original skill content here]
...

---
## Custom extensions — Astronomitaly/fabrizio-marra
*Added: YYYY-MM-DD*

[Our additions, lessons learned, specific patterns]
```

This makes it trivially easy to:
- See what is imported vs what is ours
- Update the imported part without losing our extensions
- Understand why we added something and when

---

## Importing from external repos

When importing a skill from an external repo (addyosmani, unclecatvn, etc.):
1. Read the source file via GitHub MCP
2. Copy the SKILL.md content
3. Add frontmatter with `source` and `imported` date
4. Condense if the original is very long — keep principles, cut verbosity
5. Add a `## Custom extensions` section only if we have something to add
6. Commit with message: `feat: import [skill-name] from [source]`

## Creating custom skills

When creating a skill from scratch (our own knowledge):
1. Set `source: custom — fabrizio-marra` in frontmatter
2. Base it on real patterns from actual sessions — not theory
3. Include concrete examples with tool names (read_file, str_replace_file, etc.)
4. Commit with message: `feat: add [skill-name] (custom)`

## Updating any skill

Skills can be updated from any Claude chat via GitHub MCP.
Always append to the bottom of the file:
`*Updated: YYYY-MM-DD — [what changed and why]*`
