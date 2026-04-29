---
name: documentation-and-adrs
description: Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.
source: addyosmani/agent-skills
imported: 2026-04-29
---

# Documentation and ADRs

## Overview

Document decisions, not just code. The most valuable documentation captures the *why* — context, constraints, trade-offs. Code shows *what*; documentation explains *why it was built this way*.

## When to Use

- Making a significant architectural decision
- Choosing between competing approaches
- Adding or changing a public API
- Shipping a feature that changes user-facing behavior
- When you find yourself explaining the same thing repeatedly

## ADR Template

Store in `docs/decisions/ADR-NNN-title.md`:

```markdown
# ADR-NNN: [Decision Title]

## Status
Accepted | Superseded by ADR-XXX | Deprecated

## Date
YYYY-MM-DD

## Context
What problem are we solving? What constraints apply?

## Decision
What did we decide?

## Alternatives Considered
### Option A
- Pros: ...
- Cons: ...
- Rejected because: ...

## Consequences
What are the results of this decision?
```

## Inline Documentation Rules

- Comment the *why*, not the *what*
- Never comment self-explanatory code
- Never leave TODO comments — do it now or create a ticket
- Never leave commented-out code — git has history
- Document known gotchas inline where they matter

## README Structure

```markdown
# Project Name
One-paragraph description.

## Quick Start
## Commands
## Architecture
## Contributing
```

## Changelog Format

```markdown
## [X.Y.Z] - YYYY-MM-DD
### Added
### Fixed  
### Changed
```

## Documentation for Agents

- **CLAUDE.md** — project conventions so agents follow them
- **Spec files** — keep updated so agents build the right thing
- **ADRs** — help agents understand past decisions (prevents re-deciding)
- **Inline gotchas** — prevent agents from known traps

## Red Flags

- Architectural decisions with no written rationale
- README that doesn't explain how to run the project
- Commented-out code instead of deletion
- TODO comments weeks old
- No ADRs for significant architectural choices

---
*Source: addyosmani/agent-skills — imported 2026-04-29*
