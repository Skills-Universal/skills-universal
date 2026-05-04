# SKILL — Smart Alerts / Banner in Form Odoo 19
*Patterns per posizionare e implementare banner/alert nelle form Odoo 19.*

---

## Anatomia form — zona ottimale

```xml
<form>
  <header>...</header>
  <sheet>
    <div name="button_box"/>   ← smart buttons

    ★ ZONA ALERT OTTIMALE      ← subito DOPO button_box
                                  visibili senza scroll

    <div class="oe_title"/>
    <group>...</group>
    <notebook>...</notebook>
  </sheet>
</form>
```

**Xpath corretto:**
```xml
<xpath expr="//div[@name='button_box']" position="after">
    <div class="alert alert-warning" role="alert"
         invisible="condizione">
        Testo avviso
    </div>
</xpath>
```

**Xpath sbagliato** (alert finisce in fondo, nascosto):
```xml
<!-- NON usare -->
<xpath expr="//sheet/notebook" position="before">...</xpath>
<xpath expr="//sheet" position="inside">...</xpath>
```

---

## Classi CSS disponibili

| Classe | Colore | Uso |
|---|---|---|
| `alert alert-warning` | 🟡 Giallo | Info mancante, azione richiesta |
| `alert alert-danger` | 🔴 Rosso | Errore bloccante, campo critico |
| `alert alert-info` | 🔵 Blu | Informazione contestuale |
| `alert alert-success` | 🟢 Verde | Conferma stato positivo |

---

## Template pronti

### Alert giallo con pulsante
```xml
<div class="alert alert-warning" role="alert"
     invisible="condizione_per_nascondere">
    <strong>⚠️ Titolo</strong> — Descrizione.
    <button name="nome_metodo" type="object"
            string="+ Azione"
            class="btn btn-sm btn-warning ms-3"/>
</div>
```

### Alert rosso con icona e campo inline
```xml
<div class="alert alert-danger d-flex align-items-start gap-2"
     role="alert"
     invisible="not campo_warning">
    <i class="fa fa-exclamation-triangle fa-lg mt-1"/>
    <div>
        <strong>Titolo errore</strong> —
        <field name="campo_warning" readonly="1" class="d-inline"/>
        <button name="nome_metodo" type="object"
                string="Azione →"
                class="btn btn-sm btn-danger ms-2"/>
    </div>
</div>
```

### Alert semplice senza pulsante
```xml
<div class="alert alert-info" role="alert"
     invisible="condizione">
    <i class="fa fa-info-circle me-1"/>
    Testo informativo.
</div>
```

---

## Regole `invisible` in Odoo 19

```xml
invisible="not campo_nome"            <!-- campo vuoto/falsy → mostra alert -->
invisible="campo_nome"                <!-- campo valorizzato → nascondi -->
invisible="state != 'draft'"          <!-- su selection/state -->
invisible="job_call_count == 0"       <!-- su integer -->
invisible="not job_call_warning"      <!-- su computed char -->
```

> ⚠️ NON usare `invisible="campo != False"` — non funziona in Odoo 19.

---

## Stack di alert multipli

```xml
<xpath expr="//div[@name='button_box']" position="after">
    <div class="alert alert-warning" role="alert"
         invisible="condizione_A_falsa">Alert A</div>
    <div class="alert alert-danger" role="alert"
         invisible="condizione_B_falsa">Alert B</div>
</xpath>
```
Odoo mostra/nasconde indipendentemente — solo quelli con condizione soddisfatta vengono renderizzati.

---

## Campi computed che alimentano gli alert

Pattern Astronomitaly — campi `store=False` su `project.task`:
```python
job_call_warning = fields.Char(compute='_compute_alerts', store=False)
guide_assignment_warning = fields.Char(compute='_compute_alerts', store=False)

@api.depends('stage_id', 'x_studio_guides_needed', ...)
def _compute_alerts(self):
    for task in self:
        # logica graduata
        if ...:
            task.guide_assignment_warning = "Nessuna guida disponibile"
        else:
            task.guide_assignment_warning = False
```

---

## Alert su form senza button_box

Se il form non ha `button_box`, usare:
```xml
<xpath expr="//sheet" position="inside">
    <!-- all'inizio dello sheet -->
</xpath>
```
oppure direttamente nel `<sheet>` prima del `<div class="oe_title">`.

---
*Skill creata: 2026-05-04 — estratta da SMART_ALERTS_MASTER.md e ODOO19_DEV_NOTES*
