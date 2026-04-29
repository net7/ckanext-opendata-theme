## Why

Le risorse in formato GTFS caricate su CKAN mostrano il link "Vai alla risorsa" invece del pulsante "Download", impedendo agli utenti di scaricare direttamente il file. Il problema è causato dalla condizione nel template `resource_item.html` che tratta tutti i file uploaded (`url_type == 'upload'`) come navigabili, senza eccezioni per i formati binari non visualizzabili come GTFS.

## What Changes

- Aggiunta di `gtfs` e `tar` alla lista dei formati che devono mostrare il pulsante **Download** anche quando `url_type == 'upload'`
- Modifica della condizione nel template `package/snippets/resource_item.html` per escludere esplicitamente i formati binari non visualizzabili dal ramo "Vai alla risorsa"

## Capabilities

### New Capabilities

- `gtfs-download-button`: Le risorse con formato `gtfs` o `tar` mostrano il pulsante Download al posto del link Vai alla risorsa, indipendentemente dal valore di `url_type`

### Modified Capabilities

<!-- Nessuna capability esistente con requisiti che cambiano -->

## Impact

- **Template modificato**: `ckanext/opendata_theme/templates/package/snippets/resource_item.html` (riga 43)
- **Nessuna dipendenza esterna**: la modifica è limitata al template Jinja2
- **Backward compatible**: il comportamento di tutti gli altri formati rimane invariato
