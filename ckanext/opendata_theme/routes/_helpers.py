# !/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-contact
# Created by the Natural History Museum in London, UK
import logging
import socket
from datetime import datetime, timezone

from ckan import logic
from ckan.common import asbool
from ckan.lib import mailer
from ckan.lib.navl.dictization_functions import unflatten
from ckan.plugins import PluginImplementations, toolkit
from pyisemail import is_email

from ckanext.contact import recaptcha
from ckanext.contact.interfaces import IContact

log = logging.getLogger(__name__)


def validate(data_dict):
    """
    Validates the given data and recaptcha if necessary.

    :param data_dict: the request params as a dict
    :returns: a 3-tuple of errors, error summaries and a recaptcha error, in the event
        where no issues occur the return is ({}, {}, None)
    """
    errors = {}
    error_summary = {}
    optional_fields = {'codice_ipa', 'organization_logo'}
    recaptcha_error = None

    # check each field to see if it has a value and if not, show and error
    for field, value in data_dict.items():
        # we know the save field is not necessary and may be empty so ignore it
        if field == 'save':
            continue
        # ignore optionals
        if field in optional_fields:
            continue
        if value is None or value == '':
            errors[field] = ['Missing Value']
            error_summary[field] = 'Missing value'

    # check the organization email address, if there is one and the config option isn't off
    if (
        toolkit.asbool(toolkit.config.get('ckanext.contact.check_email', True))
        and data_dict.get('organization_email')
    ):
        if not is_email(data_dict['organization_email'], check_dns=True):
            errors['organization_email'] = ['Email address appears to be invalid']
            error_summary['organization_email'] = 'Email address appears to be invalid'
    
    # check the user email address if present
    if (
        toolkit.asbool(toolkit.config.get('ckanext.contact.check_email', True))
        and data_dict.get('user_email')
    ):
        if not is_email(data_dict['user_email'], check_dns=True):
            errors['user_email'] = ['Email address appears to be invalid']
            error_summary['user_email'] = 'Email address appears to be invalid'

    # validate organization logo file if present
    if 'organization_logo' in data_dict and data_dict['organization_logo']:
        logo_file = data_dict['organization_logo']
        # Check if it's a file upload object (has filename attribute)
        if hasattr(logo_file, 'filename') and logo_file.filename:
            # Check file extension
            allowed_extensions = {'.jpg', '.jpeg', '.png'}
            file_ext = '.' + logo_file.filename.lower().split('.')[-1] if '.' in logo_file.filename else ''
            if file_ext not in allowed_extensions:
                errors['organization_logo'] = ['File deve essere .jpg, .jpeg o .png']
                error_summary['organization_logo'] = 'Formato file non supportato'
            
            # Check file size (1MB = 1048576 bytes)
            elif hasattr(logo_file, 'content_length') and logo_file.content_length > 1048576:
                errors['organization_logo'] = ['File troppo grande (massimo 1MB)']
                error_summary['organization_logo'] = 'File troppo grande'

    # only check the recaptcha if there are no errors
    if not errors:
        try:
            expected_action = toolkit.config.get('ckanext.contact.recaptcha_v3_action')
            # check the recaptcha value, this only does anything if recaptcha is setup
            recaptcha.check_recaptcha(
                data_dict.get('g-recaptcha-response', None), expected_action
            )
        except recaptcha.RecaptchaError as e:
            log.info(f'Recaptcha failed due to "{e}"')
            recaptcha_error = toolkit._('Recaptcha check failed, please try again.')

    return errors, error_summary, recaptcha_error


def build_subject(
    organization_name=None, subject=None, default='Nuova richiesta di adesione ad OpenData Toscana', timestamp_default=False
):
    """
    Creates the subject line for the contact email using the organization name.

    :param organization_name: the name of the organization requesting access
    :param subject: a user defined subject line (not used for registration form)
    :param default: the default str to use as base subject
    :param timestamp_default: the default bool to use if add_timestamp_to_subject isn't
        specified
    :returns: the subject line
    """
    # Per il form di registrazione, usa sempre un subject personalizzato con il nome organizzazione
    if organization_name:
        subject = f'{default}: {organization_name}'
    else:
        subject = default
    
    if asbool(
        toolkit.config.get(
            'ckanext.contact.add_timestamp_to_subject', timestamp_default
        )
    ):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
        subject = f'{subject} [{timestamp}]'

    prefix = toolkit.config.get('ckanext.contact.subject_prefix', '')

    return f'{prefix}{" " if prefix else ""}{subject}'


def submit():
    """
    Take the data in the request params and send an email using them. If the data is
    invalid or a recaptcha is setup and it fails, don't send the email.

    :returns: a dict of details
    """
    # this variable holds the status of sending the email
    email_success = True

    # pull out the data from the request
    data_dict = logic.clean_dict(
        unflatten(logic.tuplize_dict(logic.parse_params(toolkit.request.values)))
    )
    
    # Handle file uploads separately
    if toolkit.request.files:
        for field_name, file_obj in toolkit.request.files.items():
            if file_obj and file_obj.filename:
                data_dict[field_name] = file_obj

    # validate the request params
    errors, error_summary, recaptcha_error = validate(data_dict)

    # if there are not errors and no recaptcha error, attempt to send the email
    if len(errors) == 0 and recaptcha_error is None:
        body_parts = [
            'Richiesta di registrazione inviata da:',
            f'  Nome organizzazione: {data_dict["organization_name"]}',
            f'  Email organizzazione: {data_dict["organization_email"]}',
            f'  Nome utente: {data_dict["user_name"]}',
            f'  Email utente: {data_dict["user_email"]}',
        ]
        
        # Add IPA code if present
        if data_dict.get('codice_ipa'):
            body_parts.append(f'  Codice IPA: {data_dict["codice_ipa"]}')
        else:
            body_parts.append('  Codice IPA: Non specificato')
            
        # Add logo information if present
        if data_dict.get('organization_logo') and hasattr(data_dict['organization_logo'], 'filename'):
            logo_file = data_dict['organization_logo']
            body_parts.append(f'  Logo organizzazione: {logo_file.filename} (caricato)')
        else:
            body_parts.append('  Logo organizzazione: Non fornito')
            
        mail_dict = {
            'recipient_email': toolkit.config.get(
                'ckanext.contact.mail_to', toolkit.config.get('email_to')
            ),
            'recipient_name': toolkit.config.get(
                'ckanext.contact.recipient_name', toolkit.config.get('ckan.site_title')
            ),
            'subject': build_subject(organization_name=data_dict.get('organization_name')),
            'body': '\n'.join(body_parts),
            'headers': {'reply-to': data_dict['organization_email']},
        }

        # allow other plugins to modify the mail_dict
        for plugin in PluginImplementations(IContact):
            plugin.mail_alter(mail_dict, data_dict)

        # note the pop here so that we don't get parameter clashes when we call
        # mail_recipient below
        emails = mail_dict.pop('recipient_email')
        names = mail_dict.pop('recipient_name')
        if isinstance(emails, str):
            emails = [emails]
            names = [names]

        # send the email to each name/email pair
        for name, email in zip(names, emails):
            try:
                mailer.mail_recipient(name, email, **mail_dict)
            except (mailer.MailerException, socket.error):
                email_success = False

    return {
        'success': recaptcha_error is None and len(errors) == 0 and email_success,
        'data': data_dict,
        'errors': errors,
        'error_summary': error_summary,
        'recaptcha_error': recaptcha_error,
    }
