import click
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from ckan.plugins import toolkit
from ckan.common import config


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
@click.option('--months', type=int, default=6, help='Numero di mesi di inattività (default: 6)')
@click.option('--delete', 'do_delete', is_flag=True, help='Elimina gli utenti inattivi trovati')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente l\'eliminazione senza chiedere')
def inactive_users(months, do_delete, yes):
    """Lista e gestisce utenti inattivi.
    
    Trova tutti gli utenti che:
    - Non hanno dataset
    - Non hanno API token
    - Non si sono autenticati da più di N mesi (default: 6)
    
    Esempi:
    - Lista utenti inattivi da 6 mesi: inactive-users
    - Lista utenti inattivi da 12 mesi: inactive-users --months 12
    - Elimina utenti inattivi da 6 mesi: inactive-users --delete -y
    """
    try:
        from datetime import datetime, timedelta
        import ckan.model as model
        
        context = {'ignore_auth': True}
        
        # Calcola la data limite (N mesi fa)
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        
        click.echo(f"\n🔍 Ricerca utenti inattivi da più di {months} mesi (prima del {cutoff_date.strftime('%Y-%m-%d')})")
        click.echo("=" * 80)
        
        # Query SQL per trovare utenti inattivi
        sql_query = """
        SELECT u.id, u.name, u.fullname, u.email, u.created, u.last_active, u.state,
               COALESCE(dataset_count, 0) as dataset_count,
               COALESCE(token_count, 0) as token_count
        FROM "user" u
        LEFT JOIN (
            SELECT p.creator_user_id, COUNT(*) as dataset_count
            FROM package p
            WHERE p.state = 'active'
            GROUP BY p.creator_user_id
        ) datasets ON u.id = datasets.creator_user_id
        LEFT JOIN (
            SELECT at.user_id, COUNT(*) as token_count
            FROM api_token at
            GROUP BY at.user_id
        ) tokens ON u.id = tokens.user_id
        WHERE u.state = 'active'
          AND u.sysadmin = false
          AND (u.last_active IS NULL OR u.last_active < %s)
          AND COALESCE(dataset_count, 0) = 0
          AND COALESCE(token_count, 0) = 0
        ORDER BY u.last_active ASC NULLS FIRST, u.created ASC
        """
        
        result = model.Session.execute(sql_query, (cutoff_date,))
        inactive_users_list = []
        
        for row in result:
            user_info = {
                'id': row.id,
                'name': row.name,
                'fullname': row.fullname or row.name,
                'email': row.email,
                'created': row.created,
                'last_active': row.last_active,
                'state': row.state,
                'dataset_count': int(row.dataset_count or 0),
                'token_count': int(row.token_count or 0)
            }
            inactive_users_list.append(user_info)
        
        # Mostra risultati
        if not inactive_users_list:
            click.echo(f"\n✅ Nessun utente inattivo trovato con i criteri specificati")
            return
        
        # Header
        if do_delete:
            click.echo(f"\n❌ Utenti inattivi da eliminare ({len(inactive_users_list)} trovati):")
        else:
            click.echo(f"\n📋 Utenti inattivi trovati ({len(inactive_users_list)}):")
        
        click.echo("=" * 80)
        
        # Lista utenti
        for user in inactive_users_list:
            last_active_str = "Mai" if not user['last_active'] else user['last_active'].strftime('%Y-%m-%d')
            created_str = user['created'].strftime('%Y-%m-%d') if user['created'] else "Sconosciuto"
            
            click.echo(f"👤 {user['name']} - {user['fullname']}")
            click.echo(f"   📧 Email: {user['email'] or 'Non specificata'}")
            click.echo(f"   📅 Creato: {created_str}")
            click.echo(f"   🕒 Ultimo accesso: {last_active_str}")
            click.echo(f"   📊 Dataset: {user['dataset_count']}, Token: {user['token_count']}")
            click.echo(f"   🆔 ID: {user['id']}")
            click.echo("")
        
        # Riepilogo
        click.echo(f"📊 Trovati {len(inactive_users_list)} utenti inattivi")
        
        # Esegui eliminazione se richiesta
        if do_delete:
            if not inactive_users_list:
                return
            
            # Chiedi conferma
            if not yes and not click.confirm(f'\n⚠️  Vuoi eliminare {len(inactive_users_list)} utenti inattivi?'):
                click.echo('Operazione annullata')
                return
            
            # Elimina utenti
            success_count = 0
            
            for user in inactive_users_list:
                try:
                    # Usa l'API di CKAN per eliminare l'utente
                    toolkit.get_action('user_delete')(
                        context, {'id': user['id']})
                    success_count += 1
                    click.echo(f"✅ Eliminato: {user['name']}")
                except Exception as e:
                    click.echo(f"❌ Errore nell'eliminazione di {user['name']}: {str(e)}", err=True)
            
            click.echo(f"\n📊 Operazione completata: {success_count}/{len(inactive_users_list)} utenti eliminati")
        
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


@opendata.command()
@click.option('--to', 'recipient_email', required=True, help='Indirizzo email del destinatario')
@click.option('--subject', default='Test email da CKAN', help='Oggetto dell\'email di test')
@click.option('--smtp-server', help='Server SMTP (se non specificato usa la config CKAN)')
@click.option('--smtp-port', type=int, help='Porta SMTP (se non specificata usa la config CKAN)')
@click.option('--smtp-user', help='Username SMTP (se non specificato usa la config CKAN)')
@click.option('--smtp-password', help='Password SMTP (se non specificata usa la config CKAN)')
@click.option('--use-tls/--no-tls', default=None, help='Usa TLS (se non specificato usa la config CKAN)')
@click.option('--use-ssl/--no-ssl', default=None, help='Usa SSL (se non specificato usa la config CKAN)')
@click.option('--timeout', type=int, default=30, help='Timeout connessione in secondi (default: 30)')
@click.option('--verbose', '-v', is_flag=True, help='Mostra dettagli di debug')
def test_smtp(recipient_email, subject, smtp_server, smtp_port, smtp_user, smtp_password, 
              use_tls, use_ssl, timeout, verbose):
    """Testa l'invio di email tramite SMTP usando la configurazione CKAN o parametri custom.
    
    Esempi:
    - Test con config CKAN: test-smtp --to test@example.com
    - Test con parametri custom: test-smtp --to test@example.com --smtp-server smtp.gmail.com --smtp-port 587 --smtp-user myuser --smtp-password mypass --use-tls
    """
    try:
        # Ottieni configurazioni SMTP da CKAN se non specificate
        smtp_server = smtp_server or config.get('smtp.server')
        smtp_port = smtp_port or int(config.get('smtp.port', 25))
        smtp_user = smtp_user or config.get('smtp.user')
        smtp_password = smtp_password or config.get('smtp.password')
        smtp_from = config.get('smtp.mail_from') or config.get('ckan.site_id', 'ckan') + '@localhost'
        
        # Determina TLS/SSL dalla configurazione se non specificato
        if use_tls is None:
            starttls_config = config.get('smtp.starttls', '')
            if isinstance(starttls_config, bool):
                use_tls = starttls_config
            else:
                use_tls = str(starttls_config).lower() in ('true', '1', 'yes')
        
        if use_ssl is None:
            ssl_config = config.get('smtp.use_ssl', '')
            if isinstance(ssl_config, bool):
                use_ssl = ssl_config
            else:
                use_ssl = str(ssl_config).lower() in ('true', '1', 'yes')
        
        # Validazione parametri
        if not smtp_server:
            click.echo("❌ Errore: Server SMTP non configurato. Usa --smtp-server o configura smtp.server in CKAN", err=True)
            return
        
        click.echo(f"🔧 Configurazione SMTP:")
        click.echo(f"   Server: {smtp_server}")
        click.echo(f"   Porta: {smtp_port}")
        click.echo(f"   Utente: {smtp_user or 'Non configurato'}")
        click.echo(f"   Password: {smtp_password or 'Non configurata'}")
        click.echo(f"   TLS: {'Sì' if use_tls else 'No'}")
        click.echo(f"   SSL: {'Sì' if use_ssl else 'No'}")
        click.echo(f"   From: {smtp_from}")
        click.echo(f"   To: {recipient_email}")
        click.echo(f"   Timeout: {timeout}s")
        click.echo("")
        
        # Test connessione al server SMTP
        click.echo("🔍 Test 1: Risoluzione DNS e connettività...")
        try:
            # Risolvi il nome del server
            server_ip = socket.gethostbyname(smtp_server)
            click.echo(f"✅ DNS risolto: {smtp_server} -> {server_ip}")
            
            # Test connessione TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((smtp_server, smtp_port))
            sock.close()
            
            if result == 0:
                click.echo(f"✅ Connessione TCP riuscita su {smtp_server}:{smtp_port}")
            else:
                click.echo(f"❌ Connessione TCP fallita su {smtp_server}:{smtp_port}")
                return
                
        except socket.gaierror as e:
            click.echo(f"❌ Errore risoluzione DNS: {str(e)}")
            return
        except Exception as e:
            click.echo(f"❌ Errore connessione: {str(e)}")
            return
        
        # Test connessione SMTP
        click.echo("\n📧 Test 2: Connessione SMTP...")
        server = None
        try:
            # Crea connessione SMTP
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=timeout)
                click.echo("✅ Connessione SMTP_SSL stabilita")
            else:
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=timeout)
                click.echo("✅ Connessione SMTP stabilita")
            
            if verbose:
                server.set_debuglevel(1)
            
            # EHLO
            server.ehlo()
            click.echo("✅ Comando EHLO riuscito")
            
            # STARTTLS se richiesto e non già in SSL
            if use_tls and not use_ssl:
                server.starttls()
                server.ehlo()  # Ri-EHLO dopo STARTTLS
                click.echo("✅ STARTTLS attivato")
            
            # Autenticazione se configurata
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
                click.echo("✅ Autenticazione riuscita")
            elif smtp_user or smtp_password:
                click.echo("⚠️ Autenticazione parziale (manca user o password)")
            else:
                click.echo("ℹ️ Nessuna autenticazione configurata")
            
        except smtplib.SMTPAuthenticationError as e:
            click.echo(f"❌ Errore autenticazione SMTP: {str(e)}")
            return
        except smtplib.SMTPConnectError as e:
            click.echo(f"❌ Errore connessione SMTP: {str(e)}")
            return
        except smtplib.SMTPException as e:
            click.echo(f"❌ Errore SMTP generico: {str(e)}")
            return
        except Exception as e:
            click.echo(f"❌ Errore imprevisto: {str(e)}")
            return
        
        # Test invio email
        click.echo("\n📨 Test 3: Invio email di test...")
        try:
            # Crea messaggio
            msg = MIMEMultipart()
            msg['From'] = smtp_from
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Corpo del messaggio
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            body = f"""
Questa è un'email di test inviata da CKAN.

Dettagli del test:
- Data/Ora: {timestamp}
- Server SMTP: {smtp_server}:{smtp_port}
- TLS: {'Abilitato' if use_tls else 'Disabilitato'}
- SSL: {'Abilitato' if use_ssl else 'Disabilitato'}
- Autenticazione: {'Configurata' if smtp_user else 'Non configurata'}

Se ricevi questa email, la configurazione SMTP è corretta!

--
Inviato dal sistema CKAN OpenData
"""
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Invia email
            text = msg.as_string()
            server.sendmail(smtp_from, recipient_email, text)
            
            click.echo(f"✅ Email inviata con successo a {recipient_email}")
            click.echo(f"   Oggetto: {subject}")
            click.echo(f"   Mittente: {smtp_from}")
            
        except smtplib.SMTPRecipientsRefused as e:
            click.echo(f"❌ Destinatario rifiutato: {str(e)}")
        except smtplib.SMTPSenderRefused as e:
            click.echo(f"❌ Mittente rifiutato: {str(e)}")
        except smtplib.SMTPDataError as e:
            click.echo(f"❌ Errore dati SMTP: {str(e)}")
        except Exception as e:
            click.echo(f"❌ Errore invio email: {str(e)}")
        
        finally:
            # Chiudi connessione
            if server:
                try:
                    server.quit()
                    click.echo("\n🔌 Connessione SMTP chiusa")
                except:
                    pass
        
        click.echo("\n📋 Riepilogo test SMTP completato!")
        click.echo("Se tutti i test sono passati, la configurazione SMTP è corretta.")
        
    except Exception as e:
        click.echo(f"❌ Errore generale: {str(e)}", err=True)


@opendata.command()
def show_smtp_config():
    """Mostra la configurazione SMTP attuale di CKAN."""
    try:
        click.echo("📧 Configurazione SMTP attuale:")
        click.echo("=" * 50)
        
        # Leggi configurazioni SMTP
        smtp_server = config.get('smtp.server', 'Non configurato')
        smtp_port = config.get('smtp.port', 'Non configurato')
        smtp_user = config.get('smtp.user', 'Non configurato')
        smtp_password = config.get('smtp.password')
        smtp_from = config.get('smtp.mail_from', 'Non configurato')
        smtp_reply_to = config.get('smtp.reply_to', 'Non configurato')
        
        # Configurazioni TLS/SSL
        starttls_config = config.get('smtp.starttls', '')
        if isinstance(starttls_config, bool):
            use_tls = starttls_config
        else:
            use_tls = str(starttls_config).lower() in ('true', '1', 'yes')
        
        ssl_config = config.get('smtp.use_ssl', '')
        if isinstance(ssl_config, bool):
            use_ssl = ssl_config
        else:
            use_ssl = str(ssl_config).lower() in ('true', '1', 'yes')
        
        # Configurazioni contact plugin
        contact_mail_to = config.get('ckanext.contact.mail_to', 'Non configurato')
        contact_recipient_name = config.get('ckanext.contact.recipient_name', 'Non configurato')
        
        click.echo(f"Server SMTP: {smtp_server}")
        click.echo(f"Porta: {smtp_port}")
        click.echo(f"Utente: {smtp_user}")
        click.echo(f"Password: {'*' * len(smtp_password) if smtp_password else 'Non configurata'}")
        click.echo(f"Mail From: {smtp_from}")
        click.echo(f"Reply To: {smtp_reply_to}")
        click.echo(f"STARTTLS: {'Sì' if use_tls else 'No'}")
        click.echo(f"SSL: {'Sì' if use_ssl else 'No'}")
        click.echo("")
        click.echo("📋 Configurazione Contact Plugin:")
        click.echo(f"Destinatario: {contact_mail_to}")
        click.echo(f"Nome destinatario: {contact_recipient_name}")
        
        # Consigli
        click.echo("")
        click.echo("💡 Consigli:")
        if use_ssl and smtp_port != '465':
            click.echo("⚠️ Stai usando SSL ma non la porta 465. Considera di usare la porta 465.")
        elif use_tls and smtp_port != '587':
            click.echo("⚠️ Stai usando STARTTLS ma non la porta 587. Considera di usare la porta 587.")
        
        if use_ssl and use_tls:
            click.echo("⚠️ Hai sia SSL che STARTTLS attivi. Usa solo uno dei due.")
        
        if smtp_server == 'smtp.googlemail.com':
            if use_ssl:
                click.echo("ℹ️ Per Gmail con SSL, usa la porta 465")
            elif use_tls:
                click.echo("✅ Gmail con STARTTLS (porta 587) è la configurazione raccomandata per CKAN")
            else:
                click.echo("⚠️ Gmail richiede SSL o STARTTLS per funzionare")
        
    except Exception as e:
        click.echo(f"❌ Errore nel leggere la configurazione: {str(e)}", err=True)


@opendata.command()
@click.option('--dev', is_flag=True, help='Usa il Dockerfile.dev invece di quello di produzione')
@click.option('-y', '--yes', is_flag=True, help='Conferma automaticamente la ricostruzione')
def rebuild_docker():
    """Ricostruisce l'immagine Docker CKAN con i patch applicati."""
    try:
        import subprocess
        import os
        
        # Cambia nella directory del progetto
        project_root = '/home/dessi/Documenti/net7/ckan-docker-config'
        
        if not os.path.exists(project_root):
            click.echo(f"❌ Directory del progetto non trovata: {project_root}", err=True)
            return
        
        dockerfile = 'Dockerfile.dev' if dev else 'Dockerfile'
        container_name = 'ckan-dev' if dev else 'ckan'
        
        click.echo(f"🔧 Ricostruzione immagine Docker CKAN...")
        click.echo(f"   Dockerfile: {dockerfile}")
        click.echo(f"   Container: {container_name}")
        click.echo("")
        
        if not yes and not click.confirm('Vuoi procedere con la ricostruzione? Questo potrebbe richiedere diversi minuti.'):
            click.echo('Operazione annullata')
            return
        
        click.echo("🛑 Fermata dei container...")
        
        # Ferma i container
        try:
            subprocess.run(['docker-compose', 'down'], 
                         cwd=project_root, check=True, capture_output=True)
            click.echo("✅ Container fermati")
        except subprocess.CalledProcessError as e:
            click.echo(f"⚠️ Errore fermata container: {e}")
        
        click.echo("🔨 Ricostruzione immagine in corso...")
        
        # Ricostruisci l'immagine CKAN
        try:
            result = subprocess.run([
                'docker-compose', 'build', '--no-cache', 'ckan'
            ], cwd=project_root, check=True, capture_output=True, text=True)
            
            click.echo("✅ Immagine ricostruita con successo")
            
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Errore nella ricostruzione: {e}")
            click.echo(f"Output: {e.stdout}")
            click.echo(f"Errori: {e.stderr}")
            return
        
        click.echo("🚀 Avvio dei container...")
        
        # Riavvia i container
        try:
            subprocess.run(['docker-compose', 'up', '-d'], 
                         cwd=project_root, check=True, capture_output=True)
            click.echo("✅ Container riavviati")
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Errore riavvio container: {e}")
            return
        
        click.echo("")
        click.echo("🎉 Ricostruzione completata!")
        click.echo("Il patch del mailer SSL è ora attivo.")
        click.echo("Puoi testare l'invio email con:")
        click.echo("  ckan opendata test-smtp --to tua-email@example.com")
        
    except Exception as e:
        click.echo(f"❌ Errore generale: {str(e)}", err=True)


def get_commands():
    return [opendata]
