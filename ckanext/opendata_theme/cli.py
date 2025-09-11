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
        
        # Se non abbiamo trovato dataset ma CKAN dice che ci sono, forza la pulizia del database
        if len(all_packages) == 0:
            click.echo(f"\nNessun dataset trovato ma CKAN potrebbe avere riferimenti fantasma.")
            click.echo(f"Tentativo di pulizia forzata dal database...")
            
            try:
                import ckan.model as model
                
                # Elimina tutti i package dell'organizzazione direttamente dal database
                db_packages = model.Session.query(model.Package).filter(
                    model.Package.owner_org == org['id']
                ).all()
                
                click.echo(f"Trovati {len(db_packages)} dataset nel database da eliminare...")
                
                for db_pkg in db_packages:
                    try:
                        # Prima prova l'API
                        toolkit.get_action('dataset_purge')(
                            context, {'id': db_pkg.id})
                        click.echo(f"Purgato via API: {db_pkg.name}")
                    except Exception:
                        try:
                            # Se l'API fallisce, elimina direttamente dal database
                            model.Session.delete(db_pkg)
                            model.Session.commit()
                            click.echo(f"Eliminato dal database: {db_pkg.name}")
                        except Exception as e3:
                            click.echo(f"Errore nell'eliminazione di {db_pkg.name}: {str(e3)}", err=True)
                            
            except Exception as e:
                click.echo(f"Errore nella pulizia forzata: {str(e)}", err=True)
        
        # Poi elimina l'organizzazione
        try:
            toolkit.get_action('organization_delete')(
                context, {'id': org['id']})
            click.echo(f"\nOrganizzazione {org['name']} eliminata con successo")
            click.echo(f"Eliminati anche {deleted_datasets} dataset associati")
        except Exception as e:
            click.echo(f"Errore nell'eliminazione dell'organizzazione: {str(e)}", err=True)
            
            # Se fallisce ancora, prova a eliminare l'organizzazione direttamente dal database
            click.echo(f"\nTentativo di eliminazione forzata dell'organizzazione dal database...")
            try:
                import ckan.model as model
                
                # Trova l'organizzazione nel database
                db_org = model.Session.query(model.Group).filter(
                    model.Group.id == org['id']
                ).first()
                
                if db_org:
                    # Elimina prima tutte le associazioni
                    model.Session.query(model.Member).filter(
                        model.Member.group_id == org['id']
                    ).delete()
                    
                    # Poi elimina l'organizzazione
                    model.Session.delete(db_org)
                    model.Session.commit()
                    click.echo(f"Organizzazione {org['name']} eliminata forzatamente dal database")
                else:
                    click.echo(f"Organizzazione non trovata nel database")
                    
            except Exception as e2:
                click.echo(f"Errore nell'eliminazione forzata: {str(e2)}", err=True)
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.argument('organization_id')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'operazione senza chiedere')
def force_clean_org(organization_id, yes):
    """Pulisce forzatamente un'organizzazione eliminando tutti i dataset fantasma dal database.
    
    Args:
        organization_id: ID o nome dell'organizzazione da pulire
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
            
        click.echo(f"\nPulizia forzata dell'organizzazione {org['display_name']} ({org['name']})")
        click.echo(f"ID organizzazione: {org['id']}")
        
        try:
            import ckan.model as model
            
            # Trova tutti i package dell'organizzazione nel database
            db_packages = model.Session.query(model.Package).filter(
                model.Package.owner_org == org['id']
            ).all()
            
            click.echo(f"\nTrovati {len(db_packages)} dataset nel database:")
            for db_pkg in db_packages:
                click.echo(f"- {db_pkg.name}: {db_pkg.title or 'N/A'} (stato: {db_pkg.state})")
            
            if not db_packages:
                click.echo("Nessun dataset fantasma trovato nel database")
                return
                
            # Chiedi conferma solo se l'opzione -y non è stata specificata
            if not yes and not click.confirm(f'\nVuoi procedere con l\'eliminazione forzata di tutti i {len(db_packages)} dataset dal database?'):
                click.echo('Operazione annullata')
                return
                
            # Elimina i dataset
            deleted_count = 0
            for db_pkg in db_packages:
                try:
                    # Prima prova l'API
                    toolkit.get_action('dataset_purge')(
                        context, {'id': db_pkg.id})
                    deleted_count += 1
                    click.echo(f"Purgato via API: {db_pkg.name}")
                except Exception:
                    try:
                        # Se l'API fallisce, elimina direttamente dal database
                        
                        # Prima elimina le risorse associate
                        model.Session.query(model.Resource).filter(
                            model.Resource.package_id == db_pkg.id
                        ).delete()
                        
                        # Elimina le associazioni nei gruppi
                        model.Session.query(model.Member).filter(
                            model.Member.table_id == db_pkg.id
                        ).delete()
                        
                        # Elimina i tag associati
                        model.Session.query(model.PackageTag).filter(
                            model.PackageTag.package_id == db_pkg.id
                        ).delete()
                        
                        # Elimina gli extra
                        model.Session.query(model.PackageExtra).filter(
                            model.PackageExtra.package_id == db_pkg.id
                        ).delete()
                        
                        # Infine elimina il package
                        model.Session.delete(db_pkg)
                        model.Session.commit()
                        
                        deleted_count += 1
                        click.echo(f"Eliminato forzatamente dal database: {db_pkg.name}")
                    except Exception as e:
                        click.echo(f"Errore nell'eliminazione di {db_pkg.name}: {str(e)}", err=True)
                        model.Session.rollback()
            
            click.echo(f"\nEliminati {deleted_count} dataset fantasma dall'organizzazione")
            click.echo(f"Ora dovresti poter eliminare l'organizzazione normalmente")
            
        except Exception as e:
            click.echo(f"Errore nell'accesso al database: {str(e)}", err=True)
            
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


@opendata.command()
@click.option('--from', 'from_count', type=int, help='Numero minimo di dataset (>=)')
@click.option('--to', 'to_count', type=int, help='Numero massimo di dataset (<=)')
@click.option('--org', 'organization_id', help='Filtra per una specifica organizzazione (ID o nome)')
@click.option('--deactivate', 'do_delete', is_flag=True, help='Elimina (soft delete) le organizzazioni filtrate')
@click.option('--activate', 'do_activate', is_flag=True, help='Riattiva le organizzazioni filtrate')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'operazione senza chiedere')
def list_organizations(from_count, to_count, organization_id, do_delete, do_activate, yes):
    """Lista e gestisce organizzazioni in base al numero di dataset.
    
    Esempi:
    - Mostra tutte: list-organizations
    - Con meno di 3 dataset: list-organizations --to 2
    - Con 5+ dataset: list-organizations --from 5
    - Tra 1 e 10 dataset: list-organizations --from 1 --to 10
    - Una specifica organizzazione: list-organizations --org my-org
    - Elimina quelle con <3 dataset: list-organizations --to 2 --deactivate -y
    """
    try:
        context = {'ignore_auth': True}
        
        # Validazione opzioni
        if do_delete and do_activate:
            click.echo("Errore: Non puoi usare --deactivate e --activate insieme", err=True)
            return
        
        # Ottieni organizzazioni
        if organization_id:
            # Filtra per organizzazione specifica
            try:
                org = toolkit.get_action('organization_show')(
                    context, {'id': organization_id})
                orgs = [org]
            except toolkit.ObjectNotFound:
                click.echo(f"Errore: Organizzazione {organization_id} non trovata", err=True)
                return
        else:
            # Ottieni tutte le organizzazioni
            orgs = toolkit.get_action('organization_list')(
                context, {'all_fields': True, 'include_extras': True})
        
        # Query SQL diretta per contare i dataset per organizzazione
        try:
            import ckan.model as model
            
            # Costruisci la query con filtri WHERE e HAVING
            where_conditions = ["g.type = 'organization'"]
            having_conditions = []
            
            if organization_id:
                # Se è specificata un'organizzazione, filtra per ID o nome
                where_conditions.append(f"(g.id = '{organization_id}' OR g.name = '{organization_id}')")
            
            if from_count is not None:
                having_conditions.append(f"COUNT(p.id) >= {from_count}")
            
            if to_count is not None:
                having_conditions.append(f"COUNT(p.id) <= {to_count}")
            
            if do_delete:
                where_conditions.append("g.state != 'deleted'")
            elif do_activate:
                where_conditions.append("g.state = 'deleted'")
            
            where_clause = " AND ".join(where_conditions)
            having_clause = " AND ".join(having_conditions) if having_conditions else ""
            
            # Query SQL su singola riga come richiesto
            if having_clause:
                sql_query = f"SELECT g.id, g.name, g.title, g.state, COALESCE(COUNT(p.id), 0) as dataset_count FROM \"group\" g LEFT JOIN package p ON p.owner_org = g.id AND p.state = 'active' WHERE {where_clause} GROUP BY g.id, g.name, g.title, g.state HAVING {having_clause} ORDER BY dataset_count"
            else:
                sql_query = f"SELECT g.id, g.name, g.title, g.state, COALESCE(COUNT(p.id), 0) as dataset_count FROM \"group\" g LEFT JOIN package p ON p.owner_org = g.id AND p.state = 'active' WHERE {where_clause} GROUP BY g.id, g.name, g.title, g.state ORDER BY dataset_count"
            
            result = model.Session.execute(sql_query)
            
            filtered_orgs = []
            for row in result:
                org_info = {
                    'id': row.id,
                    'name': row.name,
                    'title': row.title or row.name,
                    'state': row.state or 'active',
                    'dataset_count': int(row.dataset_count)
                }
                filtered_orgs.append(org_info)
                
        except Exception as e:
            click.echo(f"Errore nella query SQL, uso metodo lento: {str(e)}")
            
            # Fallback al metodo lento originale
            filtered_orgs = []
            
            for org in orgs:
                # Conta i dataset dell'organizzazione
                try:
                    packages = toolkit.get_action('package_search')(
                        context, {
                            'fq': f'owner_org:{org["id"]}',
                            'rows': 1000
                        })
                    dataset_count = packages['count']
                except Exception:
                    dataset_count = 0
                
                org_info = {
                    'id': org['id'],
                    'name': org['name'],
                    'title': org.get('display_name', org.get('title', org['name'])),
                    'state': org.get('state', 'active'),
                    'dataset_count': dataset_count
                }
                
                # Applica filtri per count
                if from_count is not None and dataset_count < from_count:
                    continue
                if to_count is not None and dataset_count > to_count:
                    continue
                
                # Applica filtri per azioni
                if do_delete and org.get('state', 'active') == 'deleted':
                    continue  # Skip già eliminate
                if do_activate and org.get('state', 'active') != 'deleted':
                    continue  # Skip già attive
                
                filtered_orgs.append(org_info)
        
        # Mostra risultati
        if not filtered_orgs:
            click.echo("\nNessuna organizzazione trovata con i filtri specificati")
            return
        
        # Header con informazioni sui filtri
        filter_info = []
        if from_count is not None:
            filter_info.append(f"dataset >= {from_count}")
        if to_count is not None:
            filter_info.append(f"dataset <= {to_count}")
        if organization_id:
            filter_info.append(f"org = {organization_id}")
        
        filter_str = " AND ".join(filter_info) if filter_info else "nessun filtro"
        
        if do_delete or do_activate:
            action_str = "da eliminare" if do_delete else "da riattivare"
            click.echo(f"\nOrganizzazioni {action_str} ({filter_str}):")
        else:
            click.echo(f"\nOrganizzazioni trovate ({filter_str}):")
        
        click.echo("=" * 60)
        
        # Lista organizzazioni
        for org in sorted(filtered_orgs, key=lambda x: x['dataset_count']):
            if org['state'] == 'deleted':
                state_icon = "❌"
            elif org['dataset_count'] == 0:
                state_icon = "⚪"
            elif org['dataset_count'] < 3:
                state_icon = "⚠️"
            else:
                state_icon = "✅"
            
            click.echo(f"{state_icon} {org['name']} - {org['title']}")
            click.echo(f"   Dataset: {org['dataset_count']}, Stato: {org['state']}, ID: {org['id']}")
        
        # Riepilogo
        click.echo(f"\n📊 Trovate {len(filtered_orgs)} organizzazioni")
        
        # Esegui azioni se richieste
        if do_delete or do_activate:
            if not filtered_orgs:
                return
            
            action_verb = "eliminare (soft delete)" if do_delete else "riattivare"
            
            # Chiedi conferma
            if not yes and not click.confirm(f'\nVuoi {action_verb} {len(filtered_orgs)} organizzazioni?'):
                click.echo('Operazione annullata')
                return
            
            # Esegui operazione
            success_count = 0
            new_state = 'deleted' if do_delete else 'active'
            
            try:
                import ckan.model as model
                
                org_ids = [org['id'] for org in filtered_orgs]
                org_ids_str = "', '".join(org_ids)
                
                # Query SQL su singola riga come richiesto
                if do_delete:
                    sql_query = f"UPDATE \"group\" SET state = 'deleted' WHERE type = 'organization' AND state != 'deleted' AND id IN ('{org_ids_str}')"
                else:
                    sql_query = f"UPDATE \"group\" SET state = 'active' WHERE type = 'organization' AND state = 'deleted' AND id IN ('{org_ids_str}')"
                
                result = model.Session.execute(sql_query)
                model.Session.commit()
                
                success_count = result.rowcount
                action_past = "eliminate" if do_delete else "riattivate"
                click.echo(f"\n✅ {action_past.capitalize()} {success_count} organizzazioni tramite query SQL")
                
            except Exception as e:
                click.echo(f"Errore nella query SQL, provo con API: {str(e)}")
                
                # Fallback con API
                for org in filtered_orgs:
                    try:
                        toolkit.get_action('organization_patch')(
                            context, {'id': org['id'], 'state': new_state})
                        success_count += 1
                        action_past = "eliminata" if do_delete else "riattivata"
                        click.echo(f"{action_past.capitalize()}: {org['name']}")
                    except Exception as api_e:
                        click.echo(f"Errore nell'operazione su {org['name']}: {str(api_e)}", err=True)
            
            click.echo(f"\n📊 Operazione completata: {success_count}/{len(filtered_orgs)} organizzazioni modificate")
        
    except Exception as e:
        click.echo(f"Errore: {str(e)}", err=True)


def get_commands():
    return [opendata]
