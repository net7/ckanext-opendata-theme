"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.opendata_theme.logic import validators


def test_opendata_theme_reauired_with_valid_value():
    assert validators.opendata_theme_required("value") == "value"


def test_opendata_theme_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.opendata_theme_required(None)
