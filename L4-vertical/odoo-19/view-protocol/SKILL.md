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
     EREDITA: project.task.form  ->  ref="project.view_task_form2"
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
| Emoji negli attributi XML | Fragile con encoding/export | Solo nel testo visibile all'utente |

---

## 4. Index viste nel README del modulo

Ogni modulo che definisce viste su **modelli nativi Odoo** deve avere una sezione `## Viste` nel README.

Vedi esempio completo in `JOB_PORTAL_MASTER.md` sezione 7.

---

## 5. VIEWS_MASTER.md — registro centrale

Esiste un file centrale che mappa **tutte** le viste custom su modelli nativi:
`/opt/odoo19/custom/addons/VIEWS_MASTER.md`
Backup: `astrotourism/skills-astro/docs/VIEWS_MASTER.md`

**Quando aggiornarlo**: ogni volta che aggiungi, modifichi o rimuovi una vista su un modello nativo Odoo.

**Cosa aggiornare**: la riga della tabella del modello corretto (xpath, cosa aggiunge, controllo funzionale).

---

## 6. Workflow di modifica vista

```
1. Modifica il file XML nel modulo
2. Bump versione manifest
3. update_module
4. Verifica log: nessun errore RelaxNG o duplicati
5. Aggiorna CHANGELOG
6. Aggiorna README modulo (sezione Viste) se vista su modello nativo
7. Aggiorna VIEWS_MASTER.md       ← OBBLIGATORIO per viste su modelli nativi
8. Commit GitHub
```

**Mai:**
```
❌ Modificare arch_db via SQL diretto
❌ Usare Website Builder su viste di moduli custom backend
❌ Creare viste via ORM senza poi cristallizzarle in XML
❌ Dimenticare di aggiornare VIEWS_MASTER.md
```

---

## 7. Recupero vista orfana esistente

```python
# 1. Estrai external ID padre
SELECT module, name FROM ir_model_data
WHERE model = 'ir.ui.view' AND res_id = <inherit_id>;

# 2. Estrai arch attuale + backup modulo
# 3. Crea file XML con contenuto estratto + intestazione protocollo
# 4. update_module
# 5. Se external ID non registrato automaticamente:
INSERT INTO ir_model_data (module, name, model, res_id, noupdate)
VALUES ('modulo', 'view_nome', 'ir.ui.view', <id>, false);
# 6. Aggiorna VIEWS_MASTER.md
```

---

## 8. Checklist pre-deploy vista

```
[ ] External ID nel record XML
[ ] File XML nel manifest sotto views/
[ ] inherit_id usa ref="module.external_id" (non eval numerico)
[ ] Commento intestazione (scopo, eredita, campi custom)
[ ] Sezioni commentate se arch > 30 righe
[ ] Verifica conflitti con altri moduli sullo stesso xpath (VIEWS_MASTER.md)
[ ] README modulo aggiornato (sezione Viste)
[ ] VIEWS_MASTER.md aggiornato
[ ] Manifest version bumped
[ ] CHANGELOG aggiornato
```

---
*Creato: 2026-05-03 — basato su esperienza con astro_guide_jobcall vista 7214*
*Repo: Skills-Universal/skills-universal/L4-vertical/odoo-19/view-protocol/SKILL.md*
