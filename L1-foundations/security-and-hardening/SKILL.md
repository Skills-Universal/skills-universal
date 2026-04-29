---
name: security-and-hardening
description: Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services.
source: addyosmani/agent-skills
imported: 2026-04-29
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
*Source: addyosmani/agent-skills — imported 2026-04-29*
