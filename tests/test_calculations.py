import pytest
from src.calculations import core

@pytest.fixture
def sample_processed_data():
    return [
        {'id': 1, 'name': 'A', 'value': 10.0},
        {'id': 2, 'name': 'B', 'value': 20.0},
        {'id': 3, 'name': 'C', 'value': 30.0}
    ]

def test_calculate_total_value(sample_processed_data):
    total = core.calculate_total_value(sample_processed_data)
    assert total == 60.0
    assert core.calculate_total_value([]) == 0.0
    assert core.calculate_total_value([{'id': 1}]) == 0.0 # Test missing value key

def test_calculate_weighted_average(sample_processed_data):
    # Weighted by 'id': (1*10 + 2*20 + 3*30) / (1 + 2 + 3) = (10 + 40 + 90) / 6 = 140 / 6
    expected_avg_by_id = 140.0 / 6.0
    avg_by_id = core.calculate_weighted_average(sample_processed_data, weight_key='id')
    assert avg_by_id == pytest.approx(expected_avg_by_id)

    # Weighted by 'value': (10*10 + 20*20 + 30*30) / (10 + 20 + 30) = (100 + 400 + 900) / 60 = 1400 / 60
    expected_avg_by_value = 1400.0 / 60.0
    avg_by_value = core.calculate_weighted_average(sample_processed_data, weight_key='value')
    assert avg_by_value == pytest.approx(expected_avg_by_value)

def test_calculate_weighted_average_zero_weight():
    data = [{'id': 0, 'value': 10}, {'id': 0, 'value': 20}]
    assert core.calculate_weighted_average(data, weight_key='id') == 0.0
    assert core.calculate_weighted_average([]) == 0.0

def test_advanced_calculator_transform(sample_processed_data):
    calculator = core.AdvancedCalculator(exponent=2.0)
    transformed = calculator.transform_values(sample_processed_data)
    assert len(transformed) == len(sample_processed_data)
    assert transformed[0]['value_transformed'] == 100.0 # 10^2
    assert transformed[1]['value_transformed'] == 400.0 # 20^2
    assert transformed[2]['value_transformed'] == 900.0 # 30^2
    assert 'value' in transformed[0] # Ensure original key is preserved

    calculator_half = core.AdvancedCalculator(exponent=0.5)
    transformed_half = calculator_half.transform_values(sample_processed_data)
    assert transformed_half[0]['value_transformed'] == pytest.approx(3.16227766) # sqrt(10) 