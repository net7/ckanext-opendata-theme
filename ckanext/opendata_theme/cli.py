import click
from ckan.plugins import toolkit


@click.group(short_help='OpenData Theme useful actions')
def opendata():
    """OpenData Theme CLI commands."""
    pass


@opendata.command()
@click.argument('package_id')
def list_resources(package_id):
    """Lista tutte le risorse di un dataset.
    
    Args:
        package_id: ID o nome del dataset
    """
    try:
        context = {'ignore_auth': True}
        package = toolkit.get_action('package_show')(
            context, {'id': package_id})
        
        if not package.get('resources'):
            click.echo(f"Nessuna risorsa trovata nel dataset {package_id}")
            return

        click.echo(f"\nRisorse del dataset {package_id}:")
        for res in package.get('resources', []):
            click.echo(f"- {res['id']}: {res['name']} ({res['format']})")
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('package_id')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def delete_resources(package_id, yes):
    """Elimina tutte le risorse di un dataset.
    
    Args:
        package_id: ID o nome del dataset
    """
    try:
        # Prima mostra le risorse che verranno eliminate
        context = {'ignore_auth': True}
        package = toolkit.get_action('package_show')(
            context, {'id': package_id})
        
        if not package.get('resources'):
            click.echo(f"Nessuna risorsa da eliminare nel dataset {package_id}")
            return

        click.echo(f"\nLe seguenti risorse verranno eliminate:")
        for res in package.get('resources', []):
            click.echo(f"- {res['id']}: {res['name']}")
            
        # Chiedi conferma solo se l'opzione -y non è stata specificata
        if not yes and not click.confirm('\nVuoi procedere con l\'eliminazione?'):
            click.echo('Operazione annullata')
            return

        # Elimina le risorse
        for res in package.get('resources', []):
            toolkit.get_action('resource_delete')(
                context, {'id': res['id']})
        
        click.echo(f"\nEliminate {len(package['resources'])} risorse dal dataset {package_id}")
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('resource_id')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def delete_resource(resource_id, yes):
    """Elimina una risorsa specifica in base al suo ID.
    
    Args:
        resource_id: ID della risorsa da eliminare
    """
    try:
        context = {'ignore_auth': True}
        
        # Ottieni informazioni sulla risorsa
        try:
            resource = toolkit.get_action('resource_show')(
                context, {'id': resource_id})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Risorsa con ID {resource_id} non trovata", err=True)
            return
            
        # Mostra dettagli della risorsa
        click.echo(f"\nStai per eliminare la seguente risorsa:")
        click.echo(f"- ID: {resource['id']}")
        click.echo(f"- Nome: {resource['name']}")
        click.echo(f"- Dataset: {resource['package_id']}")
        
        # Chiedi conferma solo se l'opzione -y non è stata specificata
        if not yes and not click.confirm('\nVuoi procedere con l\'eliminazione?'):
            click.echo('Operazione annullata')
            return
            
        # Elimina la risorsa
        toolkit.get_action('resource_delete')(
            context, {'id': resource_id})
        
        click.echo(f"\nRisorsa {resource_id} eliminata con successo")
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('username')
def list_api_tokens(username):
    """Lista tutti gli API token di un utente.
    
    Args:
        username: Nome utente di cui visualizzare i token
    """
    try:
        context = {'ignore_auth': True}
        
        # Verifica che l'utente esista
        try:
            user = toolkit.get_action('user_show')(
                context, {'id': username})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Utente {username} non trovato", err=True)
            return
            
        # Ottieni i token dell'utente
        tokens = toolkit.get_action('api_token_list')(
            context, {'user': username})
        
        if not tokens:
            click.echo(f"\nNessun API token trovato per l'utente {username}")
            return
            
        click.echo(f"\nAPI token dell'utente {username}:")
        for token in tokens:
            # Mostra informazioni sul token
            click.echo(f"- ID: {token['id']}")
            click.echo(f"  Nome: {token.get('name', 'Nessun nome')}")
            click.echo(f"  Data creazione: {token['created_at']}")
            click.echo(f"  Data scadenza: {token.get('expires_at', 'Nessuna scadenza')}")
            
            # Controlla diverse possibili chiavi per l'ultimo accesso
            last_access = token.get('last_access') or token.get('lastAccess') or token.get('last_used')
            if last_access and last_access != 'None' and last_access != 'null':
                click.echo(f"  Ultimo accesso: {last_access}")
            else:
                click.echo(f"  Ultimo accesso: Mai utilizzato")
            
            click.echo("")
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('token_id')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def delete_api_token(token_id, yes):
    """Elimina un API token specifico in base al suo ID.
    
    Args:
        token_id: ID del token da eliminare
    """
    try:
        context = {'ignore_auth': True}
        
        # Ottieni informazioni sul token
        # Nota: CKAN non ha un'azione per ottenere un singolo token per ID
        # quindi dobbiamo procedere direttamente con l'eliminazione
        
        # Chiedi conferma solo se l'opzione -y non è stata specificata
        if not yes and not click.confirm(f'\nVuoi eliminare il token con ID {token_id}?'):
            click.echo('Operazione annullata')
            return
            
        # Elimina il token
        toolkit.get_action('api_token_revoke')(
            context, {'jti': token_id})
        
        click.echo(f"\nAPI token {token_id} eliminato con successo")
    except toolkit.ObjectNotFound:
        click.echo(f"Errore: Token con ID {token_id} non trovato", err=True)
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('username')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def delete_unused_tokens(username, yes):
    """Elimina tutti gli API token non utilizzati di un utente.
    
    Args:
        username: Nome utente di cui eliminare i token non utilizzati
    """
    try:
        context = {'ignore_auth': True}
        
        # Verifica che l'utente esista
        try:
            user = toolkit.get_action('user_show')(
                context, {'id': username})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Utente {username} non trovato", err=True)
            return
            
        # Ottieni i token dell'utente
        tokens = toolkit.get_action('api_token_list')(
            context, {'user': username})
        
        if not tokens:
            click.echo(f"\nNessun API token trovato per l'utente {username}")
            return
        
        # Filtra i token non utilizzati
        unused_tokens = []
        for token in tokens:
            last_access = token.get('last_access') or token.get('lastAccess') or token.get('last_used')
            if not last_access or last_access == 'None' or last_access == 'null':
                unused_tokens.append(token)
        
        if not unused_tokens:
            click.echo(f"\nNessun token non utilizzato trovato per l'utente {username}")
            return
            
        # Mostra i token che verranno eliminati
        click.echo(f"\nI seguenti token non utilizzati verranno eliminati:")
        for token in unused_tokens:
            click.echo(f"- ID: {token['id']}")
            click.echo(f"  Nome: {token.get('name', 'Nessun nome')}")
            click.echo(f"  Data creazione: {token['created_at']}")
            click.echo("")
            
        # Chiedi conferma solo se l'opzione -y non è stata specificata
        if not yes and not click.confirm('\nVuoi procedere con l\'eliminazione?'):
            click.echo('Operazione annullata')
            return
            
        # Elimina i token
        deleted_count = 0
        for token in unused_tokens:
            try:
                toolkit.get_action('api_token_revoke')(
                    context, {'jti': token['id']})
                deleted_count += 1
            except Exception as e:
                click.echo(f"Errore nell'eliminazione del token {token['id']}: {str(e)}", err=True)
        
        click.echo(f"\nEliminati {deleted_count} token non utilizzati dell'utente {username}")
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('organization_id')
def check_org_datasets(organization_id):
    """Controlla tutti i dataset di un'organizzazione (inclusi quelli eliminati).
    
    Args:
        organization_id: ID o nome dell'organizzazione
    """
    try:
        context = {'ignore_auth': True}
        
        # Verifica che l'organizzazione esista
        try:
            org = toolkit.get_action('organization_show')(
                context, {'id': organization_id})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Organizzazione {organization_id} non trovata", err=True)
            return
            
        click.echo(f"\nAnalisi completa dell'organizzazione {org['display_name']} ({org['name']}):")
        click.echo(f"ID organizzazione: {org['id']}")
        
        # Cerca dataset attivi
        active_packages = toolkit.get_action('package_search')(
            context, {
                'fq': f'owner_org:{org["id"]}',
                'rows': 1000
            })
        
        click.echo(f"\n1. Dataset attivi trovati via API: {active_packages['count']}")
        for package in active_packages['results']:
            click.echo(f"   - {package['name']}: {package['title']} (stato: {package.get('state', 'active')})")
        
        # Cerca via Solr
        try:
            import ckan.lib.search as search
            
            solr_query = f'owner_org:{org["id"]}'
            search_result = search.query_for('package').run({
                'q': '*:*',
                'fq': solr_query,
                'rows': 1000,
                'fl': 'id,name,title,state'
            })
            
            click.echo(f"\n2. Dataset trovati via Solr: {len(search_result.get('results', []))}")
            for doc in search_result.get('results', []):
                click.echo(f"   - {doc.get('name', doc['id'])}: {doc.get('title', 'N/A')} (stato: {doc.get('state', 'sconosciuto')})")
                
        except Exception as e:
            click.echo(f"\n2. Errore nella ricerca Solr: {str(e)}")
        
        # Cerca nel database
        try:
            import ckan.model as model
            
            db_packages = model.Session.query(model.Package).filter(
                model.Package.owner_org == org['id']
            ).all()
            
            click.echo(f"\n3. Dataset trovati nel database: {len(db_packages)}")
            for db_pkg in db_packages:
                click.echo(f"   - {db_pkg.name}: {db_pkg.title or 'N/A'} (stato: {db_pkg.state})")
                
        except Exception as e:
            click.echo(f"\n3. Errore nell'accesso al database: {str(e)}")
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('organization_id')
def list_org_datasets(organization_id):
    """Lista tutti i dataset di un'organizzazione.
    
    Args:
        organization_id: ID o nome dell'organizzazione
    """
    try:
        context = {'ignore_auth': True}
        
        # Verifica che l'organizzazione esista
        try:
            org = toolkit.get_action('organization_show')(
                context, {'id': organization_id})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Organizzazione {organization_id} non trovata", err=True)
            return
            
        # Ottieni i dataset dell'organizzazione
        packages = toolkit.get_action('package_search')(
            context, {
                'fq': f'owner_org:{org["id"]}',
                'rows': 1000  # Limite alto per ottenere tutti i dataset
            })
        
        if not packages['results']:
            click.echo(f"\nNessun dataset trovato nell'organizzazione {organization_id}")
            return
            
        click.echo(f"\nDataset dell'organizzazione {org['display_name']} ({org['name']}):")
        click.echo(f"Totale dataset: {packages['count']}")
        click.echo("")
        
        for package in packages['results']:
            click.echo(f"- {package['id']}: {package['title']} ({package['name']})")
            click.echo(f"  Stato: {package.get('state', 'attivo')}")
            click.echo(f"  Risorse: {len(package.get('resources', []))}")
            click.echo("")
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('organization_id')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def delete_org_datasets(organization_id, yes):
    """Elimina tutti i dataset di un'organizzazione.
    
    Args:
        organization_id: ID o nome dell'organizzazione
    """
    try:
        context = {'ignore_auth': True}
        
        # Verifica che l'organizzazione esista
        try:
            org = toolkit.get_action('organization_show')(
                context, {'id': organization_id})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Organizzazione {organization_id} non trovata", err=True)
            return
            
        # Ottieni i dataset dell'organizzazione
        packages = toolkit.get_action('package_search')(
            context, {
                'fq': f'owner_org:{org["id"]}',
                'rows': 1000  # Limite alto per ottenere tutti i dataset
            })
        
        if not packages['results']:
            click.echo(f"\nNessun dataset da eliminare nell'organizzazione {organization_id}")
            return
            
        # Mostra i dataset che verranno eliminati
        click.echo(f"\nI seguenti {packages['count']} dataset verranno eliminati dall'organizzazione {org['display_name']}:")
        for package in packages['results']:
            click.echo(f"- {package['id']}: {package['title']} ({package['name']})")
            
        # Chiedi conferma solo se l'opzione -y non è stata specificata
        if not yes and not click.confirm(f'\nVuoi procedere con l\'eliminazione di tutti i {packages["count"]} dataset?'):
            click.echo('Operazione annullata')
            return
            
        # Elimina i dataset
        deleted_count = 0
        for package in packages['results']:
            try:
                toolkit.get_action('package_delete')(
                    context, {'id': package['id']})
                deleted_count += 1
                click.echo(f"Eliminato dataset: {package['name']}")
            except Exception as e:
                click.echo(f"Errore nell'eliminazione del dataset {package['id']}: {str(e)}", err=True)
        
        click.echo(f"\nEliminati {deleted_count} dataset dall'organizzazione {organization_id}")
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('organization_id')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def delete_organization(organization_id, yes):
    """Elimina un'organizzazione e tutti i suoi dataset.
    
    Args:
        organization_id: ID o nome dell'organizzazione da eliminare
    """
    try:
        context = {'ignore_auth': True}
        
        # Verifica che l'organizzazione esista
        try:
            org = toolkit.get_action('organization_show')(
                context, {'id': organization_id})
        except toolkit.ObjectNotFound:
            click.echo(f"Errore: Organizzazione {organization_id} non trovata", err=True)
            return
            
        # Ottieni i dataset dell'organizzazione (inclusi quelli in tutti gli stati)
        all_packages = []
        
        # Cerca dataset attivi
        active_packages = toolkit.get_action('package_search')(
            context, {
                'fq': f'owner_org:{org["id"]}',
                'rows': 1000
            })
        all_packages.extend(active_packages['results'])
        
        # Cerca anche dataset eliminati usando solr direttamente
        try:
            import ckan.lib.search as search
            
            # Cerca tutti i dataset dell'organizzazione, inclusi quelli eliminati
            solr_query = f'owner_org:{org["id"]}'
            search_result = search.query_for('package').run({
                'q': '*:*',
                'fq': solr_query,
                'rows': 1000,
                'fl': 'id,name,title,state'
            })
            
            # Aggiungi i dataset trovati da Solr che non sono già nella lista
            existing_ids = {pkg['id'] for pkg in all_packages}
            for doc in search_result.get('results', []):
                if doc['id'] not in existing_ids:
                    all_packages.append({
                        'id': doc['id'],
                        'name': doc.get('name', doc['id']),
                        'title': doc.get('title', doc.get('name', doc['id'])),
                        'state': doc.get('state', 'active')
                    })
        except Exception as e:
            click.echo(f"Avviso: Non è stato possibile cercare dataset eliminati via Solr: {str(e)}")
            
            # Come fallback, prova a usare direttamente il database
            try:
                import ckan.model as model
                
                # Cerca tutti i package dell'organizzazione nel database
                db_packages = model.Session.query(model.Package).filter(
                    model.Package.owner_org == org['id']
                ).all()
                
                existing_ids = {pkg['id'] for pkg in all_packages}
                for db_pkg in db_packages:
                    if db_pkg.id not in existing_ids:
                        all_packages.append({
                            'id': db_pkg.id,
                            'name': db_pkg.name,
                            'title': db_pkg.title or db_pkg.name,
                            'state': db_pkg.state
                        })
                        
                click.echo(f"Trovati {len(db_packages)} dataset totali nel database")
            except Exception as e2:
                click.echo(f"Avviso: Non è stato possibile accedere al database: {str(e2)}")
        
        # Mostra informazioni sull'organizzazione
        click.echo(f"\nStai per eliminare l'organizzazione:")
        click.echo(f"- ID: {org['id']}")
        click.echo(f"- Nome: {org['name']}")
        click.echo(f"- Titolo: {org['display_name']}")
        click.echo(f"- Dataset associati: {len(all_packages)}")
        
        if all_packages:
            click.echo(f"\nI seguenti dataset verranno eliminati insieme all'organizzazione:")
            for package in all_packages:
                state_info = f" (stato: {package.get('state', 'sconosciuto')})" if package.get('state') != 'active' else ""
                click.echo(f"- {package['name']}: {package.get('title', 'Titolo non disponibile')}{state_info}")
        
        # Chiedi conferma solo se l'opzione -y non è stata specificata
        if not yes and not click.confirm(f'\nVuoi procedere con l\'eliminazione dell\'organizzazione e di tutti i suoi {len(all_packages)} dataset?'):
            click.echo('Operazione annullata')
            return
            
        # Prima elimina tutti i dataset
        deleted_datasets = 0
        if all_packages:
            click.echo(f"\nEliminazione dei dataset in corso...")
            for package in all_packages:
                try:
                    # Prima prova a eliminare normalmente
                    toolkit.get_action('package_delete')(
                        context, {'id': package['id']})
                    deleted_datasets += 1
                    click.echo(f"Eliminato dataset: {package['name']}")
                except Exception as e:
                    # Se fallisce, prova a purgare definitivamente
                    try:
                        toolkit.get_action('dataset_purge')(
                            context, {'id': package['id']})
                        deleted_datasets += 1
                        click.echo(f"Purgato dataset: {package['name']}")
                    except Exception as e2:
                        click.echo(f"Errore nell'eliminazione del dataset {package['id']}: {str(e2)}", err=True)
        
        # Poi elimina l'organizzazione
        try:
            toolkit.get_action('organization_delete')(
                context, {'id': org['id']})
            click.echo(f"\nOrganizzazione {org['name']} eliminata con successo")
            click.echo(f"Eliminati anche {deleted_datasets} dataset associati")
        except Exception as e:
            click.echo(f"Errore nell'eliminazione dell'organizzazione: {str(e)}", err=True)
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


def get_commands():
    return [opendata]
