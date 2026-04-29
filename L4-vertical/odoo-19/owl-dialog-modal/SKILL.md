---
name: odoo-19-owl-dialog
description: Pattern OWL dialog modale in Odoo 19. Caricare quando si deve implementare
  un dialog modale bloccante o non bloccante, usare useService dialog, patchare
  FormController, gestire Many2one update via OWL. Verificato e funzionante su
  astro_company_selector v19.0.1.1.0.
source: custom — verificato Astronomitaly 2026-03-19
created: 2026-04-29
layer: L4
---

# OWL Dialog Modale — Odoo 19

## Struttura file necessari

```
modulo/static/src/
    my_dialog.xml        ← template OWL + CSS
    my_dialog.js         ← componente dialog
    my_form_patch.js     ← patch FormController
```

```python
# __manifest__.py
'assets': {
    'web.assets_backend': [
        'modulo/static/src/my_dialog.xml',
        'modulo/static/src/my_dialog.js',
        'modulo/static/src/my_form_patch.js',
    ],
},
```

## Componente dialog

```javascript
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class MyDialog extends Component {
    static template = "modulo.MyDialog";
    static components = { Dialog };
    static props = {
        close: Function,      // iniettato automaticamente
        onConfirm: Function,  // callback custom
    };
    confirm(value) {
        this.props.onConfirm(value);
        this.props.close();  // chiamare SEMPRE dopo callback
    }
}
```

## Template dialog

```xml
<t t-name="modulo.MyDialog">
    <Dialog title="'Titolo'" size="'md'" technical="false">
        <t t-set-slot="default">
            <button t-on-click="() => this.confirm('valore')">Scegli</button>
        </t>
        <!-- Footer vuoto = utente NON può chiudere con Annulla -->
        <t t-set-slot="footer"><span/></t>
    </Dialog>
</t>
```

**Parametri Dialog:** `size` = sm/md/lg/xl | `technical="false"` rimuove stile grigio

## Patch FormController

```javascript
/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";
import { onMounted } from "@odoo/owl";
import { MyDialog } from "./my_dialog";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        if (this.props.resModel !== "sale.order") return;  // filtra modello
        this.dialogService = useService("dialog");
        onMounted(async () => {  // ⚠️ onMounted NON onWillStart
            if (this.model.root.resId) return;  // solo record nuovi
            await new Promise((resolve) => {     // blocca form
                this.dialogService.add(MyDialog, {
                    onConfirm: async (value) => {
                        await this.model.root.update({ my_field: value });
                        resolve();  // sblocca
                    },
                });
            });
        });
    },
});
```

## ⚠️ CRITICO — Many2one richiede oggetto {id, display_name}

```javascript
// ✅ CORRETTO
await this.model.root.update({
    company_id: { id: 7, display_name: "Astrotourism.com di Fabiana Rossetti" },
});

// ❌ SBAGLIATO — intero puro
await this.model.root.update({ company_id: 7 });

// ❌ SBAGLIATO — formato RPC [id, name]
await this.model.root.update({ company_id: [7, "Nome"] });
```

## Anti-pattern

- NON usare `onWillStart` — dialog service non disponibile
- NON omettere `static props` — warning OWL in Odoo 19
- NON dimenticare `this.props.close()` dopo il callback

## Debug console browser

```javascript
function findFC(owlNode, depth = 0) {
    if (!owlNode || depth > 25) return null;
    const comp = owlNode.component;
    if (comp?.model?.root && comp?.props?.resModel === 'MODELLO') return comp;
    for (const child of Object.values(owlNode.children || {})) {
        const r = findFC(child, depth + 1);
        if (r) return r;
    }
    return null;
}
const fc = findFC(odoo.__WOWL_DEBUG__.root.__owl__);
console.log(fc.model.root.data.company_id);  // ispeziona Many2one
```

---
*Source: custom — verificato Astronomitaly 2026-03-19 su astro_company_selector*
