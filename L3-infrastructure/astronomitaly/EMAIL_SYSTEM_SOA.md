# EMAIL_SYSTEM_SOA — Astronomitaly
*State of Art — configurazione e architettura sistema email*  
*Aggiornato: 2026-04-30 | Versione: 1.0.0*

---

## 1. Entità e domini

| Entità | Dominio email | Company Odoo | Prefisso preventivi |
|--------|--------------|--------------|--------------------|
| Astronomitaly di Fabrizio Marra | `astronomitaly.com` | id=1 | AIT- |
| Astrotourism.com di Fabiana Rossetti | `astrotourism.com` | id=7 | ATM- |

Hosting email: **SupportHost** (account `astrotou`, IP `162.55.130.111`)  
Server IMAP/SMTP: `mail.astronomitaly.com` / `mail.astrotourism.com` (entrambi su SupportHost)  
Server Odoo (Hetzner): `49.13.223.181`, ERP: `erp.astronomitaly.com`

---

## 2. Architettura invio (SMTP)

### Server SMTP configurati in Odoo

| Nome | Host | Porta | User | From Filter | Uso |
|------|------|-------|------|-------------|-----|
| SMTP Astronomitaly | `mail.astronomitaly.com` | 587 STARTTLS | `noreply@astronomitaly.com` | `astronomitaly.com` | Tutte le email operative AIT |
| SMTP Astrotourism | `mail.astrotourism.com` | 587 STARTTLS | `noreply@astrotourism.com` | `astrotourism.com` | Tutte le email operative ATM |
| Sendgrid Astronomitaly | `smtp.sendgrid.net` | 587 | `apikey` | `news@astronomitaly.com` | **Solo newsletter/mass mail** |
| Sendgrid Astrotourism | `smtp.sendgrid.net` | 587 | `apikey` | `astrotourism.com` | **Solo newsletter/mass mail** |
| Preventivi | `mail.astronomitaly.com` | 587 STARTTLS | `preventivi@astronomitaly.com` | `preventivi@astronomitaly.com` | Invio preventivi dedicato |

### Decisione architetturale: SupportHost per operative, SendGrid solo per newsletter

**Motivazione:** i pool IP condivisi di SendGrid sono periodicamente in blacklist RBL
(Spamcop, Malware.Expert). Per email operative (preventivi, conferme, CRM) un blocco
temporaneo è inaccettabile. SendGrid è riservato al modulo Email Marketing (newsletter)
dove la deliverability immediata è meno critica e i volumi sono prevedibili.

### `default_from` e `noreply`

Entrambi i domini alias Odoo hanno `default_from = noreply`:
- `noreply@astronomitaly.com` → mittente di fallback per email automatiche di sistema
- `noreply@astrotourism.com` → idem per ATM

**Comportamento `noreply`:**
- Invio: abilitato (usato come `smtp_user` su SupportHost)
- Ricezione: **abilitata** (SupportHost, `suspended_incoming = 0`)
- Forwarder SupportHost: `noreply@` → `catchall@` (stesso dominio)
- Risultato: le risposte dei clienti a email automatiche entrano in Odoo via fetchmail
  catchall e vengono instradate da `astro_mail_forward` nel chatter del record originale

---

## 3. Architettura ricezione (IMAP Fetchmail)

### Server fetchmail attivi in Odoo (cron ogni 5 minuti)

| ID | Nome | Casella | Server | Stato |
|----|------|---------|--------|-------|
| 3 | Catchall | `catchall@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 14 | Catchall Astrotourism | `catchall@astrotourism.com` | `mail.astrotourism.com:993` | ✅ done |
| 4 | Amministrazione | `amministrazione@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 5 | Prenotazioni | `prenotazioni@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 6 | Voucher IMAP | `voucher@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 7 | Commerciale | `commerciale@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 8 | Comunicazione | `comunicazione@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 9 | AstroWedding | `astrowedding@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 10 | Preventivi Astronomitaly | `preventivi@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 11 | Preventivi Astrotourism | `preventivi@astrotourism.com` | `mail.astronomitaly.com:993` | ✅ done |
| 1 | IMAP Astrotourism | `mail@astrotourism.com` | `mail.astrotourism.com:993` | ✅ done |
| 2 | IMAP Astronomitaly | `mail@astronomitaly.com` | `mail.astronomitaly.com:993` | ✅ done |
| 12 | IMAP Leonardo | `leonardo@astronomitaly.com` | `mail.astronomitaly.com:993` | ⚠️ DISABILITATO |
| 13 | IMAP Roberto | `roberto@astronomitaly.com` | `mail.astronomitaly.com:993` | ⚠️ stato draft |

### Flusso ricezione risposta cliente

```
Cliente risponde a noreply@astronomitaly.com
    → SupportHost riceve (ricezione abilitata) ✅
    → Forwarder SupportHost: noreply@ → catchall@ ✅
    → Fetchmail id=3 preleva da catchall@astronomitaly.com ogni 5 min ✅
    → astro_mail_forward classifica (TYPE_REPLY / TYPE_FORWARD) ✅
    → Threading Odoo: aggancia al record giusto via Message-ID ✅
    → Appare nel chatter automaticamente ✅

Cliente risponde a noreply@astrotourism.com
    → SupportHost riceve ✅
    → Forwarder SupportHost: noreply@ → catchall@astrotourism.com ✅
    → Fetchmail id=14 preleva da catchall@astrotourism.com ogni 5 min ✅
    → astro_mail_forward → chatter ✅
```

---

## 4. Alias Odoo configurati

### Alias domain

| Dominio | catchall | bounce | default_from |
|---------|----------|--------|-------------|
| `astronomitaly.com` (id=7) | `catchall` | `bounce` | `noreply` |
| `astrotourism.com` (id=6) | `catchall` | `bounce` | `noreply` |

### Alias attivi principali

| Alias | Dominio | Modello Odoo | Team/Default | Stato |
|-------|---------|--------------|--------------|-------|
| `informazioni@` | `astronomitaly.com` | `helpdesk.ticket` | Customer Care (team 1) | valid |
| `prenotazioni@` | `astronomitaly.com` | `helpdesk.ticket` | Prenotazioni (team 11) | valid |
| `commerciale@` | `astronomitaly.com` | `helpdesk.ticket` | Commerciale (team 8) | valid |
| `comunicazione@` | `astronomitaly.com` | `helpdesk.ticket` | Comunicazione (team 10) | valid |
| `voucher@` | `astronomitaly.com` | `helpdesk.ticket` | Voucher (team 13) | valid |
| `astrowedding@` | `astronomitaly.com` | `helpdesk.ticket` | Astrowedding (team 12) | valid |
| `amministrazione@` | `astronomitaly.com` | `helpdesk.ticket` | Amministrazione (team 9) | valid |
| `prenotazioni@` — alias IT | `astronomitaly.com` | `helpdesk.ticket` | Prenotazioni (team 11) | valid |
| `preventivi@` | `astronomitaly.com` | `crm.lead` | Team vendita 4 | valid |
| `preventivi@` | `astrotourism.com` | `crm.lead` | Team vendita 1 | valid |
| `candidature@` | `astronomitaly.com` | `hr.applicant` | Job id=11 | not_tested |
| `it@` | `astronomitaly.com` | `helpdesk.ticket` | IT (team 16) | valid |

---

## 5. Forwarder SupportHost configurati

### astronomitaly.com

| Da | A | Motivo |
|----|---|--------|
| `noreply@` | `catchall@astronomitaly.com` | Risposte clienti → Odoo |
| `informazioni@` | `catchall@astronomitaly.com` | Redirect verso catchall |
| `it@` | `catchall@astronomitaly.com` | Redirect verso catchall |
| `astrobox@` | `voucher@astronomitaly.com` | Alias legacy |
| `astrotour@` | `info@astronomitaly.com` | Alias legacy |
| `news@` | `press@astronomitaly.com` | Redirect stampa |
| `roberto@` | `roberto@touralys.com` | Roberto esterno |
| `web@` | `web@astrotourism.com` | Cross-dominio |

### astrotourism.com

| Da | A | Motivo |
|----|---|--------|
| `noreply@` | `catchall@astrotourism.com` | Risposte clienti → Odoo |
| `amministrazione@` | `amministrazione@astronomitaly.com` | Cross-dominio |
| `press@` | `press@astronomitaly.com` | Cross-dominio |
| `shop@` | `ordini@astronomitaly.com` | Cross-dominio |
| `team@` | `jobs@astronomitaly.com` | Cross-dominio |

---

## 6. Caselle SupportHost — restrizioni note

| Casella | suspended_incoming | Note |
|---------|--------------------|------|
| `noreply@astronomitaly.com` | 0 (abilitata) | Forwarder → catchall@ |
| `noreply@astrotourism.com` | 0 (abilitata) | Forwarder → catchall@ |
| `bounce@astronomitaly.com` | 1 (bloccata) | Intenzionale — gestisce bounce |
| `bounce@astrotourism.com` | 1 (bloccata) | Intenzionale — login sospeso |
| `catchall@astronomitaly.com` | 0 | Quota 500 MB (era 10 MB — aumentata 2026-04-30) |
| `catchall@astrotourism.com` | 0 | Quota 500 MB |

---

## 7. Cron email Odoo

| ID | Nome | Intervallo | Note |
|----|------|------------|------|
| 6 | Mail: Fetchmail Service | **5 minuti** | Scarica da tutte le caselle IMAP |
| 7 | Mail: Post scheduled messages | **5 minuti** | Invia messaggi schedulati (delay recall) |
| 3 | Mail: Email Queue Manager | **5 minuti** | Processa coda invio outgoing |
| 143 | Astro Mail: Retry email fallite (SMTP) | **1 ora** | Retry su exception SMTP transitori |

---

## 8. Moduli custom che gestiscono email

| Modulo | Versione | Funzione |
|--------|----------|----------|
| `astro_mail_forward` | 19.0.2.2.0 | Routing intelligente email in ingresso — classifica EXTERNAL/FORWARD/REPLY, estrae cliente, crea ticket/lead |
| `astro_mail_delay` | 19.0.3.0.0 | Delay 15 min recall + retry automatico SMTP + notifica fallimento |

---

## 9. SendGrid

| Parametro | Valore |
|-----------|--------|
| Account | Astronomitaly (userid 1850273, piano paid 50.000 email/mese) |
| Reputazione | 100/100 |
| Domain Authentication | `astronomitaly.com` ✅ `astrotourism.com` ✅ `fabriziomarra.net` ✅ |
| DKIM | Valido su tutti e 3 i domini |
| Inbound Parse | **Rimosso** (2026-04-30) — non operativo, infrastruttura smontata |
| Event Webhook | **Attivato** (2026-04-30) — bounce, dropped, delivered, spam, unsubscribe |
| API key Odoo | `ODOO API` (id `-CUSdZsSQuKVq4rH7F7l-g`) |
| Uso corrente | Solo newsletter/mass mail tramite modulo Email Marketing Odoo |

---

## 10. Configurazione company Odoo

| Company | ID | Email | Alias domain |
|---------|-----|-------|-------------|
| Astronomitaly di Fabrizio Marra | 1 | `informazioni@astronomitaly.com` | `astronomitaly.com` |
| Astrotourism.com di Fabiana Rossetti | 7 | `info@astrotourism.com` | `astrotourism.com` |

---

## 11. Decisioni architetturali chiave

1. **SupportHost per operative, SendGrid solo per newsletter** — IP blacklist RBL su pool condiviso SendGrid rende inaffidabile l'uso per email operative.

2. **`noreply` con ricezione abilitata + forwarder** — invece di bloccare la ricezione (che causa perdita silenziosa di risposte clienti), `noreply` accetta email e le inoltra al catchall. `astro_mail_forward` le instraderà nel chatter giusto via threading.

3. **Catchall come unico punto di ingresso Odoo** — tutte le email non dirette a un alias specifico convergono su `catchall@`. Il fetchmail catchall è il safety net del sistema.

4. **`astro_mail_forward` come router intelligente** — gestisce tutti i casi: email diretta cliente, inoltro da interno, risposta a cliente con alias in CC. Nessun ticket creato con cliente sbagliato.

5. **SendGrid Inbound Parse smontato** — configurato nel 2025 come alternativa al fetchmail IMAP (bloccato da Hetzner), mai completato. Rimosso 2026-04-30: webhook eliminati, DNS mantenuto (inoffensivo).

---

## 12. Alert e monitoraggio

| Alert | Condizione | Azione |
|-------|-----------|--------|
| ⚠️ Quota catchall piena | `catchall@astronomitaly.com` > 400 MB (su 500) | Aumentare quota su SupportHost |
| ⚠️ Leonardo casella piena | `leonardo@astronomitaly.com` 80% (3.08/3.81 GB) | Svuotare o aumentare quota |
| ⚠️ Amministrazione casella piena | `amministrazione@astronomitaly.com` 87% (879/1000 MB) | Svuotare o aumentare quota |
| 🔴 email in exception | `mail.mail.state = exception` | `astro_mail_delay` ritenta automaticamente 3 volte poi notifica |
| 🔴 Fetchmail IMAP Roberto | id=13, stato `draft` | Completare configurazione o disabilitare |

---

*Documento di riferimento — aggiornare ad ogni modifica dell'infrastruttura email.*
