# SKILL — Protocollo Viste Odoo 19
*Astronomitaly / Skills-Universal — approvato 2026-05-03*
*Applicare a tutti i moduli `astro_*`*

---

## Regola fondamentale: XML-first

> **Mai creare o modificare viste solo nel DB.**
> Ogni vista deve avere un file XML nel modulo e un external ID registrato in `ir_model_data`.
> Violazione = VISTE-N nel MASTER_TODO con priorità 🔴.

Perché:
- Viste solo-DB non sono versionabili
- `update_module` le ignora → duplicati silenti
- Se il DB viene corrotto → persa senza recovery
- Non compaiono nel CHANGELOG → storia invisibile

---

## 1. Naming convention

### External ID
Schema: `<modulo>.<view_modello_tipo_funzione>`

```
astro_guide_jobcall.view_task_form_jobcall_tab
astro_guide_jobcall.view_task_form_jobcall_alerts
astro_event_stages.view_task_form_meteo_banner
astro_guide_matching.view_task_form_matching_tab
astro_receipt.view_task_form_receipt_button
```

Regole:
- `modello` = parte significativa (`task`, `sale`, `lead`, `invite`)
- `tipo` = `form` / `list` / `search` / `kanban`
- `funzione` = cosa aggiunge (`tab`, `banner`, `button`, `alerts`, `fields`)
- Tutto lowercase, underscore, niente abbreviazioni creative

### `name` field (nome tecnico Odoo)
Convenzione esistente: `modello.tipo.modulo.funzione`
```
project.task.form.job.call.tab
project.task.form.meteo.banner
astro.guide.invite.form
```

### File XML
Un file per modello target:
```
views/project_task_views.xml      ← tutte le viste su project.task
views/sale_order_views.xml        ← tutte le viste su sale.order
views/astro_job_call_views.xml    ← viste sul modello proprio del modulo
```

---

## 2. Struttura del file XML

### Intestazione file
```xml
<?xml version="1.0" encoding="utf-8"?>
<!--
    <nome_modulo>/views/<nome_file>.xml
    Viste su: <modello Odoo target>

    Contiene:
      - view_task_form_jobcall_tab    : tab Job Call + alert + smart buttons
      - view_task_form_jobcall_search : filtri rapidi JC (futuro)

    Regola: modificare sempre manifest version + CHANGELOG dopo ogni cambio.
-->
<odoo>
    ...
</odoo>
```

### Intestazione record (commento sopra ogni `<record>`)
```xml
<!-- ============================================================
     VISTA: view_task_form_jobcall_tab
     SCOPO: Tab "Job Call" + alert banner + smart buttons
            sulla form task (PRENOTAZIONI PRIVATE/EVENTI)
     EREDITA: project.task.form  →  ref="project.view_task_form2"
     MODULO: astro_guide_jobcall — introdotta in v19.0.1.48.0
     CAMPI CUSTOM RICHIESTI:
       x_job_call_enabled, job_call_count, job_call_state,
       job_call_warning, has_pending_direct_assign,
       guides_confirmed_count, guides_assigned_count, receipt_count
     NOTA: cristallizzata da vista orfana DB id=7214 il 2026-05-03
     ============================================================ -->
<record id="view_task_form_jobcall_tab" model="ir.ui.view">
```

### Sezioni nell'arch
Per viste > 30 righe, commentare ogni xpath con `=== NOME ===`:
```xml
<field name="arch" type="xml">
    <data>
        <!-- === 1. SMART BUTTONS (button_box header) === -->
        <xpath expr="//div[@name='button_box']" position="inside">
            ...
        </xpath>

        <!-- === 2. ALERT BANNER (sotto button_box) === -->
        <!-- Alert giallo: JC mancante -->
        <!-- Alert rosso: JC non pubblicata -->
        <xpath expr="//div[@name='button_box']" position="after">
            ...
        </xpath>

        <!-- === 3. TAB JOB CALL (notebook) === -->
        <xpath expr="//notebook" position="inside">
            <page string="Job Call" name="job_call_tab">
                ...
            </page>
        </xpath>
    </data>
</field>
```

---

## 3. Cosa NON mettere nei commenti XML

| Non mettere | Perché | Dove va invece |
|---|---|---|
| Version history completa | Diventa stale, duplica CHANGELOG | `CHANGELOG.md` del modulo |
| "Viste che dipendono da questa" | Impossibile mantenere | Non documentare |
| Tutti i campi (ovvi inclusi) | Rumore | Solo campi custom non ovvi |
| Emoji negli attributi XML (`string=`, `name=`) | Fragile con encoding/export | Solo nel testo visibile all'utente |

---

## 4. Index viste nel README del modulo

Ogni modulo che definisce viste su **modelli nativi Odoo** (non solo i propri modelli)
deve avere una sezione `## Viste` nel README:

```markdown
## Viste

### Viste su modelli esterni

| External ID | Modello | Tipo | Cosa aggiunge |
|---|---|---|---|
| `view_task_form_jobcall_tab` | `project.task` | form | Tab Job Call + alert banner + smart buttons |
| `view_sale_order_jobcall_button` | `sale.order` | form | Smart button Job Call nel preventivo |
| `view_project_form_jobcall_settings` | `project.project` | form | Toggle abilitazione Job Call sul progetto |

### Viste sui modelli del modulo

| External ID | Modello | Tipo | Note |
|---|---|---|---|
| `view_job_call_list` | `astro.job.call` | list | Lista principale JC |
| `view_job_call_form` | `astro.job.call` | form | Form principale JC |
| `view_guide_invite_list` | `astro.guide.invite` | list | Lista invite/candidature |
| `view_guide_invite_form` | `astro.guide.invite` | form | Form invite |
```

**Perché l'index è utile:**
- Le viste sui modelli nativi sono le più rischiose (conflitti con altri moduli)
- In un modulo grande (astro_guide_jobcall ha 166 file) non si capisce cosa tocca cosa
- L'index dice subito "questo modulo modifica project.task in 3 punti"
- Utile per debugging: "questo tab non appare" → cerchi nell'index chi lo mette

**Quando NON serve:**
- Moduli piccoli (< 5 viste) che toccano solo i propri modelli
- In quel caso basta il commento nel file XML

---

## 5. Workflow di modifica vista

```
1. Modifica il file XML nel modulo
2. Bump versione manifest (es. 19.0.1.80.0 → 19.0.1.81.0)
3. button_immediate_upgrade sul modulo
4. Verifica nel log: nessun errore RelaxNG
5. Aggiorna CHANGELOG con descrizione modifica vista
6. Se il README ha index viste → aggiornarlo se cambia struttura
```

**Mai:**
```
❌ Modificare arch_db via SQL diretto
❌ Usare Website Builder su viste di moduli custom backend
❌ Creare viste via ORM senza poi cristallizzarle in XML
```

---

## 6. Recupero vista orfana esistente

Se esiste già una vista solo-DB da cristallizzare:

```python
# 1. Estrai external ID padre
SELECT module, name FROM ir_model_data
WHERE model = 'ir.ui.view' AND res_id = <inherit_id>;

# 2. Estrai arch attuale
SELECT arch_db FROM ir_ui_view WHERE id = <vista_id>;

# 3. Backup prima di toccare
backup_module('nome_modulo', label='pre_cristallizzazione_NNNNN')

# 4. Crea file XML con il contenuto estratto
# 5. Aggiungi al manifest in data/views
# 6. update_module
# 7. Verifica che ir_model_data ora abbia il record
SELECT id FROM ir_model_data
WHERE model = 'ir.ui.view' AND name = 'view_task_form_jobcall_tab';
```

---

## 7. Checklist pre-deploy vista

```
[ ] External ID presente nel record XML
[ ] File XML nel manifest sotto views/
[ ] inherit_id usa ref="module.external_id" (non eval numerico)
[ ] Commento intestazione presente (scopo, eredita, campi custom)
[ ] Sezioni commentate se > 30 righe
[ ] README aggiornato se vista su modello nativo
[ ] Manifest version bumped
[ ] CHANGELOG aggiornato
```

---
*Creato: 2026-05-03 — basato su esperienza con astro_guide_jobcall vista 7214*
*Repo: Skills-Universal/skills-universal/L4-vertical/odoo-19/view-protocol/SKILL.md*
