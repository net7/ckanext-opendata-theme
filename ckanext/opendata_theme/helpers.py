from pyproj import Transformer
from flask import request
import ckan.plugins.toolkit as toolkit
from html.parser import HTMLParser
import random
from datetime import datetime
import json
import re
import html


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
        "get_last_updated_datasets": get_last_updated_datasets,
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
        "get_current_package_notes": get_current_package_notes,
    }


def get_current_package_notes(package_id_or_name):
    """
    Restituisce le note del package (descrizione) con una chiamata fresca a package_show,
    usando la stessa logica di get_translated della pagina di lettura.
    Utile nel form di edit per evitare valori obsoleti passati dal contesto della view.
    """
    if not package_id_or_name:
        return ""
    try:
        pkg = toolkit.get_action("package_show")(
            {"for_view": True}, {"id": package_id_or_name}
        )
        return toolkit.h.get_translated(pkg, "notes") or pkg.get("notes") or ""
    except Exception:
        return ""


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
    Numero di dataset formattato, con cache applicativa.
    """
    return _cached('datasets', 'dataset_count', _get_formatted_dataset_count_uncached)


def _get_formatted_dataset_count_uncached():
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


def _get_current_lang():
    """
    Restituisce il codice della lingua corrente (es. 'it'), con fallback su 'it'.

    Serve a leggere le traduzioni da package_multilang senza passare da
    package_show.
    """
    try:
        lang = toolkit.request.environ.get('CKAN_LANG')
        if lang:
            return lang
    except Exception:
        pass
    try:
        from ckan.common import config
        return config.get('ckan.locale_default') or 'it'
    except Exception:
        return 'it'


# Colonne comuni alle due liste di dataset della homepage.
#
# Il titolo passa da package_multilang quando la traduzione esiste (LEFT JOIN +
# COALESCE): sostituire package_show con una query diretta su package.title
# mostrerebbe i titoli non tradotti. Il tema resta il valore grezzo dell'extra
# 'theme', che viene poi passato a extract_themes() per usare esattamente la
# stessa logica di parsing di prima.
_DATASET_CARD_COLUMNS = '''
            p.name AS name,
            COALESCE(pm.text, p.title) AS title,
            pe.value AS theme_raw,
            pa.value AS themes_aggregate_raw
'''

_DATASET_CARD_JOINS = '''
            LEFT JOIN package_multilang pm
                   ON pm.package_id = p.id
                  AND pm.field = 'title'
                  AND pm.lang = :lang
            LEFT JOIN package_extra pe
                   ON pe.package_id = p.id
                  AND pe.key = 'theme'
                  AND pe.state = 'active'
            LEFT JOIN package_extra pa
                   ON pa.package_id = p.id
                  AND pa.key = 'themes_aggregate'
                  AND pa.state = 'active'
'''


def _resolve_theme(theme_raw, themes_aggregate_raw):
    """
    Ricava il codice del tema con la stessa precedenza usata da dcatapit.

    dcatapit non salva l'extra 'theme' a database: lo sintetizza in
    package_show a partire da 'themes_aggregate' (vedi
    ckanext/dcatapit/plugin.py, after_show). Saltando package_show dobbiamo
    replicare quella precedenza:

      1. extra 'theme', se presente
      2. primo tema di 'themes_aggregate'
      3. 'GOVE' come default, come fa dcatapit quando l'aggregato manca
    """
    if theme_raw:
        theme = extract_themes([{'key': 'theme', 'value': theme_raw}])
        if theme:
            return theme

    if themes_aggregate_raw:
        try:
            aggregate = json.loads(themes_aggregate_raw)
        except (ValueError, TypeError):
            aggregate = None
        if aggregate:
            for entry in aggregate:
                if isinstance(entry, dict) and entry.get('theme'):
                    return entry['theme']

    return 'GOVE'


def _build_dataset_cards(rows):
    """
    Converte le righe della query nella forma attesa dai template della
    homepage: name, title, theme (codice), views.
    """
    cards = []
    for row in rows:
        cards.append({
            'name': row.name,
            'title': row.title,
            'theme': _resolve_theme(row.theme_raw, row.themes_aggregate_raw),
            'views': int(row.views or 0),
        })
    return cards


def get_most_viewed_datasets(limit=4):
    """
    Dataset più consultati, con cache applicativa.

    Args:
        limit (int): Numero massimo di dataset da restituire (default: 4)

    Returns:
        list: Lista di dizionari con chiavi name, title, theme, views
    """
    return _cached('datasets', 'most_viewed:%s:%s' % (limit, _get_current_lang()),
                   lambda: _get_most_viewed_datasets_uncached(limit))


def _get_most_viewed_datasets_uncached(limit=4):
    """
    Recupera i dataset più consultati in base alle statistiche di
    visualizzazione.

    Una sola query: name, titolo tradotto, tema e totale visualizzazioni. Non
    carica i package completi, quindi il costo non dipende dal numero di
    risorse dei dataset (il più visto ne ha oltre 900).

    Args:
        limit (int): Numero massimo di dataset da restituire (default: 4)

    Returns:
        list: Lista di dizionari con chiavi name, title, theme, views
    """
    try:
        from sqlalchemy import text
        from ckan.model import Session

        # I totali arrivano dalla vista materializzata package_views_summary,
        # aggiornata da `ckan opendata refresh-views-summary`. Aggregare
        # tracking_summary in linea costa ~0,8 s e cresce con la tabella.
        sql = '''
            SELECT {columns}, agg.views AS views
            FROM {fonte} agg
            JOIN package p
              ON p.id = agg.package_id
             AND p.state = 'active'
             AND p.private = false
            {joins}
            ORDER BY agg.views DESC
            LIMIT :limit
        '''
        fonte_materializzata = 'package_views_summary'
        fonte_diretta = '''(
                SELECT package_id, SUM(count) AS views
                FROM tracking_summary
                WHERE package_id IS NOT NULL
                  AND package_id != '~~not~found~~'
                GROUP BY package_id
            )'''
        params = {'limit': limit, 'lang': _get_current_lang()}

        try:
            rows = Session.execute(
                text(sql.format(columns=_DATASET_CARD_COLUMNS,
                                joins=_DATASET_CARD_JOINS,
                                fonte=fonte_materializzata)), params
            ).fetchall()
        except Exception:
            # La vista non esiste ancora (primo avvio dopo il rilascio): si
            # ricalcola, piu lentamente ma con lo stesso risultato.
            Session.rollback()
            import logging
            logging.getLogger(__name__).warning(
                "package_views_summary non disponibile, ricalcolo i totali da "
                "tracking_summary: creare la vista con "
                "vista_totali_visualizzazioni.sql")
            rows = Session.execute(
                text(sql.format(columns=_DATASET_CARD_COLUMNS,
                                joins=_DATASET_CARD_JOINS,
                                fonte=fonte_diretta)), params
            ).fetchall()

        return _build_dataset_cards(rows)
    except Exception:
        import logging
        logging.getLogger(__name__).exception(
            "Errore nel recupero dei dataset piu visti")
        return []


def get_last_updated_datasets(limit=4):
    """
    Dataset aggiornati di recente, con cache applicativa.

    Args:
        limit (int): Numero massimo di dataset da restituire (default: 4)

    Returns:
        list: Lista di dizionari con chiavi name, title, theme, views
    """
    return _cached('datasets', 'last_updated:%s:%s' % (limit, _get_current_lang()),
                   lambda: _get_last_updated_datasets_uncached(limit))


def _get_last_updated_datasets_uncached(limit=4):
    """
    Recupera i dataset più recentemente aggiornati in base a
    metadata_modified.

    Stessa forma di get_most_viewed_datasets: i dataset vengono prima
    selezionati e limitati, poi arricchiti con traduzione e tema.

    Args:
        limit (int): Numero massimo di dataset da restituire (default: 4)

    Returns:
        list: Lista di dizionari con chiavi name, title, theme, views
    """
    try:
        from sqlalchemy import text
        from ckan.model import Session

        sql = '''
            WITH recenti AS (
                SELECT id
                FROM package
                WHERE state = 'active'
                  AND private = false
                  AND metadata_modified IS NOT NULL
                ORDER BY metadata_modified DESC
                LIMIT :limit
            )
            SELECT {columns}, COALESCE(v.views, 0) AS views
            FROM recenti
            JOIN package p ON p.id = recenti.id
            {joins}
            LEFT JOIN LATERAL (
                SELECT SUM(count) AS views
                FROM tracking_summary ts
                WHERE ts.package_id = p.id
            ) v ON true
            ORDER BY p.metadata_modified DESC
        '''.format(columns=_DATASET_CARD_COLUMNS, joins=_DATASET_CARD_JOINS)

        rows = Session.execute(
            text(sql), {'limit': limit, 'lang': _get_current_lang()}
        ).fetchall()
        return _build_dataset_cards(rows)
    except Exception:
        import logging
        logging.getLogger(__name__).exception(
            "Errore nel recupero dei dataset aggiornati di recente")
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
    Organizzazioni del carosello della homepage, con cache applicativa.

    Returns:
        list: Lista di dizionari con chiavi name, title, image_display_url
    """
    return _cached('organizations', 'home_orgs:%s' % _get_current_lang(),
                   _get_home_organizations_uncached)


def _get_home_organizations_uncached():
    """
    Restituisce le organizzazioni mostrate nel carosello della homepage.

    Una sola query per tutti gli enti dell'elenco. Il template usa soltanto
    name, title e image_display_url: organization_show caricava molto altro
    (130 query per 13 enti, oltre 600 con include_datasets).

    L'ordine dell'elenco viene mantenuto; gli enti non trovati sono saltati
    silenziosamente, come faceva la versione precedente.
    """
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
    try:
        from sqlalchemy import text
        from ckan.model import Session

        sql = """
            SELECT g.name AS name,
                   COALESCE(gm.text, g.title) AS title,
                   g.image_url AS image_url
            FROM "group" g
            LEFT JOIN group_multilang gm
                   ON gm.group_id = g.id
                  AND gm.field = 'title'
                  AND gm.lang = :lang
            WHERE g.is_organization = true
              AND g.state = 'active'
              AND g.name = ANY(:names)
        """
        rows = Session.execute(
            text(sql),
            {'names': organizations_names, 'lang': _get_current_lang()}
        ).fetchall()

        by_name = {
            row.name: {
                'name': row.name,
                'title': row.title,
                'image_display_url': _group_image_display_url(row.image_url),
            }
            for row in rows
        }
        # Rispetta l'ordine dell'elenco sopra, non quello del database.
        return [by_name[name] for name in organizations_names if name in by_name]
    except Exception:
        import logging
        logging.getLogger(__name__).exception(
            "Errore nel recupero delle organizzazioni della homepage")
        return []


def _group_image_display_url(image_url):
    """
    Costruisce image_display_url come fa group_dictize di CKAN: l'URL assoluto
    resta com'è, il nome di un file caricato diventa un URL sotto
    uploads/group/.
    """
    if not image_url:
        return image_url
    if image_url.startswith('http'):
        return image_url
    try:
        return toolkit.h.url_for_static(
            'uploads/group/%s' % image_url, qualified=True)
    except Exception:
        return image_url


def count_organizations():
    """
    Numero di organizzazioni con almeno un dataset, con cache applicativa.

    Returns:
        int
    """
    return _cached('organizations', 'count_orgs', _count_organizations_uncached)


def _count_organizations_uncached():
    """
    Restituisce il numero di organizzazioni con almeno un dataset attivo e
    pubblico.

    Una sola query di conteggio: organization_list(all_fields=True,
    include_extras=True) caricava tutte le organizzazioni con extras e
    package_count (197 query, ~1,1 s) solo per contarne una parte.
    """
    try:
        from sqlalchemy import text
        from ckan.model import Session

        sql = """
            SELECT count(*)
            FROM "group" g
            WHERE g.is_organization = true
              AND g.state = 'active'
              AND EXISTS (
                  SELECT 1
                  FROM package p
                  WHERE p.owner_org = g.id
                    AND p.state = 'active'
                    AND p.private = false
              )
        """
        return Session.execute(text(sql)).scalar() or 0
    except Exception:
        import logging
        logging.getLogger(__name__).exception(
            "Errore nel conteggio delle organizzazioni")
        return 0


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


# --- Cache applicativa della homepage -------------------------------------
#
# Le utility _get_from_redis_cache / _set_redis_cache trattano solo stringhe
# (fanno .decode('utf-8') sul valore) e aprono una connessione nuova a ogni
# chiamata: vanno bene per il contatore testuale di get_formatted_view_count,
# non per liste di dizionari. Qui sopra ci mettiamo un livello che serializza in
# JSON e riusa una sola connessione.
#
# La cache è un accorgimento di latenza, non il rimedio a una query lenta: i
# dati pesanti sono già pre-aggregati in package_views_summary. Per questo i TTL
# di default sono corti, a vantaggio della freschezza.

_HOMEPAGE_CACHE_PREFIX = 'opendata_theme:homepage:'

# Secondi. Sovrascrivibili da ckan.ini con le chiavi indicate.
_CACHE_TTL_DEFAULTS = {
    # ckanext.opendata_theme.cache_ttl.datasets
    'datasets': 300,
    # ckanext.opendata_theme.cache_ttl.organizations
    'organizations': 3600,
}

_redis_connection = None
_redis_unavailable_logged = False


def _get_shared_redis_connection():
    """
    Restituisce una connessione Redis riusata tra le chiamate, o None se non è
    possibile crearla.

    Il caso "None" viene segnalato nei log una volta sola: senza questo
    avviso una configurazione sbagliata di ckan.redis.url spegnerebbe la cache
    in silenzio, perché la homepage continuerebbe a funzionare ricalcolando
    tutto a ogni richiesta.
    """
    global _redis_connection, _redis_unavailable_logged
    if _redis_connection is None:
        _redis_connection = _get_redis_connection()
        if _redis_connection is None and not _redis_unavailable_logged:
            _redis_unavailable_logged = True
            import logging
            from ckan.common import config
            logging.getLogger(__name__).warning(
                "Cache della homepage disattivata: nessuna connessione Redis "
                "(ckan.redis.url = %r). La homepage funziona comunque, ma "
                "ricalcola i dati a ogni richiesta.",
                config.get('ckan.redis.url'))
    return _redis_connection


def _get_cache_ttl(kind):
    """
    TTL in secondi per una famiglia di dati della homepage.

    Un TTL a 0 (o negativo) disattiva la cache per quella famiglia, il che
    permette di spegnerla da configurazione senza toccare il codice.
    """
    try:
        from ckan.common import config
        value = config.get(
            'ckanext.opendata_theme.cache_ttl.%s' % kind)
        if value not in (None, ''):
            return int(value)
    except Exception:
        pass
    return _CACHE_TTL_DEFAULTS.get(kind, 0)


def _cached(kind, key, producer):
    """
    Restituisce il valore in cache per `key`, altrimenti lo calcola con
    `producer` e lo memorizza.

    Se Redis non risponde o il contenuto non è leggibile, il valore viene
    ricalcolato e restituito comunque: la homepage non deve dipendere dalla
    disponibilità della cache.
    """
    ttl = _get_cache_ttl(kind)
    if ttl <= 0:
        return producer()

    full_key = _HOMEPAGE_CACHE_PREFIX + key
    log = None
    try:
        connection = _get_shared_redis_connection()
        if connection is not None:
            cached = connection.get(full_key)
            if cached:
                return json.loads(cached)
    except Exception:
        import logging
        log = logging.getLogger(__name__)
        log.warning("Cache della homepage non leggibile (%s), "
                    "ricalcolo i dati", full_key, exc_info=True)

    value = producer()

    try:
        connection = _get_shared_redis_connection()
        if connection is not None:
            connection.setex(full_key, ttl, json.dumps(value))
    except Exception:
        import logging
        (log or logging.getLogger(__name__)).warning(
            "Cache della homepage non scrivibile (%s)", full_key,
            exc_info=True)

    return value


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
        'REGI': 'outline--building-office',        # Regioni e città
        'GOVE': 'outline--building-library',       # Governo e settore pubblico
        'TECH': 'outline--beaker',                 # Scienza e tecnologia
        'TRAN': 'outline--map',                    # Trasporti
        'ECON': 'outline--presentation-chart-bar', # Economia e finanza
        'ENER': 'outline--bolt',                   # Energia
        'EDUC': 'outline--book-open',              # Educazione, cultura e sport
        'SOCI': 'outline--user-group',             # Popolazione e società
        'HEAL': 'heart-rate-pulse-graph',          # Salute
        'AGRI': 'leaf--nature-environment-leaf-ecology-plant-plants-eco', # Agricoltura
        'JUST': 'outline--scale',                  # Giustizia e sicurezza pubblica
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


def get_org_defaults_for_dataset(org_id):
    if not org_id:
        return {}
    try:
        org = toolkit.get_action('organization_show')(
            {'ignore_auth': True},
            {'id': org_id, 'include_extras': True}
        )
        org_email = ''
        for extra in org.get('extras', []):
            if extra.get('key') == 'email':
                org_email = extra.get('value', '')
                break
        org_title = org.get('title', '')
        defaults = {
            'author': org_title,
            'author_email': org_email,
            'maintainer': org_title,
            'maintainer_email': org_email,
        }
        return defaults
    except Exception:
        return {}


def render_markdown(text):
    """
    Converte testo con Markdown semplice e entità HTML in HTML formattato.
    Gestisce:
    - Link in formato [testo](url) 
    - Entità HTML come &#8226; (bullet points)
    - Line breaks
    - URL automatici
    
    Args:
        text (str): Testo da convertire
        
    Returns:
        str: HTML formattato
    """
    if not text:
        return ""
    
    # Decodifica entità HTML (es. &#8226; diventa •)
    text = html.unescape(text)
    
    # Converte link Markdown [testo](url) in HTML
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Converte URL semplici in link (solo se non sono già dentro tag <a>)
    text = re.sub(r'(?<!href=")(?<!href=\")(?<!>)(https?://[^\s<>"]+)', r'<a href="\1">\1</a>', text)
    
    # Converte line breaks in <br>
    text = text.replace('\n', '<br>')
    
    return text

