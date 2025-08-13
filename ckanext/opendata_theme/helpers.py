from pyproj import Transformer
from flask import request
import ckan.plugins.toolkit as toolkit
from html.parser import HTMLParser

def opendata_theme_hello():
    return "Hello, opendata_theme!"


def get_helpers():
    return {
        "opendata_theme_hello": opendata_theme_hello,
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
    Restituisce il numero di visualizzazioni dell'anno precedente formattato in stile italiano.
    """
    try:
        # Accesso diretto al database usando SQLAlchemy
        from sqlalchemy import text
        from ckan.model import Session
        
        # Usa sempre l'anno precedente a quello corrente
        year_condition = "EXTRACT(YEAR FROM tracking_date) = EXTRACT(YEAR FROM CURRENT_DATE) - 1"
            
        sql = f'''
            SELECT SUM(count) as total_count
            FROM tracking_summary
            WHERE tracking_type = 'page' 
            AND {year_condition}
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
                return f"+{millions} milione"
            else:
                return f"+{millions} milioni"
        # Formattazione per numeri in migliaia
        elif view_count >= 1000:
            thousands = round(view_count / 1000)
            return f"+{thousands} mila"
        else:
            return f"{view_count:,}".replace(',', '.')
    except Exception as e:
        # In caso di errore, ritorna il valore statico originale
        return f"+0"


def get_formatted_download_count():
    """
    Restituisce il numero di download dell'anno precedente formattato in stile italiano.
    """
    try:
        # Accesso diretto al database usando SQLAlchemy
        from sqlalchemy import text
        from ckan.model import Session
        
        # Usa sempre l'anno precedente a quello corrente
        year_condition = "EXTRACT(YEAR FROM tracking_date) = EXTRACT(YEAR FROM CURRENT_DATE) - 1"
            
        sql = f'''
            SELECT SUM(count) as total_count
            FROM tracking_summary
            WHERE tracking_type = 'resource' 
            AND {year_condition}
        '''
        
        # Esegui la query direttamente
        result = Session.execute(text(sql))
        row = result.fetchone()
        
        if row and row.total_count:
            download_count = row.total_count
        else:
            download_count = 0
        
        # Formattazione per numeri in migliaia
        if download_count >= 1000:
            thousands = round(download_count / 1000)
            return f"+{thousands} mila"
        else:
            return f"{download_count:,}".replace(',', '.')
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
                dataset = toolkit.get_action('package_show')({}, {'id': package_id})
                dataset['view_count'] = get_dataset_views(package_id)
                dataset['download_count'] = 0
                datasets.append(dataset)
            except toolkit.ObjectNotFound:
                # Ignora i dataset che non esistono più
                continue
                
        return datasets
    except Exception as e:
        # In caso di errore, ritorna una lista vuota
        return []


def get_dataset_views(package_id):
    """
    Restituisce il numero di visualizzazioni per un dataset.
    
    Args:
        package_id (str): L'ID del dataset di cui calcolare i download
        
    Returns:
        int: Numero totale di visualizzazioni
    """
    try:
        # Accesso diretto al database usando SQLAlchemy
        from sqlalchemy import text
        from ckan.model import Session
        
        if not package_id:
            return 0
            
        sql = '''
            SELECT SUM(count) as total_views
            FROM tracking_summary
            WHERE package_id = :package_id
            AND tracking_type = 'page'
        '''
        
        result = Session.execute(text(sql), {'package_id': package_id})
        row = result.fetchone()
        
        if row and row.total_views:
            return row.total_views
        return 0
    except Exception as e:
        # In caso di errore, ritorna 0
        return 0


def get_dataset_downloads(package_id):
    """
    Calcola il numero totale di download per tutte le risorse di un dataset.
    
    Args:
        package_id (str): L'ID del dataset di cui calcolare i download
        
    Returns:
        int: Numero totale di download di tutte le risorse
    """
    try:
        from sqlalchemy import text
        from ckan.model import Session
        
        if not package_id:
            return 0
            
        sql = '''
            SELECT SUM(ts.count) as total_downloads
            FROM tracking_summary ts
            JOIN resource r ON ts.object_id = r.id
            WHERE r.package_id = :package_id
            AND ts.tracking_type = 'resource'
        '''
        
        result = Session.execute(text(sql), {'package_id': package_id})
        row = result.fetchone()
        
        if row and row.total_downloads:
            return row.total_downloads
        return 0
    except Exception as e:
        return 0


def get_all_organizations():
    """
    Restituisce tutte le organizzazioni disponibili nel sistema
    """
    try:
        context = {'ignore_auth': True}
        data_dict = {'all_fields': True, 'include_users': False, 'include_extras': True}
        organizations = toolkit.get_action('organization_list')(context, data_dict)
        return organizations
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