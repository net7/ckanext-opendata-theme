## 1. Modifica template

- [x] 1.1 In `ckanext/opendata_theme/templates/package/snippets/resource_item.html`, aggiungere la variabile `download_formats` con i valori `['gtfs', 'tar']`
- [x] 1.2 Aggiornare la condizione alla riga 43 aggiungendo `and res.format.lower() not in download_formats` per escludere i formati binari dal ramo "Vai alla risorsa"

## 2. Verifica manuale

- [x] 2.1 Verificare che una risorsa GTFS mostri il pulsante "Download" nella pagina dataset
- [x] 2.2 Verificare che una risorsa TAR mostri il pulsante "Download" nella pagina dataset
- [x] 2.3 Verificare che altri formati (CSV, ZIP, PDF, link) mantengano il comportamento precedente
