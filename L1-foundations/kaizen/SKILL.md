---
name: kaizen
description: Guide for continuous improvement, error proofing, and standardization. Use when improving code quality, refactoring, or discussing process improvements. Always applied for implementation, architecture, error handling, and workflow improvements.
source: sickn33/antigravity-awesome-skills
imported: 2026-04-29
---

# Kaizen: Continuous Improvement

## Overview

Small improvements, continuously. Error-proof by design. Follow what works. Build only what's needed.

**Core principle:** Many small improvements beat one big change. Prevent errors at design time, not with fixes.

## The Four Pillars

### 1. Continuous Improvement
- Make smallest viable change that improves quality
- One improvement at a time, verify each before next
- First: make it work. Second: make it clear. Third: make it efficient.
- Never try all three at once
- Always leave code better than you found it

### 2. Poka-Yoke (Error Proofing)
- Design systems that prevent errors at compile/design time
- Validate at system boundaries, once — then safe everywhere
- Fail fast and loudly with helpful messages
- Validate config at startup, not during requests
- Make invalid states unrepresentable (type system)

### 3. Standardized Work
- Follow existing codebase patterns — consistency over cleverness
- New pattern only if significantly better + team agreement
- Document the *why*, not the *what*
- Check CLAUDE.md / ODOO19_DEV_NOTES.md before introducing new patterns
- Automate standards: linters, type checks, tests, CI/CD

### 4. Just-In-Time (YAGNI)
- Implement only current requirements — no "just in case" features
- Simplest thing that works first
- Abstract only when pattern proven across 3+ cases (Rule of Three)
- Optimize only when measured, not assumed
- Delete speculative code

## Red Flags

- "I'll refactor it later" — never happens
- Validation after use instead of before
- "I prefer to do it my way" — ignoring existing patterns
- "We might need this someday" — YAGNI violation
- Optimizing without profiling first
- Big bang rewrites instead of incremental improvements

## Remember

Kaizen is: small improvements continuously, preventing errors by design, following proven patterns, building only what's needed.

Not: perfection on first try, massive refactoring, clever abstractions, premature optimization.

**Mindset:** Good enough today, better tomorrow. Repeat.

---
*Source: sickn33/antigravity-awesome-skills — imported 2026-04-29*
