# -*- coding: utf-8 -*-
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ckanext-opendata_theme',
    version='1.0.0',
    description='Opendata Theme',
    long_description='Tema OpenData per CKAN',
    classifiers=[],
    keywords='',
    author='Net7',
    author_email='info@netseven.it',
    url='https://gitlab.netseven.it/net7-main/ckan/ckanext-opendata-theme',
    entry_points='''
        [ckan.plugins]
        opendata_theme=ckanext.opendata_theme.plugin:OpendataThemePlugin
    ''',

    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates/**.html', 'ckan', None),
        ],
    },
    include_package_data=True,
    package_data={
        'opendata_theme': [
            'assets/css/*.css',
            'assets/js/*.js',
            'templates/*.html'
        ]
    }
)
