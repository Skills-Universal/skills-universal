# TODO — Sistema Email Astronomitaly
*Generato al termine della sessione 2026-04-30*

---

## 🔴 Alta priorità

### 1. Blacklist fetchmail in `astro_mail_forward`
**Modulo:** `astro_mail_forward`  
**Problema:** Odoo crea partner per qualsiasi mittente sconosciuto che arriva via fetchmail — inclusi indirizzi di sistema (`noreply@`, alias interni), bot bancari (Crédit Agricole), notifiche automatiche.  
**Casi reali già identificati:**
- `documentionline@credit-agricole.it` → ha creato ticket helpdesk inutili (id=1290, 1325)
- `noreply@astrotourism.com` → partner duplicati creati (id=1804, 1851)
- Alias interni che scrivono a se stessi

**Design proposto:**
```
Impostazioni → astro_mail_forward → Blacklist mittenti
├── Domini ignorati: creditagricole.it, postmaster, mailer-daemon, ...
├── Indirizzi ignorati: noreply@astrotourism.com, ...
└── Comportamento: TYPE_BLACKLISTED → scartata silenziosamente
    (no partner creato, no ticket, no lead)
```
Implementazione: parametro di sistema `astro_mail_forward.blacklist_domains` e
`astro_mail_forward.blacklist_emails` configurabili da Odoo senza deploy.
Classificazione in `email_classifier.py` come primo check prima di tutti gli altri tipi.

---

## 🟡 Media priorità

### 2. Svuotare / aumentare quota caselle quasi piene
**Dove:** SupportHost cPanel  
**Caselle critiche:**
| Casella | Usato | Quota | % |
|---------|-------|-------|---|
| `amministrazione@astronomitaly.com` | 879 MB | 1 GB | **87%** |
| `leonardo@astronomitaly.com` | 3.08 GB | 3.81 GB | **80%** |
| `commerciale@astronomitaly.com` | 1.48 GB | 1.95 GB | 75% |
| `info@astronomitaly.com` | 1.22 GB | 1.95 GB | 62% |

**Azione:** svuotare via webmail o aumentare quota via cPanel API `edit_pop_quota`.

### 3. Completare o disattivare `IMAP Roberto` (fetchmail id=13)
**Stato:** `draft` — non attivo ma non disabilitato  
**Azione:** se Roberto deve ricevere email in Odoo → completare configurazione con password.
Se non necessario → disabilitare (`active=False`) per pulizia.

### 4. Unificare partner duplicati `noreply@astrotourism.com`
**Stato:** partner id=1851 archiviato (✅ fatto), ma id=1804 ha ancora email
`noreply@astrotourism.com` e 9 messaggi come autore.  
**Azione:** verificare se i 9 messaggi sono coerenti, eventualmente riassegnare
the authorship a un partner più appropriato (es. company Astrotourism).

### 5. Aggiornare email Company 1 `info@astronomitaly.com` in dismissione
**Stato:** email company aggiornata a `informazioni@astronomitaly.com` (✅ fatto).  
**Azione residua:** verificare che tutti i template email e le notifiche di sistema
non referenzino ancora `info@astronomitaly.com` hardcoded.

---

## 🟢 Bassa priorità / Cleanup

### 6. Rimuovere record MX DNS `inbound.astrotourism.com`
**Stato:** webhook SendGrid Inbound Parse rimosso (✅), ma il record MX DNS
`inbound.astrotourism.com → mx.sendgrid.net` è ancora presente nel DNS SupportHost.  
**Azione:** rimuovere il record MX da cPanel DNS zone per `astrotourism.com`.
Non causa danni attivi ma è infrastruttura inutilizzata.

### 7. Abilitare Event Webhook SendGrid su endpoint Odoo
**Stato:** Event Webhook attivato su SendGrid (✅) verso
`https://erp.astronomitaly.com/odoo/sendgrid/events`.  
**Problema:** l'endpoint `/odoo/sendgrid/events` non esiste in Odoo — restituisce 404.
SendGrid invierà eventi (bounce, delivered, spam) ma Odoo non li processerà.  
**Azione:** creare controller Odoo che riceve e logga gli eventi SendGrid,
oppure disabilitare il webhook se non si vuole sviluppare l'integrazione.

### 8. Completare configurazione `IMAP Roberto` (fetchmail id=13)
Vedi punto 3 sopra.

### 9. Test suite email post-modifiche
**Script esistente:** `/opt/odoo19/custom/scripts/test_portal_access/test_portal_access.py`  
**Da creare:** script di test per il sistema email equivalente — verifica:
- Fetchmail tutti i server in stato `done`
- Nessuna email in `exception`
- Alias Odoo tutti in stato `valid`
- Forwarder SupportHost corretti
- Quota catchall < 80%

---

## 📋 Decisioni aperte

### D1 — `mail@astronomitaly.com` e `mail@astrotourism.com`
Caselle create come "default pulito" per invio email ma mai entrate in produzione
(uso reale = 0 messaggi). Fetchmail IMAP attivi ma zero email processate.  
**Opzioni:**
- A) Usarle come `default_from` + `smtp_user` (richiede aggiornamento Odoo + SMTP)
- B) Tenerle come caselle dormienti di riserva
- C) Eliminarle se non servono

### D2 — Blacklist vs lista bianca per fetchmail
La blacklist (D1 sopra) blocca mittenti noti indesiderati.
Alternativa più robusta: **lista bianca** dei soli mittenti accettati — ma troppo
rigida per un sistema B2B dove i clienti sono imprevedibili.  
**Decisione:** procedere con blacklist per domini/indirizzi noti.

---

*Documento aggiornato: 2026-04-30*  
*Riferimento SOA: `L3-infrastructure/astronomitaly/EMAIL_SYSTEM_SOA.md`*
