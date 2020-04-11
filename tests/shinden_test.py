import pytest
import shinden.scrapping as sh

def test_search_titles():
        results = sh.search_titles('alchemist')
        first_result = results[0]
        assert first_result.title == 'Fullmetal Alchemist'

def test_top_ten_titles():
        results = sh.get_top_ten_titles()
        assert len(results) == 10

def test_character():
        results = sh.search_characters('Violet Evergarden', 'contains', False)
        first_result = results[0]
        assert first_result.name == 'Violet Evergarden'

def test_tags():
        results = sh.get_tags()
        assert results != []

def test_user():
        results = sh.search_users('Shaderlight')
        first_result = results[0]
        assert first_result.nickname == 'Shaderlight'

def test_search_titles_without_result():
        results = sh.search_titles('jkfbsjhdfbwkefbdv wehfdfwejidhnjk')
        print(results)
        assert results == None

def test_search_character_without_result():
        results = sh.search_titles('jkfbsjhdfbwkefbdv wehfdfwejidhnjk')
        print(results)
        assert results == None

def test_user_without_result():
        results = sh.search_titles('jkfbsjhdfbwkefbdv wehfdfwejidhnjk')
        print(results)
        assert results == None