"""Tests for helpers.py."""

import ckanext.opendata_theme.helpers as helpers


def test_opendata_theme_hello():
    assert helpers.opendata_theme_hello() == "Hello, opendata_theme!"
