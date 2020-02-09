import pytest
from shinden.scrapping import *

def test_search_titles():
        results = search_titles('alchemist')
        first_result = results[0]
        assert first_result.title == 'Fullmetal Alchemist'

def test_top_ten_titles():
        results = get_top_ten_titles()
        assert len(results) == 10

def test_character():
        results = search_characters('Violet Evergarden', 'contains', False)
        first_result = results[0]
        assert first_result.name == 'Violet Evergarden'

def test_tags():
        results = get_tags()
        assert results != []

def test_user():
        results = search_users('Shaderlight')
        first_result = results[0]
        assert first_result.nickname == 'Shaderlight'