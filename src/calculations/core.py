from typing import List, Dict, Any, Tuple
from collections import Counter
import math # Already imported, but good practice to be explicit if needed

from src.utils.helpers import setup_logger
from src.utils.math_utils import add, multiply, divide, power, calculate_std_dev, Vector2D # Added std_dev, Vector2D

logger = setup_logger(__name__)

def calculate_total_value(data: List[Dict[str, Any]]) -> float:
    """Calculates the sum of all 'value' fields in the processed data."""
    logger.info(f"Calculating total value for {len(data)} records.")
    total = 0.0
    for record in data:
        total = add(total, record.get('value', 0.0))
    logger.info(f"Total value calculated: {total}")
    return total

def calculate_weighted_average(data: List[Dict[str, Any]], weight_key: str = 'id') -> float:
    """Calculates a weighted average of 'value', weighted by another key (default 'id')."""
    logger.info(f"Calculating weighted average for {len(data)} records, weighted by '{weight_key}'.")
    total_value_sum = 0.0
    total_weight_sum = 0.0
    valid_records = 0
    for record in data:
        value = record.get('value')
        weight = record.get(weight_key)
        
        # Ensure both value and weight are numeric and present
        if isinstance(value, (int, float)) and isinstance(weight, (int, float)):
            total_value_sum = add(total_value_sum, multiply(value, weight))
            total_weight_sum = add(total_weight_sum, weight)
            valid_records += 1
        else:
            logger.debug(f"Skipping record for weighted average due to non-numeric/missing fields: {record}")

    if total_weight_sum == 0:
        logger.warning(f"Total weight is zero after processing {valid_records} valid records. Cannot calculate weighted average. Returning 0.")
        return 0.0
    
    weighted_avg = divide(total_value_sum, total_weight_sum)
    logger.info(f"Weighted average calculated using {valid_records} records: {weighted_avg}")
    return weighted_avg

def calculate_value_statistics(data: List[Dict[str, Any]], value_key: str = 'value') -> Dict[str, float]:
    """Calculates basic statistics (min, max, mean, std dev) for a given key."""
    logger.info(f"Calculating statistics for key '{value_key}' on {len(data)} records.")
    values = [record.get(value_key) for record in data if isinstance(record.get(value_key), (int, float))]
    
    if not values:
        logger.warning(f"No valid numeric data found for key '{value_key}'. Cannot calculate statistics.")
        return {'min': 0.0, 'max': 0.0, 'mean': 0.0, 'std_dev': 0.0, 'count': 0}
        
    stats = {
        'min': min(values),
        'max': max(values),
        'mean': sum(values) / len(values),
        'count': len(values)
    }
    
    # Standard deviation requires at least 2 points
    if len(values) >= 2:
        try:
            stats['std_dev'] = calculate_std_dev(values)
        except Exception as e:
            logger.error(f"Could not calculate standard deviation: {e}")
            stats['std_dev'] = float('nan') # Indicate calculation failure
    else:
        stats['std_dev'] = 0.0 # Std dev is 0 for single point, undefined for zero points
        
    logger.info(f"Statistics calculated for '{value_key}': {stats}")
    return stats

def find_most_common_categories(data: List[Dict[str, Any]], category_key: str = 'category', top_n: int = 3) -> List[Tuple[str, int]]:
    """Finds the most common values for a given category key."""
    logger.info(f"Finding top {top_n} most common categories for key '{category_key}'.")
    categories = [record.get(category_key, "Unknown") for record in data if category_key in record]
    if not categories:
        logger.warning(f"No data found for category key '{category_key}'.")
        return []
    
    category_counts = Counter(categories)
    most_common = category_counts.most_common(top_n)
    logger.info(f"Most common categories: {most_common}")
    return most_common

class AdvancedCalculator:
    def __init__(self, exponent: float = 2.0):
        self.exponent = exponent
        self.logger = setup_logger(f"{__name__}.AdvancedCalculator")

    def transform_values(self, data: List[Dict[str, Any]], value_key: str = 'value') -> List[Dict[str, Any]]:
        self.logger.info(f"Transforming values for {len(data)} records using exponent {self.exponent}")
        transformed_data = []
        errors = 0
        for record in data:
            new_record = record.copy()
            original_value = new_record.get(value_key)
            if isinstance(original_value, (int, float)):
                try:
                    transformed_value = power(original_value, self.exponent)
                    new_record[f"{value_key}_transformed"] = transformed_value
                except ValueError as e: # e.g., power might raise error for negative base with non-integer exp
                    self.logger.warning(f"Could not transform value {original_value} with exponent {self.exponent}: {e}")
                    new_record[f"{value_key}_transformed"] = None # Indicate transformation failure
                    errors += 1
            else:
                self.logger.debug(f"Skipping transformation for non-numeric value in record: {record}")
                new_record[f"{value_key}_transformed"] = None
                errors += 1
                
            transformed_data.append(new_record)
            
        self.logger.info(f"Transformation complete. Encountered {errors} issues.")
        return transformed_data

    def calculate_vector_sum(self, vectors: List[Vector2D]) -> Vector2D:
        """Calculates the sum of a list of Vector2D objects."""
        self.logger.info(f"Calculating sum of {len(vectors)} vectors.")
        if not vectors:
            return Vector2D(0, 0)
        
        sum_vector = Vector2D(0, 0)
        for vec in vectors:
            if isinstance(vec, Vector2D):
                sum_vector += vec
            else:
                self.logger.warning(f"Skipping non-Vector2D item during summation: {vec}")
        
        self.logger.info(f"Calculated vector sum: {sum_vector}")
        return sum_vector 