import pytest
from src.utils import helpers, string_utils, math_utils

def test_get_current_timestamp():
    ts = helpers.get_current_timestamp()
    assert isinstance(ts, str)
    assert len(ts) > 10 # Basic check for ISO format

def test_format_data():
    data = {'a': 1, 'b': 'test'}
    formatted = helpers.format_data(data)
    assert "a: 1" in formatted
    assert "b: test" in formatted
    assert formatted.startswith("{\n")
    assert formatted.endswith("\n}")

def test_sanitize_string():
    assert string_utils.sanitize_string("Hello! World? 123.") == "Hello World 123"
    assert string_utils.sanitize_string("@#$%^") == ""

def test_capitalize_words():
    assert string_utils.capitalize_words("hello world") == "Hello World"
    assert string_utils.capitalize_words(" single ") == "Single"

def test_reverse_string():
    assert string_utils.reverse_string("abc") == "cba"
    assert string_utils.reverse_string("") == ""

def test_add():
    assert math_utils.add(1, 2) == 3
    assert math_utils.add(-1, 1) == 0

def test_subtract():
    assert math_utils.subtract(5, 2) == 3

def test_multiply():
    assert math_utils.multiply(3, 4) == 12

def test_divide():
    assert math_utils.divide(10, 2) == 5
    with pytest.raises(ValueError):
        math_utils.divide(1, 0)

def test_power():
    assert math_utils.power(2, 3) == 8
    assert math_utils.power(5, 0) == 1 