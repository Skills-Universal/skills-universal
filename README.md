# Skills Universal

Universal knowledge repository for Claude agent skills.
Modular, composable, reusable across all projects and businesses.

## Architecture

```
L1-foundations/     — Universal principles (UX, security, methodology, Kaizen)
L2-development/     — General software development (debugging, planning, spec-driven)
L3-infrastructure/  — Tooling & integrations (Docker, Nginx, MCP servers)
L4-vertical/        — Domain-specific (Odoo 19, WordPress, Postiz/Social)
```

## Usage

Each business has its own private `skills-[business]` repo containing only
business-specific knowledge (L5). That repo references this one for L1-L4.

In any Claude chat, both repos are readable via GitHub MCP — no manual loading needed.

## Business repos

| Business | Repo | Visibility |
|---|---|---|
| Astronomitaly | skills-astronomitaly (TBD) | Private |
| Vivere Senza Stomaco | skills-vss (TBD) | Private |
| Fabiana Rossetti | skills-fabiana (TBD) | Private |
| FM Consulting | skills-fm-consulting (TBD) | Private |

## Contributing

Skills are imported from best-in-class public repositories and extended with
practical lessons learned. Sources credited in each skill file.

---
*Maintained by Fabrizio Marra — last updated: 2026-04-29*
