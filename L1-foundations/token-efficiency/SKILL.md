---
name: token-efficiency
description: Reduces token consumption in Claude.ai sessions with MCP connectors. Use at the start of every session and when planning multi-step tasks. Especially relevant for long Odoo development sessions, file operations on Hetzner, and GitHub MCP workflows.
source: custom — Astronomitaly/fabrizio-marra
created: 2026-04-29
---

# Token Efficiency

## Overview

Token efficiency in Claude.ai is fundamentally different from Claude Code.
The only levers available are: **what goes into context**, **when it goes in**, and **how much of it**.

**Core principle:** Load context just-in-time, not up-front.

---

## Rule 1 — Never load a full file when you need only part of it

```
read_file('ODOO19_DEV_NOTES.md', start_line=1, end_line=80)  # GOOD
read_file('ODOO19_DEV_NOTES.md')                              # BAD — 500 lines
```

Use `search_addon_code` to find the relevant lines first, then `read_file` con `start_line`/`end_line`.

---

## Rule 2 — Use search before read

```
search_addon_code('def _compute_status', addon_name='astro_guide')  # trova le righe
read_file('models/guide.py', start_line=142, end_line=165)           # legge solo quelle
```

---

## Rule 3 — One tool call per question

No exploratory calls "just to check". Every result entra nel context e non esce mai.

---

## Rule 4 — str_replace_file over write_file for small changes

`str_replace_file` → solo la stringa cambiata entra nel context.
`write_file` → solo per file nuovi o ristrutturazione completa.

---

## Rule 5 — Load devnotes once per session, not per task

ODOO19_DEV_NOTES.md è ~500 righe. Leggerlo una volta sola per sessione,
solo la sezione rilevante. Per sessioni brevi, usare `search_addon_code` direttamente.

---

## Rule 6 — GitHub MCP: fetch only the file you need

Skill files hanno path prevedibili. Fetcha direttamente senza browsare la directory.

---

## Rule 7 — Avoid redundant project_knowledge_search

Non cercare cose già in context, ovvie, o disponibili più velocemente sul server.

---

## Rule 8 — Prefer psql queries over ORM reads for data exploration

`run_psql('SELECT id, name FROM astro_guide LIMIT 5')` → output compatto.
`execute_method search_read` → dizionari ORM verbosi, 8x più token.

---

## Rule 9 — Plan before tool calls

Prima di qualsiasi tool call, scrivi il piano:
- Cosa serve leggere (con righe)
- Quante chiamate stimate
- Ordine di esecuzione

---

## Rule 10 — Close long sessions proactively

Sintomi: risultati troncati, risposte lente, riferimenti a cose vecchie.
Azione: salva stato su server, apri nuova chat, carica solo il necessario.

---

## Rule 11 — Batch GitHub pushes

Un solo `push_files` con array di file invece di N chiamate separate.

---

## Rule 12 — exec_python_file for multi-step DB operations

Un solo script Python che fa tutto in una transazione invece di N `execute_method`.

---

## Rule 13 — Skip skills loading for simple/known tasks

Non caricare skill per: fix typo XML, aggiungere campo noto, leggere log, query SQL semplice.
Caricare skill per: nuova architettura, pagina portale, migration script.

---

## Rule 14 — Compress session notes

4-6 righe bastano per riprendere una sessione: decisione, cosa fatto, prossimo step, pendente.

---

## Rule 15 — One module per chat

Cross-module work moltiplica il context. Se servono due moduli: due chat separate.

---

## Rule 16 — AGENTS.md / CLAUDE.md: massimo 100 righe

*Basato su ricerca ETH Zurich (Gloaguen et al., feb 2026) su 138 task reali:*
- File generati da AI riducono il successo dei task del ~3%
- File scritti a mano migliorano di ~4%
- Includere questi file aumenta i costi di inferenza del +20%

**Il test per ogni riga:**
> *"Rimuovendo questa riga, l'agente farebbe un errore che non può correggere da solo?"*

Se la risposta è no → elimina la riga. Il codice spiega il codice.
Non ridondare documentazione già presente nei file sorgente.
Non spiegare convenzioni standard che l'AI già conosce.
Solo istruzioni **non inferibili** dal contesto e dal codice.

---

## Token Cost Reference (approximate, claude.ai)

| Operation | Tokens |
|---|---|
| read_file 500 righe | ~3,000 |
| read_file 50 righe | ~300 |
| search_addon_code | ~200 |
| run_psql 5 righe | ~100 |
| execute_method 10 record | ~800 |
| project_knowledge_search | ~1,500 |
| GitHub get_file_contents medio | ~2,000 |

Target per sessione: sotto 30,000 token totali.

---
*Source: custom — Astronomitaly/fabrizio-marra*
*Updated: 2026-04-29 — added Rule 16 AGENTS.md 100-line test*
