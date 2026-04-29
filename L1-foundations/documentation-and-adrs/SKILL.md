---
name: documentation-and-adrs
description: Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase.
source: addyosmani/agent-skills
imported: 2026-04-29
custom_sections: true
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

- **CLAUDE.md / AGENTS.md** — project conventions so agents follow them
- **Spec files** — keep updated so agents build the right thing
- **ADRs** — help agents understand past decisions (prevents re-deciding)
- **ALERTS.md** — per-module critical rules agents must read before working on that module
- **Inline gotchas** — prevent agents from known traps

## Red Flags

- Architectural decisions with no written rationale
- README that doesn't explain how to run the project
- Commented-out code instead of deletion
- TODO comments weeks old
- No ADRs for significant architectural choices

---

<!-- CUSTOM:START — non rimuovere questo marcatore -->
## Module design principles — Odoo / custom development
*Added: 2026-04-29*

### Group related functionality in thematic modules

Avoid creating overly specific modules for a single function.
Group everything that belongs to the same operational domain in one module.

**Anti-pattern:**
```
astro_recruitment_sign/   ← only contracts
astro_recruitment_stages/ ← only stages
astro_recruitment_email/  ← only emails
```

**Correct pattern:**
```
astro_recruitment/   ← recruiting + sign + stages + onboarding + emails
astro_mail_templates/ ← ALL email template customizations in one place
```

**Rule:** if a function concerns the same operational domain, it belongs to the same module.

### Always track configuration in code, never only in DB

Any customization applied via ORM/UI directly to the DB (mail templates,
ir.ui.view modifications, ir.config_parameter) must be mirrored in an XML
file in a custom module with `noupdate="1"`.

If it's only in the DB, it will be lost on restore, upgrade, or reinstall.

```xml
<!-- Always in a custom module data/ folder -->
<odoo>
    <data noupdate="1">
        <record id="..." model="mail.template">
            <field name="body_html">...</field>
        </record>
    </data>
</odoo>
```

### ALERTS.md — per-module critical rules

Every module with non-obvious critical constraints should have an `ALERTS.md`
file in its root. Agents must check for and read this file before working
on the module.

```
modulo/
├── __manifest__.py
├── README.md      ← what it does, dependencies, how to install
├── CHANGELOG.md   ← version history
└── ALERTS.md      ← ⚠️ critical rules, locks, architectural decisions
```

ALERTS.md content: field locks, known incidents, decisions that cannot be
reversed, SOA for configurations that live only in the DB.
<!-- CUSTOM:END -->

---
*Source: addyosmani/agent-skills — imported 2026-04-29*
*Updated: 2026-04-29 — added module design principles and ALERTS.md pattern*
