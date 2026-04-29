## ADDED Requirements

### Requirement: Formati binari non visualizzabili mostrano il pulsante Download
Le risorse con formato `gtfs` o `tar` SHALL mostrare il pulsante "Download" nella lista risorse del dataset, indipendentemente dal valore di `url_type` o dalla presenza di views.

#### Scenario: Risorsa GTFS caricata mostra Download
- **WHEN** una risorsa ha `format = 'GTFS'` e `url_type = 'upload'`
- **THEN** nella pagina dataset viene mostrato il pulsante "Download" e non il link "Vai alla risorsa"

#### Scenario: Risorsa TAR caricata mostra Download
- **WHEN** una risorsa ha `format = 'TAR'` e `url_type = 'upload'`
- **THEN** nella pagina dataset viene mostrato il pulsante "Download" e non il link "Vai alla risorsa"

#### Scenario: Formato GTFS case-insensitive
- **WHEN** una risorsa ha `format = 'gtfs'` (minuscolo)
- **THEN** viene comunque mostrato il pulsante "Download"

#### Scenario: Altri formati non sono alterati
- **WHEN** una risorsa ha un formato diverso da `gtfs` e `tar` (es. `csv`, `zip`, `pdf`)
- **THEN** il comportamento preesistente rimane invariato
