import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins import SingletonPlugin, implements
from . import cli
from ckanext.opendata_theme import helpers
from ckanext.opendata_theme.cli import get_commands

# import ckanext.opendata_theme.cli as cli
# import ckanext.opendata_theme.helpers as helpers
import ckanext.opendata_theme.views as views
# from ckanext.opendata_theme.logic import (
#     action, auth, validators
# )


class OpendataThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IClick)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    
    # plugins.implements(plugins.IAuthFunctions)
    # plugins.implements(plugins.IActions)
    # plugins.implements(plugins.IClick)
    # plugins.implements(plugins.ITemplateHelpers)
    # plugins.implements(plugins.IValidators)


    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("assets", "opendata-theme")
        toolkit.add_resource('fanstatic', 'opendata_theme')

    
    # IAuthFunctions

    # def get_auth_functions(self):
    #     return auth.get_auth_functions()

    # IActions

    # def get_actions(self):
    #     return action.get_actions()

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprints()

    # IClick

    def get_commands(self):
        return get_commands()

    # ITemplateHelpers

    def get_helpers(self):
        """
        Registra gli helper personalizzati disponibili nei template.
        """
        return {
            'is_current': helpers.is_current,
            'get_formatted_dataset_count': helpers.get_formatted_dataset_count,
            'get_formatted_view_count': helpers.get_formatted_view_count,
            'get_formatted_download_count': helpers.get_formatted_download_count,
            'get_most_viewed_datasets': helpers.get_most_viewed_datasets,
            'get_dataset_views': helpers.get_dataset_views,
            'get_dataset_downloads': helpers.get_dataset_downloads,
            'opendata_theme_get_helpers': helpers.get_helpers,
            'get_all_organizations': helpers.get_all_organizations,
            'get_all_organizations_random': helpers.get_all_organizations_random,
            'count_organizations': helpers.count_organizations,
            'get_recent_news': helpers.get_recent_news,
            'get_page_image': helpers.get_page_image
        }

    # IValidators

    # def get_validators(self):
    #     return validators.get_validators()
    
