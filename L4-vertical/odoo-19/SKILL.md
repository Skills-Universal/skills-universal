---
name: odoo-19
description: Odoo 19 development knowledge base with 18 specialized guides covering Actions, Controllers, Data files, API Decorators, Field types, Manifest, Migration, Mixins, Model Methods, OWL, Performance, Reports, Security, Testing, Transactions, Translation, Views & XML. Use when writing, reviewing, or debugging any Odoo 19 Python or XML code.
source: unclecatvn/agent-skills
imported: 2026-04-29
custom_sections: true
---

# Odoo 19 Skill — Master Index

Master index for all Odoo 19 development guides.
Full guides available at: github.com/unclecatvn/agent-skills/skills/odoo-19.0/references/

## Quick Reference

| Topic | File | When to Use |
|---|---|---|
| Actions | odoo-19-actions-guide.md | Creating actions, menus, scheduled jobs, server actions |
| API Decorators | odoo-19-decorator-guide.md | Using @api decorators, compute fields, validation |
| Controllers | odoo-19-controller-guide.md | Writing HTTP endpoints, routes, web controllers |
| Data Files | odoo-19-data-guide.md | XML/CSV data files, records, shortcuts |
| Development | odoo-19-development-guide.md | Creating modules, manifest, reports, security, wizards |
| Field Types | odoo-19-field-guide.md | Defining model fields, choosing field types |
| Manifest | odoo-19-manifest-guide.md | __manifest__.py configuration, dependencies, hooks |
| Migration | odoo-19-migration-guide.md | Upgrading modules, data migration, version changes |
| Mixins | odoo-19-mixins-guide.md | mail.thread, activities, email aliases, tracking |
| Model Methods | odoo-19-model-guide.md | Writing ORM queries, CRUD operations, domain filters |
| OWL Components | odoo-19-owl-guide.md | Building OWL UI components, hooks, services |
| Performance | odoo-19-performance-guide.md | Optimizing queries, fixing slow code, preventing N+1 |
| Reports | odoo-19-reports-guide.md | QWeb reports, PDF/HTML, templates, paper formats |
| Security | odoo-19-security-guide.md | Access rights, record rules, field permissions |
| Testing | odoo-19-testing-guide.md | Writing tests, mocking, assertions, browser testing |
| Transactions | odoo-19-transaction-guide.md | Handling database errors, savepoints, UniqueViolation |
| Translation | odoo-19-translation-guide.md | Adding translations, localization, i18n |
| Views & XML | odoo-19-view-guide.md | Writing XML views, actions, menus, QWeb templates |

---

<!-- CUSTOM:START — non rimuovere questo marcatore -->
## Custom extensions — Odoo 19 manifest best practices
*Added: 2026-04-29*

### `description` vs `summary` — regola definitiva

In Odoo 19 il manifest ha due campi testuali distinti:

| Campo | Dove appare | Formato richiesto |
|---|---|---|
| `summary` | UI Odoo → lista App, card modulo backend | Testo semplice |
| `description` | Pagina dettaglio modulo in Settings → Apps | reStructuredText valido |

La `description` appare solo se si clicca sul singolo modulo in Settings → Apps.
Per moduli interni non distribuiti a terzi ha utilità quasi zero.

**Tre opzioni — tutte valide:**

```python
# OPZIONE A — consigliata per moduli interni (zero RST warning)
'summary': 'Breve descrizione visibile nel backend.',
'description': '',

# OPZIONE B — accettabile se si vuole documentazione in-app
'summary': 'Breve descrizione visibile nel backend.',
'description': """
Descrizione estesa del modulo.

Funzionalità
------------

* Feature 1
* Feature 2
""",

# OPZIONE C — da NON usare (genera RST warning nel log di update_module)
'description': 'Testo libero senza struttura RST.',
```

**Regole RST per evitare warning:**
- Riga vuota prima e dopo ogni lista
- Titoli sezione con `---` (almeno tanti `-` quanto i caratteri del titolo)
- Bullet con `*` non `-`
- Nessun rientro irregolare

**I RST warning non sono bloccanti** — il modulo si carica correttamente.
Sono solo rumore nel log che rende più difficile vedere warning veri.

**Versione** — formato obbligatorio: `19.0.x.x.x`
**License** — sempre presente: `LGPL-3`, `OPL-1`, o `AGPL-3`

### Riferimenti Astronomitaly-specifici

Pattern specifici del nostro setup non coperti dalle guide generali:
→ `/opt/odoo19/custom/addons/ODOO19_DEV_NOTES.md` su Hetzner

Casi di crisi documentati (viste orfane, noupdate, psycopg2, portal multisite):
→ Vedi sezione ERRORI FATALI in ODOO19_DEV_NOTES.md
<!-- CUSTOM:END -->

---
*Source: unclecatvn/agent-skills — imported 2026-04-29*
*Updated: 2026-04-29 — added manifest description/RST best practices*
