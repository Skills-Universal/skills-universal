# CLAUDE.md — Skills Universal
*Questo file viene letto automaticamente da Claude all'inizio di ogni sessione.*
*Aggiornabile da qualsiasi chat via GitHub MCP senza toccare il project Claude.*

---

## Istruzioni operative

Prima di qualsiasi task di sviluppo:

1. **Task Odoo 19** → leggi `L4-vertical/odoo-19/SKILL.md`
2. **Task con modifiche a più file** → leggi `L1-foundations/incremental-implementation/SKILL.md`
3. **Task con errori/debug** → leggi `L1-foundations/debugging-and-error-recovery/SKILL.md`
4. **Feature nuova o ambigua** → leggi `L1-foundations/spec-driven-development/SKILL.md`
5. **Task complesso o lungo** → leggi `L1-foundations/planning-and-task-breakdown/SKILL.md`
6. **Task con UI/portale** → leggi `L1-foundations/frontend-ui-engineering/SKILL.md`
7. **Qualsiasi task** → applica `L1-foundations/kaizen/SKILL.md` e `L1-foundations/token-efficiency/SKILL.md`

---

## Regole universali sempre attive

- Una chat = un modulo Odoo
- `backup_module` PRIMA di qualsiasi modifica
- `str_replace_file` per modifiche chirurgiche, `write_file` solo per file nuovi
- `search_addon_code` prima di `read_file`
- `read_file` con `start_line`/`end_line` — mai leggere file interi
- Viste vivono nei file XML, mai solo nel DB
- `summary` valorizzato, `description` vuota o RST valido nel manifest
- Versione manifest formato `19.0.x.x.x`
- Non aggiornare version senza istruzione esplicita

---

## File di riferimento sul server Hetzner

| Cosa | Path |
|---|---|
| Pattern tecnici Odoo 19 | `/opt/odoo19/custom/addons/ODOO19_DEV_NOTES.md` |
| Flusso operativo 7 passi | `/opt/odoo19/custom/addons/FLUSSO_OPERATIVO.md` |
| Troubleshooting GitHub MCP | `/opt/odoo19/custom/addons/GITHUB_MCP_TROUBLESHOOTING.md` |

---

## Skill disponibili

### L1 — Foundations
| Skill | Path | Quando |
|---|---|---|
| incremental-implementation | L1-foundations/incremental-implementation/SKILL.md | Modifiche multi-file |
| debugging-and-error-recovery | L1-foundations/debugging-and-error-recovery/SKILL.md | Errori e debug |
| spec-driven-development | L1-foundations/spec-driven-development/SKILL.md | Feature nuove |
| planning-and-task-breakdown | L1-foundations/planning-and-task-breakdown/SKILL.md | Task complessi |
| security-and-hardening | L1-foundations/security-and-hardening/SKILL.md | Input utente, auth |
| documentation-and-adrs | L1-foundations/documentation-and-adrs/SKILL.md | Decisioni architetturali |
| frontend-ui-engineering | L1-foundations/frontend-ui-engineering/SKILL.md | UI, portale, form |
| kaizen | L1-foundations/kaizen/SKILL.md | Sempre |
| token-efficiency | L1-foundations/token-efficiency/SKILL.md | Sempre |

### L4 — Vertical
| Skill | Path | Quando |
|---|---|---|
| odoo-19 | L4-vertical/odoo-19/SKILL.md | Qualsiasi task Odoo |

---
*Aggiornato: 2026-04-29*
*Per aggiornare questo file: GitHub MCP → create_or_update_file su Skills-Universal/skills-universal/CLAUDE.md*
