from flask import Blueprint
from ckanext.opendata_theme import utils

def get_blueprints():
    """
    Restituisce i blueprint per le pagine statiche del tema opendata
    """
    blueprints = []
    
    # Blueprint per la pagina credits
    credits_blueprint = Blueprint(
        'opendata_theme_credits',
        __name__,
        url_prefix='/credits'
    )
    credits_blueprint.add_url_rule(
        '/',
        'index',
        utils.credits_index,
        methods=['GET']
    )
    blueprints.append(credits_blueprint)
    
    # Blueprint per la pagina infografica
    infog_blueprint = Blueprint(
        'opendata_theme_infog',
        __name__,
        url_prefix='/infografica'
    )
    infog_blueprint.add_url_rule(
        '/',
        'index',
        utils.infog_index,
        methods=['GET']
    )
    blueprints.append(infog_blueprint)
    
    # Blueprint per la pagina report
    report_blueprint = Blueprint(
        'opendata_theme_report',
        __name__,
        url_prefix='/report'
    )
    report_blueprint.add_url_rule(
        '/',
        'index',
        utils.reports_index,
        methods=['GET']
    )
    blueprints.append(report_blueprint)
    
    return blueprints