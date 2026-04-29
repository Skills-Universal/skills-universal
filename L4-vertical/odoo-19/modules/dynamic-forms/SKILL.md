---
name: odoo-dynamic-forms
description: Analisi modulo marketplace dynamic_custom_odoo_form_builde su Odoo 19.
  Caricare quando si valuta se usare dynamic forms, si lavora su form portale clienti,
  si discute di astro_event_publication, form builder Odoo, wizard multistep portale,
  raccolta dati evento, embedding form in pagine Odoo.
source: custom — analisi Astronomitaly aprile 2026
created: 2026-04-29
layer: L4
---

# Dynamic Forms — Analisi modulo Odoo 19
*Modulo: `dynamic_custom_odoo_form_builde` v19.0.2.0.0*
*Analisi effettuata: aprile 2026 su Odoo 19 Enterprise*

## Struttura dati

```
dynamic.form                       ← il form (nome, campi, embed code)
  └── dynamic.form.field             ← campi (tipo, label, placeholder, required)
  └── dynamic.form.field.condition   ← logica show/hide condizionale
  └── dynamic.form.email.notification

dynamic.form.submission            ← ogni risposta ricevuta
  ├── form_data (JSON)               ← tutti i valori compilati
  ├── target_model                   ← modello Odoo collegato
  └── target_record_id               ← record specifico

dynamic.form.field.mapping         ← mappa campo → campo Odoo
```

## Come funziona l'embedding

Ogni form genera uno snippet JS incollabile in qualsiasi pagina HTML o portale Odoo:
```html
<script src="https://erp.example.com/dynamic-form/view/TOKEN.js"></script>
```
Le risposte vengono salvate come record `dynamic.form.submission` direttamente in Odoo.

## Tipi di campo supportati

`text`, `email`, `phone`, `select`, `textarea`, `date`, `checkbox`, `multi-select`
più condizioni show/hide basate su valori.

## Risposte salvate come JSON

```json
{"programma": "...", "descrizione": "...", "maltempo": "indoor"}
```

## Cosa NON fa nativamente

- **Accesso via token** — non gestisce link personalizzati con token temporanei
- **Multi-step** — form a singola pagina (si può strutturare con show/hide)
- **Trigger automatici** — non sa creare form al cambio stage task
- **Upload immagini ottimizzate** — nessuna integrazione Pillow
- **Dati pre-popolati da Odoo** — non mostra campi in sola lettura da record esistente
- **Mapping su modelli custom** — `field.mapping` è vuoto, non testato su modelli non standard

## Architettura ibrida consigliata

```
LAYER 1 — Dynamic Forms (no-code)
  Struttura form: campi, label, placeholder, opzioni select
  Modificabile via UI drag & drop senza programmazione
        ↓ on_submission (hook ORM)
LAYER 2 — modulo custom leggero
  Logica business: token, trigger stage, stati, WP REST API
  Cambia raramente, codice Python stabile
```

**Vantaggio:** chi non programma può modificare la struttura del form senza toccare il codice.

## Confronto approccio hardcoded vs Dynamic Forms

| Operazione | Hardcoded | Dynamic Forms |
|---|---|---|
| Aggiungere un campo | Script Python + arch_db | UI drag & drop |
| Cambiare un testo | Edit XML + sync DB | Edit diretto backend |
| Nuova opzione select | Edit XML + sync DB | Click backend |
| Logica trigger/email | Codice Python | Codice Python |
| Upload immagini | Codice Python | Codice Python |

## Domande aperte da verificare prima di migrare

1. **Token auth** — il link con token funziona con Dynamic Forms?
2. **Pre-popolamento** — i dati da record Odoo si mostrano in sola lettura?
3. **Multi-step** — è supportato o solo show/hide condizionale?
4. **Modelli custom** — `field.mapping` funziona con `astro.event.publication`?

## Contesto Astronomitaly

- `astro_event_publication` usa un wizard multistep custom (4 step, WYSIWYG, upload)
- Il form è disaccoppiato dal DB: modifiche via script Python diretti, non via XML
- Il modulo `dynamic_custom_odoo_form_builde` è installato ma non ancora usato
- Migrazione valutata ma non avviata — vedere `astrotourism/skills-astro/docs/`
  per TODO specifici

## Raccomandazione

Non buttare via il lavoro fatto su `astro_event_publication` — funziona.
La migrazione a Dynamic Forms è un miglioramento, non una correzione di bug.
Testare prima i 4 punti aperti in ambiente reale prima di decidere.

---
*Analisi originale: 2026-04-10 — migrata in skill: 2026-04-29*
*Risparmio: ~3.000 token di rianalisi ogni volta che il modulo viene valutato*
