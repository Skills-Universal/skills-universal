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
## Custom extensions — Viste XML-first: gate obbligatorio
*Added: 2026-05-02*

### Regola universale — mai viste solo nel DB

**Principio:** ogni vista Odoo deve avere un `external_id` registrato in `ir.model.data`.
Senza external ID, la vista esiste solo nel DB ed è vulnerabile a perdita ad ogni `update_module`.

**Gate obbligatorio — eseguire PRIMA di toccare qualsiasi vista, esistente o nuova:**

```sql
SELECT id FROM ir_model_data
WHERE model = 'ir.ui.view' AND res_id = <VIEW_ID>;
```

| Risultato | Azione |
|---|---|
| **Non vuoto** | Vista ha external ID → modificarla normalmente via XML ✅ |
| **Vuoto** | Vista orfana → **STOP. NON modificare via SQL diretto.** |

**Procedura obbligatoria per viste orfane:**
1. Leggere `arch_db` attuale: `SELECT arch_db FROM ir_ui_view WHERE id = <ID>`
2. Creare in XML nel modulo:
```xml
<record id="view_my_model_form_custom" model="ir.ui.view">
    <field name="name">my.model.form.custom</field>
    <field name="model">my.model</field>
    <field name="inherit_id" ref="base_module.view_to_inherit"/>
    <field name="arch" type="xml">
        <!-- contenuto attuale dal DB -->
    </field>
</record>
```
3. Fare `update_module` per registrare l'external ID
4. Verificare che `ir_model_data` ora contenga il record
5. Solo dopo: modificare via XML normalmente

**Perché questo problema esiste:**
- Le viste create via ORM (`ir.ui.view.create()`) senza `xml_id` non hanno external ID
- Le viste create via script SQL ovviamente nemmeno
- `update_module` può sovrascrivere viste orfane se trova una vista XML con lo stesso `name`
- Il Website Builder di Odoo crea spesso viste orfane — mai fidarsi che siano al sicuro

**Nessuna eccezione per urgenza o rapidità.** Il costo di cristallizzare la vista è basso;
il costo di perderla e ricostruirla è alto.

---

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

---

## Custom extensions — message_post HTML rendering
*Added: 2026-04-29*

### Markup() obbligatorio per HTML nel chatter — regola critica

**Sintomo:** il chatter mostra il testo con tag HTML visibili come testo grezzo
(`<strong>Titolo</strong>` invece di **Titolo**).

**Causa:** Odoo escapa automaticamente le stringhe Python normali nel `body`
di `message_post()`. Solo gli oggetti `Markup` vengono renderizzati come HTML.

```python
# ✅ CORRETTO — HTML renderizzato correttamente nel chatter
from markupsafe import Markup

task.message_post(
    body=Markup(
        '<p><strong>Titolo</strong></p>'
        '<p>Testo con <em>%s</em> e <a href="%s">link</a></p>'
    ) % (valore_variabile, url),
    subtype_xmlid='mail.mt_comment',
    partner_ids=partner_ids,
)

# ❌ SBAGLIATO — mostra tag HTML come testo grezzo
task.message_post(
    body='<strong>Titolo</strong> — testo',  # stringa normale
    ...
)

# ❌ SBAGLIATO — anche con f-string
task.message_post(
    body=f'<strong>{titolo}</strong>',  # f-string non è Markup
    ...
)
```

**Pattern consolidato (verificato in produzione):**

```python
from markupsafe import Markup

# Blocchi HTML statici → stringa Markup diretta
body = Markup('<p><strong>GO confermato.</strong> Evento all\'orario previsto.</p>')

# Con variabili → Markup() con % interpolation
body = Markup(
    '<p><strong>%s</strong></p>'
    '<ul>'
    '<li>Valore: <strong>%s</strong></li>'
    '</ul>'
) % (titolo, valore)

# Con parti condizionali
parte_opzionale = Markup('<li>Extra: %s</li>') % extra if extra else Markup('')
body = Markup('<p>Testo</p><ul>%s</ul>') % parte_opzionale
```

**Regole:**
- Importare sempre `from markupsafe import Markup` a inizio file
- Mai usare f-string con HTML — usare `Markup(...) % (vars,)`
- Per parti condizionali: usare `Markup('')` come fallback, non stringa vuota `''`
- Le emoji Unicode dirette (🎯 📋) funzionano in Markup senza encoding HTML

<!-- CUSTOM:END -->

---
*Source: unclecatvn/agent-skills — imported 2026-04-29*
*Updated: 2026-05-02 — added XML-first gate for orphan views*
