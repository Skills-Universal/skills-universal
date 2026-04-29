# Skills Universal

Universal knowledge repository for Claude agent skills.
Modular, composable, reusable across projects.

## Architecture

```
L1-foundations/     — Universal principles (UX, security, methodology, Kaizen)
L2-development/     — General software development (debugging, planning, spec-driven)
L3-infrastructure/  — Tooling & integrations (Docker, Nginx, MCP servers)
L4-vertical/        — Domain-specific (Odoo 19, WordPress, Social)
```

## Usage

Skills are loaded on demand via GitHub MCP in any Claude chat.
Each skill's `SKILL.md` contains triggers that activate it automatically
when the task matches.

Business-specific knowledge lives in separate private repos
that reference this one for L1-L4.

## Contributing

See `CONTRIBUTING.md` for import policy, update rules, and custom section protection.

Skills are imported from best-in-class public repositories and extended with
practical lessons learned. Sources credited in each skill file.

---
*Maintained by Fabrizio Marra — last updated: 2026-04-29*
