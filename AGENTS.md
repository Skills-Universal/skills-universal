# AGENTS.md — Skills Universal
*Standard cross-AI (Linux Foundation AAIF, dic 2025).*
*Aggiornabile da qualsiasi chat via GitHub MCP — non toccare il file nel project Claude.*

---

## Skill da caricare per task

| Task | Skill da leggere |
|---|---|
| Qualsiasi | `L1-foundations/kaizen/SKILL.md` + `L1-foundations/token-efficiency/SKILL.md` |
| Odoo 19 | `L4-vertical/odoo-19/SKILL.md` |
| Modifiche multi-file | `L1-foundations/incremental-implementation/SKILL.md` |
| Errori / debug | `L1-foundations/debugging-and-error-recovery/SKILL.md` |
| Feature nuova | `L1-foundations/spec-driven-development/SKILL.md` |
| Task complesso | `L1-foundations/planning-and-task-breakdown/SKILL.md` |
| UI / portale / form | `L1-foundations/frontend-ui-engineering/SKILL.md` |
| Input utente / auth | `L1-foundations/security-and-hardening/SKILL.md` |
| Decisione architetturale | `L1-foundations/documentation-and-adrs/SKILL.md` |

---

## Regole operative — Odoo / Hetzner

- Una chat = un modulo
- `backup_module` PRIMA di qualsiasi modifica
- `str_replace_file` per modifiche chirurgiche; `write_file` solo per file nuovi
- `search_addon_code` → `read_file start_line/end_line` — mai file interi
- Viste nei file XML, mai solo nel DB
- Manifest: `summary` valorizzato, `description` vuota o RST valido, versione `19.0.x.x.x`
- Non aggiornare version senza istruzione esplicita

---

## File di riferimento sul server Hetzner

- Pattern tecnici Odoo 19: `/opt/odoo19/custom/addons/ODOO19_DEV_NOTES.md`
- Flusso operativo: `/opt/odoo19/custom/addons/FLUSSO_OPERATIVO.md`

---

## Regola qualità di questo file

> Ogni riga deve superare il test: *"Rimuovendo questa riga, l'agente farebbe un errore che non può correggere da solo?"*
> Massimo 100 righe. Niente ridondanze, niente spiegazioni — solo istruzioni non inferibili dal codice.

---
*Aggiornato: 2026-04-29 — rinominato da CLAUDE.md a AGENTS.md (standard AAIF Linux Foundation)*
