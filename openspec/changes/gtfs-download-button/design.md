## Context

Il template `package/snippets/resource_item.html` gestisce la visualizzazione di ciascuna risorsa nella pagina dataset. Alla riga 43 una condizione decide se mostrare il link "Vai alla risorsa" o il pulsante "Download":

```jinja2
{% if res.has_views or res.url_type == 'upload' or res.format.lower() == 'link' %}
  <!-- Vai alla risorsa -->
{% else %}
  <!-- Download -->
{% endif %}
```

Il problema: `url_type == 'upload'` cattura tutti i file caricati su CKAN, compresi GTFS e TAR che sono formati binari non visualizzabili e per cui l'utente si aspetta un download diretto.

## Goals / Non-Goals

**Goals:**
- I formati `gtfs` e `tar` mostrano il pulsante Download anche quando `url_type == 'upload'`
- La logica è estendibile a nuovi formati senza modifiche strutturali

**Non-Goals:**
- Non si modifica il comportamento di CSV, ZIP o altri formati già corretti
- Non si interviene sulla logica di preview/views

## Decisions

### Decisione: lista di formati da forzare a Download nel template

Introdurre una variabile `download_formats` nel template con la lista dei formati che devono sempre mostrare il pulsante Download, e sottrarre questi formati dalla condizione esistente.

```jinja2
{% set download_formats = ['gtfs', 'tar'] %}
{% if (res.has_views or res.url_type == 'upload' or res.format.lower() == 'link') and res.format.lower() not in download_formats %}
  <!-- Vai alla risorsa -->
{% else %}
  <!-- Download -->
{% endif %}
```

**Alternativa scartata**: configurare la lista in Python (helper o config CKAN) — eccessivo per una modifica minima che non richiede logica server-side né test unitari separati.

## Risks / Trade-offs

- [Risorse GTFS con views abilitate] → Rimarrebbero nel ramo Download; le views non verranno mai mostrate. Mitigazione: GTFS non supporta preview in CKAN di default, quindi il rischio è trascurabile.
- [Formati case-sensitive] → `res.format.lower()` già normalizza, nessun rischio.
