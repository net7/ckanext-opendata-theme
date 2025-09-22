from pyproj import Transformer
from flask import request
import ckan.plugins.toolkit as toolkit
from html.parser import HTMLParser
import random
from datetime import datetime
import json


def opendata_theme_hello():
    return "Hello, opendata_theme!"


def get_helpers():
    return {
        "opendata_theme_hello": opendata_theme_hello,
        "convert_coordinates": convert_coordinates,
        "is_current": is_current,
        "get_formatted_dataset_count": get_formatted_dataset_count,
        "get_formatted_view_count": get_formatted_view_count,
        "get_most_viewed_datasets": get_most_viewed_datasets,
        "get_all_organizations": get_all_organizations,
        "get_all_organizations_random": get_all_organizations_random,
        "get_home_organizations": get_home_organizations,
        "count_organizations": count_organizations,
        "get_recent_news": get_recent_news,
        "get_page_image": get_page_image,
        "format_date": format_date,
        "get_first_theme": get_first_theme,
        "get_theme_icon": get_theme_icon,
        "extract_themes": extract_themes,
        "get_theme_name": get_theme_name,
    }


def convert_coordinates(x: float, y: float, source_crs: str = 'EPSG:3003') -> tuple:
    """
    Converte le coordinate da un sistema di riferimento specificato a WGS84 (EPSG:4326)
    
    Args:
        x (float): Coordinata X nel sistema di origine
        y (float): Coordinata Y nel sistema di origine
        source_crs (str): Codice EPSG del sistema di riferimento di origine
        
    Returns:
        tuple: (longitudine, latitudine) in WGS84
    """
    try:
        transformer = Transformer.from_crs(source_crs, 'EPSG:3003')
        lon, lat = transformer.transform(x, y)
        return lon, lat
    except Exception as e:
        raise ValueError(f"Errore nella conversione delle coordinate: {str(e)}")


def is_current(blueprint_name, attribute_value):
    """
    Verifica se il blueprint corrente corrisponde a quello specificato e restituisce
    l'attributo richiesto se la condizione è vera.
    
    Args:
        blueprint_name (str): Il nome del blueprint da confrontare
        attribute_value (str): Il valore dell'attributo da restituire (es. 'is-current')
    
    Returns:
        str: L'attributo specificato se il blueprint corrente corrisponde, altrimenti stringa vuota
    """
    if request.blueprint == blueprint_name:
        return attribute_value
    return ''


def get_formatted_dataset_count():
    """
    Restituisce il numero di dataset formattato come "+X mila" se maggiore di 1000,
    altrimenti restituisce il numero esatto con separatore delle migliaia.
    """
    stats = toolkit.get_action('package_search')({}, {'rows': 0})
    dataset_count = stats.get('count', 0)
    
    if dataset_count >= 1000:
        rounded_count = (dataset_count // 1000) * 1000
        return f"+{rounded_count // 1000} mila"
    else:
        # Formattazione con separatore delle migliaia in stile italiano
        return f"{dataset_count:,}".replace(',', '.')


def get_formatted_view_count():
    """
    Restituisce il numero di visualizzazioni delle risorse nell'ultimo anno formattato in stile italiano.
    Utilizza cache Redis per migliorare le performance.
    
    Vanno prima puliti i dati
    
    DELETE FROM tracking_summary WHERE tracking_type NOT IN ('page', 'resource');
    """
    try:
        # Prova a utilizzare la cache Redis
        cache_key = "opendata_theme:resource_views_last_year"
        cached_result = _get_from_redis_cache(cache_key)
        
        if cached_result:
            return cached_result
        
        # Cache miss o non disponibile, calcola il valore
        from sqlalchemy import text
        from ckan.model import Session
        
        # Conta le visualizzazioni delle risorse nell'ultimo anno (365 giorni)
        sql = '''
            SELECT SUM(count) as total_count
            FROM tracking_summary
            WHERE package_id IS NOT NULL
            AND package_id != '~~not~found~~'
            AND tracking_date >= CURRENT_DATE - INTERVAL '1 year'
        '''
        
        # Esegui la query direttamente
        result = Session.execute(text(sql))
        row = result.fetchone()
        
        if row and row.total_count:
            view_count = row.total_count
        else:
            view_count = 0
        
        # Formattazione per numeri in milioni
        if view_count >= 1000000:
            millions = round(view_count / 1000000)
            if millions == 1:
                formatted_result = f"+{millions} milione"
            else:
                formatted_result = f"+{millions} milioni"
        # Formattazione per numeri in migliaia
        elif view_count >= 1000:
            thousands = round(view_count / 1000)
            formatted_result = f"+{thousands} mila"
        else:
            formatted_result = f"{view_count:,}".replace(',', '.')
        
        # Salva il risultato in cache per 1 ora (3600 secondi)
        _set_redis_cache(cache_key, formatted_result, 3600)
        
        return formatted_result
        
    except Exception as e:
        # In caso di errore, ritorna il valore statico originale
        return f"+0"


def get_most_viewed_datasets(limit=4):
    """
    Recupera i dataset più consultati in base alle statistiche di visualizzazione.
    
    Args:
        limit (int): Numero massimo di dataset da restituire (default: 4)
        
    Returns:
        list: Lista di dizionari contenenti i dataset più consultati
    """
    try:
        # Ottieni i dataset più visualizzati dal database
        from sqlalchemy import text
        from ckan.model import Session, Package
        
        sql = '''
            SELECT package_id, SUM(count) as total_views
            FROM tracking_summary
            WHERE package_id IS NOT NULL
            AND package_id != '~~not~found~~'
            GROUP BY package_id
            ORDER BY total_views DESC
            LIMIT :limit
        '''
        
        result = Session.execute(text(sql), {'limit': limit})
        package_ids = [row.package_id for row in result]
        
        # Recupera i dettagli completi dei dataset
        datasets = []
        for package_id in package_ids:
            
            try:
                dataset = toolkit.get_action('package_show')({}, {'id': package_id, 'include_tracking': True})
                datasets.append(dataset)
            except toolkit.ObjectNotFound:
                # Ignora i dataset che non esistono più
                continue
                
        return datasets
    except Exception as e:
        # In caso di errore, ritorna una lista vuota
        return []


def get_all_organizations(limit=None):
    """
    Restituisce tutte le organizzazioni disponibili nel sistema
    """
    try:
        context = {'ignore_auth': True}
        data_dict = {'all_fields': True, 'include_users': False, 'include_extras': True}
        organizations = toolkit.get_action('organization_list')(context, data_dict)
        if limit:
            return organizations[:limit]
        return organizations
    except Exception as e:
        raise ValueError(f"Errore nel recupero delle organizzazioni: {str(e)}")


def get_all_organizations_random(limit=10):
    """
    Restituisce un numero limitato di organizzazioni in ordine casuale
    
    Args:
        limit (int): Numero massimo di organizzazioni da restituire (default: 10)
        
    Returns:
        list: Lista di organizzazioni selezionate casualmente
    """
    try:
        context = {'ignore_auth': True}
        data_dict = {'all_fields': True, 'include_users': False, 'include_extras': True}
        organizations = toolkit.get_action('organization_list')(context, data_dict)
        
        # Se abbiamo meno organizzazioni del limite richiesto, restituisci tutte
        if len(organizations) <= limit:
            random.shuffle(organizations)
            return organizations
        
        # Altrimenti, seleziona casualmente il numero richiesto
        return random.sample(organizations, limit)
    except Exception as e:
        raise ValueError(f"Errore nel recupero delle organizzazioni: {str(e)}")


def get_home_organizations():
    """
    Restituisce le organizzazioni per la homepage:
    
     - Consorzio LaMMA Toscana
     - Comune di Firenze
     - Comune di Arezzo
     - Comune di Siena
     - Città Metropolitana di Firenze
     - Comune di Livorno
     - Comune di Montevarchi
     - Comune di Poggibonsi
     - Comune di Piombino
     - Comune di Vernio
     - Comune di Vaiano
     - Comune di Cantagallo
     - Comune di Montemurlo
    """
    try:
        organizations_names = [
            'lamma-toscana',
            'comune-di-firenze',
            'comune-di-arezzo',
            'comune-di-siena',
            'citta-metropolitana-firenze',
            'comune-livorno',
            'comune-di-montevarchi',
            'comune-di-poggibonsi',
            'comune-di-piombino',
            'comune-di-vernio',
            'comune-di-vaiano',
            'comune-di-cantagallo',
            'comune-di-montemurlo',
        ]
        organizations = []
        context = {'ignore_auth': True}
        
        for org_name in organizations_names:
            try:
                org = toolkit.get_action('organization_show')(
                    context, {'id': org_name, 'include_datasets': True})
                organizations.append(org)
            except toolkit.ObjectNotFound:
                # Organizzazione non trovata, salta silenziosamente
                continue
            except toolkit.NotAuthorized:
                # Utente non autorizzato, salta silenziosamente
                continue
        
        return organizations
    except Exception as e:
        # Log dell'errore ma non interrompere il caricamento della pagina
        import logging
        log = logging.getLogger(__name__)
        log.error(f"Errore nel recupero delle organizzazioni: {str(e)}")
        return []


def count_organizations():
    """
    Restituisce il numero di organizzazioni disponibili nel sistema
    """
    try:
        context = {'ignore_auth': True}
        data_dict = {'all_fields': True, 'include_users': False, 'include_extras': True}
        organizations = toolkit.get_action('organization_list')(context, data_dict)
        return len(organizations)
    except Exception as e:
        raise ValueError(f"Errore nel recupero delle organizzazioni: {str(e)}")


def get_recent_news(number=4):
    """
    Restituisce le ultime pagine/notizie disponibili nel sistema
    Helper personalizzato per sostituire h.get_recent_blog_posts() di ckanext-pages
    
    :param number: numero massimo di pagine da recuperare (default: 4)
    :return: lista delle pagine ordinate per data discendente
    """
    try:
        pages_list = toolkit.get_action('ckanext_pages_list')({}, {
            'private': False,
        })
        return pages_list[:number]
        
    except Exception as e:
        raise ValueError(f"Errore nel recupero delle pagine: {str(e)}")
    

def get_page_image(content):
    """
    Restituisce l'immagine di una pagina
    """
    try:
        class HTMLFirstImage(HTMLParser):
            def __init__(self):
                super().__init__()
                self.image_url = None

            def handle_starttag(self, tag, attrs):
                if tag == 'img' and not self.image_url:
                    for attr, value in attrs:
                        if attr == 'src':
                            self.image_url = value
                            break

        parser = HTMLFirstImage()
        parser.feed(content)
        image_url = parser.image_url
        return image_url
    except Exception as e:
        return None
    
def format_date(date_input, format='dmy'):
    """
    Formatta una data (stringa ISO o oggetto datetime) in formato italiano
    
    Args:
        date_input: Può essere una stringa ISO (es. "2024-07-20T11:34:23.364783") o un oggetto datetime
        format (str): Formato di output ('dmy' per "20 lug 2024", 'dmmy' per "20 luglio 2024", 'ymd' per "2024-07-20")
    
    Returns:
        str: Data formattata in italiano o None se errore
    """
    if not date_input:
        return None
    
    # Se è una stringa, convertila in oggetto datetime
    if isinstance(date_input, str):
        try:
            # Gestisce stringhe ISO con o senza microsecondi e timezone
            date_obj = datetime.fromisoformat(date_input.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            # Se non riesce a convertire, restituisce la stringa originale
            return date_input
    else:
        # È già un oggetto datetime
        date_obj = date_input
    
    # Dizionari per i mesi in italiano
    italian_months_short = {
        1: 'gen', 2: 'feb', 3: 'mar', 4: 'apr', 5: 'mag', 6: 'giu',
        7: 'lug', 8: 'ago', 9: 'set', 10: 'ott', 11: 'nov', 12: 'dic'
    }

    italian_months_long = {
        1: 'gennaio', 2: 'febbraio', 3: 'marzo', 4: 'aprile', 5: 'maggio', 6: 'giugno',
        7: 'luglio', 8: 'agosto', 9: 'settembre', 10: 'ottobre', 11: 'novembre', 12: 'dicembre'
    }
    
    # Formattazione in base al formato richiesto
    if format == 'dmy':
        day = date_obj.day
        month = italian_months_short[date_obj.month]
        year = date_obj.year
        return f"{day} {month} {year}"
    
    elif format == 'dmmy':
        day = date_obj.day
        month = italian_months_long[date_obj.month]
        year = date_obj.year
        return f"{day} {month} {year}"
        
    elif format == 'ymd':
        day = f"{date_obj.day:02d}"
        month = f"{date_obj.month:02d}"
        year = date_obj.year
        return f"{year}-{month}-{day}"
    
    return None


def _get_redis_connection():
    """
    Ottiene la connessione Redis utilizzando la configurazione CKAN.
    """
    try:
        import redis
        from ckan.common import config
        
        redis_url = config.get('ckan.redis.url')
        if redis_url:
            return redis.from_url(redis_url)
        else:
            # Fallback ai parametri separati se l'URL non è configurato
            redis_host = config.get('ckan.redis.host', 'localhost')
            redis_port = int(config.get('ckan.redis.port', 6379))
            redis_db = int(config.get('ckan.redis.db', 0))
            return redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    except Exception:
        return None


def _get_from_redis_cache(key):
    """
    Recupera un valore dalla cache Redis.
    """
    try:
        redis_conn = _get_redis_connection()
        if redis_conn:
            cached_value = redis_conn.get(key)
            if cached_value:
                return cached_value.decode('utf-8')
    except Exception:
        pass
    return None


def _set_redis_cache(key, value, ttl=3600):
    """
    Salva un valore nella cache Redis con TTL specificato.
    """
    try:
        redis_conn = _get_redis_connection()
        if redis_conn:
            redis_conn.setex(key, ttl, value)
    except Exception:
        pass


def get_first_theme(dataset_extras):
    """
    Estrae il primo valore del campo 'theme' da dataset.extras.
    
    Args:
        dataset_extras (list): Lista di dizionari con chiavi 'key' e 'value' dal campo extras del dataset
        
    Returns:
        str: Il primo tema estratto dal campo theme, o None se non trovato
        
    Example:
        Input: [{'key': 'theme', 'value': '["GOVE", "TECH"]'}, ...]
        Output: "GOVE"
    """
    try:
        if not dataset_extras:
            return None
            
        theme_extra = next((extra for extra in dataset_extras if extra.get('key', '').lower() == 'theme'), None)
        
        if not theme_extra or not theme_extra.get('value'):
            return None
            
        theme_value = theme_extra['value']
        
        # Se il valore è già una stringa semplice (non JSON), restituiscila
        if not theme_value.startswith('['):
            return theme_value.strip('"\'')
            
        # Prova a parsare come JSON
        try:
            theme_list = json.loads(theme_value)
            if isinstance(theme_list, list) and len(theme_list) > 0:
                return theme_list[0]
        except (json.JSONDecodeError, TypeError):
            # Se il parsing JSON fallisce, prova a estrarre manualmente
            # Rimuove [ ] e prende il primo elemento
            clean_value = theme_value.strip('[]')
            if clean_value:
                # Divide per virgola e prende il primo elemento
                first_theme = clean_value.split(',')[0].strip().strip('"\'')
                return first_theme
                
        return None
        
    except Exception as e:
        # In caso di errore, ritorna None
        return None


def extract_themes(pkg_extras, first_only=True):
    """
    Estrae i valori dei temi da pkg.extras
    
    Args:
        pkg_extras: Lista degli extras del package, formato [{'key': 'theme', 'value': '["TRAN"]'}]
        first_only (bool): Se True estrae solo il primo tema, se False estrae tutti i temi
        
    Returns:
        str o list: Se first_only=True restituisce il codice del primo tema (es. "TRAN") o None se non trovato.
                   Se first_only=False restituisce una lista di codici temi (es. ["TRAN", "ECON"]) o lista vuota se non trovati.
    """
    if not pkg_extras:
        return None if first_only else []
        
    try:
        for extra in pkg_extras:
            if extra.get('key').lower() == 'theme':
                theme_value = extra.get('value', '')
                if theme_value:
                    # Rimuove le parentesi quadre esterne
                    clean_value = theme_value.strip('[]"\'')
                    if clean_value:
                        # Divide per virgola e pulisce ogni elemento
                        themes = [theme.strip().strip('"\'') for theme in clean_value.split(',')]
                        # Filtra elementi vuoti
                        themes = [theme for theme in themes if theme]
                        
                        if first_only:
                            # Restituisce solo il primo tema
                            return themes[0] if themes else None
                        else:
                            # Restituisce tutti i temi
                            return themes
        
        return None if first_only else []
    except Exception as e:
        return None if first_only else []




def get_theme_icon(theme_code):
    """
    Restituisce l'icona SVG corretta per il codice tema specificato
    
    Args:
        theme_code (str): Codice del tema (es. "TRAN", "ENVI", ecc.)
        
    Returns:
        str: Nome dell'icona SVG (es. "outline--map")
    """
    theme_icons = {
        'ENVI': 'outline--sun',                    # Ambiente
        'REGI': 'outline--building-office',       # Regioni e città
        'GOVE': 'outline--building-library',      # Governo e settore pubblico
        'TECH': 'outline--beaker',                # Scienza e tecnologia
        'TRAN': 'outline--map',                   # Trasporti
        'ECON': 'outline--presentation-chart-bar', # Economia e finanza
        'ENER': 'outline--bolt',                  # Energia
        'EDUC': 'outline--book-open',             # Educazione, cultura e sport
        'SOCI': 'outline--user-group',            # Popolazione e società
        'HEAL': 'heart-rate-pulse-graph',         # Salute
        'AGRI': 'leaf--nature-environment-leaf-ecology-plant-plants-eco', # Agricoltura
        'JUST': 'outline--scale',                 # Giustizia e sicurezza pubblica
        'OP_DATPRO': 'outline--calendar-check',    # Dati provvisori
    }
    
    # Restituisce l'icona corrispondente o un'icona di default
    return theme_icons.get(theme_code, 'outline--sun')


def get_theme_name(theme_code):
    """
    Restituisce il nome leggibile del tema a partire dal codice, utilizzando le traduzioni
    
    Args:
        theme_code (str): Codice del tema (es. "ECON", "TRAN", ecc.)
        
    Returns:
        str: Nome leggibile del tema tradotto (es. "Economy and finance" in inglese, "Economia e finanza" in italiano)
    """
    # Importa toolkit per accedere alle traduzioni
    import ckan.plugins.toolkit as toolkit
    
    # 'ENVI': 'Ambiente',
    # 'REGI': 'Regioni e città', 
    # 'GOVE': 'Governo e settore pubblico',
    # 'TECH': 'Scienza e tecnologia',
    # 'TRAN': 'Trasporti',
    # 'ECON': 'Economia e finanza',
    # 'ENER': 'Energia',
    # 'EDUC': 'Educazione, cultura e sport',
    # 'SOCI': 'Popolazione e società',
    # 'HEAL': 'Salute',
    # 'AGRI': 'Agricoltura',
    # 'JUST': 'Giustizia e sicurezza pubblica',
    # 'OP_DATPRO': 'Dati provvisori'
    
    # Mappa dei codici tema alle stringhe inglesi (che verranno tradotte)
    theme_names = {
        'ENVI': 'Environment',
        'REGI': 'Regions and cities', 
        'GOVE': 'Government and public sector',
        'TECH': 'Science and technology',
        'TRAN': 'Transport',
        'ECON': 'Economy and finance',
        'ENER': 'Energy',
        'EDUC': 'Education, culture and sport',
        'SOCI': 'Population and society',
        'HEAL': 'Health',
        'AGRI': 'Agriculture',
        'JUST': 'Justice and public safety',
        'OP_DATPRO': 'Provisional data'
    }
    
    # Ottiene la stringa inglese e la traduce
    english_name = theme_names.get(theme_code, theme_code)
    return toolkit._(english_name)