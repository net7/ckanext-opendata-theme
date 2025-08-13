import ckan.plugins.toolkit as tk


def opendata_theme_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "opendata_theme_required": opendata_theme_required,
    }
