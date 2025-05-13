import pytest
from src.data_processing import loader, parser

@pytest.fixture
def sample_raw_data():
    return [
        {'id': '1', 'name': ' Apple ', 'value': '10.5'},
        {'id': '2', 'name': 'Banana!', 'value': '20'},
        {'id': '3', 'name': 'Cherry?', 'value': '-5.0'}
    ]

@pytest.fixture
def sample_parsed_data():
    return [
        {'id': 1, 'name': 'Apple', 'value': 10.5},
        {'id': 2, 'name': 'Banana', 'value': 20.0},
        {'id': 3, 'name': 'Cherry', 'value': -5.0}
    ]

def test_load_dummy_data():
    data = loader.load_dummy_data()
    assert isinstance(data, list)
    assert len(data) == 4
    assert 'id' in data[0]
    assert 'name' in data[0]
    assert 'value' in data[0]

def test_parse_raw_data(sample_raw_data, sample_parsed_data):
    parsed = parser.parse_raw_data(sample_raw_data)
    assert parsed == sample_parsed_data

def test_parse_raw_data_errors():
    bad_data = [
        {'id': '1', 'name': 'Good'},
        {'id': 'bad', 'name': 'Bad ID', 'value': '10'},
        {'id': '3', 'name': 'Bad Value', 'value': 'abc'},
    ]
    parsed = parser.parse_raw_data(bad_data)
    # Only the first record is partially valid (missing value), 
    # the others cause errors and are skipped.
    # Let's check based on logs or expected output size if strict.
    # For this simple test, we expect it *not* to crash and return an empty list
    # as all records have issues that cause them to be skipped by the error handling.
    assert len(parsed) == 0 # Adjust based on actual skipping logic

# Note: Testing classes like DataLoader and DataParser might require mocking
# dependencies (like file reads or other modules), which is more involved.
# These tests cover the core functions for simplicity. 