---
name: security-and-hardening
description: Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.
source: addyosmani/agent-skills
imported: 2026-04-29
custom_sections: true
---

# Security and Hardening

## Overview

Security-first development. Treat every external input as hostile, every secret as sacred, every authorization check as mandatory.

## When to Use

- Building anything that accepts user input
- Implementing authentication or authorization
- Storing or transmitting sensitive data
- Integrating with external APIs or services
- Handling payment or PII data

## The Three-Tier Boundary

### Always Do
- Validate all external input at system boundary
- Parameterize all database queries — never concatenate user input into SQL
- Encode output to prevent XSS
- Use HTTPS for all external communication
- Hash passwords with bcrypt/scrypt/argon2
- Set security headers (CSP, HSTS, X-Frame-Options)
- Use httpOnly, secure, sameSite cookies

### Never Do
- Never commit secrets to version control
- Never log sensitive data (passwords, tokens)
- Never trust client-side validation as security boundary
- Never disable security headers for convenience
- Never use eval() or innerHTML with user-provided data
- Never expose stack traces to users

## Secrets Management

```
.env files:
  .env.example  → Committed (template with placeholders)
  .env          → NOT committed (real secrets)
  .env.local    → NOT committed (local overrides)
```

## Security Review Checklist

- [ ] Passwords hashed (salt rounds ≥ 12)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Every endpoint checks permissions
- [ ] All user input validated at boundary
- [ ] SQL queries parameterized
- [ ] No secrets in code or version control
- [ ] Security headers configured
- [ ] Error messages don't expose internals

## Red Flags

- User input passed directly to DB queries or HTML
- Secrets in source code or commit history
- API endpoints without auth checks
- Missing CORS configuration
- No rate limiting on auth endpoints

---

<!-- CUSTOM:START — non rimuovere questo marcatore -->
## Separazione pubblico/privato nei repository AI
*Added: 2026-04-29*

Quando si organizza conoscenza su GitHub per alimentare agenti AI, applicare
la stessa logica dei segreti: **mai mescolare conoscenza universale e dati riservati
nello stesso repository.**

### La regola

| Tipo di contenuto | Dove va |
|---|---|
| Pattern tecnici, best practices, guide | Repository pubblico o privato universale |
| IP server, credenziali DB, path interni | Project Claude (mai su GitHub) |
| URL interni, nomi database, token API | Project Claude o repo privato aziendale |
| Pipeline operative, workflow aziendali | Repository privato aziendale |
| Dati personali, informazioni clienti | Mai in nessun repository |

### Struttura corretta per progetti multi-repo

```
skills-universal/          ← pubblico o privato — ZERO info riservate
  AGENTS.md                ← regole operative generiche
  L1-foundations/          ← best practices universali
  L4-vertical/odoo-19/     ← pattern tecnici Odoo (senza IP/path specifici)

skills-[azienda]/          ← sempre PRIVATO
  AGENTS.md                ← istruzioni con dati infrastruttura
  AGENTS.infra.md          ← IP, path, DB, configurazioni server
  AGENTS.business.md       ← workflow aziendali riservati

project Claude (CLAUDE.md) ← mai su GitHub
  contesto fisso            ← IP, URL, connettori MCP specifici
```

### Test prima di fare commit su GitHub

Prima di ogni push, chiediti:
> *"Se questo file fosse pubblico domani, ci sarebbe qualcosa che non voglio che il mondo veda?"*

Se sì → il file non appartiene a GitHub. Va nel project Claude o in un file
sul server accessibile solo tramite connettori autenticati (Astro MCP Bridge).

### Errori comuni

- Mettere IP server o path assoluti in `AGENTS.md` pubblico
- Inserire nomi di database o credenziali in skill files
- Documentare architettura interna (nomi moduli, struttura ERP) in repo pubblici
- Caricare `.docx` con dati di installazione nel project invece di migrarli
  in un file `.md` versionato in un repo privato aziendale
<!-- CUSTOM:END -->

---
*Source: addyosmani/agent-skills — imported 2026-04-29*
*Updated: 2026-04-29 — added public/private repository separation rule*
