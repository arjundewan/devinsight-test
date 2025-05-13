from typing import List, Dict, Any, Optional, Tuple
import datetime

from src.utils.helpers import setup_logger
from src.utils.string_utils import sanitize_string, capitalize_words, snake_to_camel
from .loader import DataLoader # Relative import from within the same package

logger = setup_logger(__name__)

# Define expected schema for validation
EXPECTED_SCHEMA = {
    'id': int,
    'name': str,
    'value': float,
    'category': str,
    'timestamp': datetime.datetime
}

# Define valid categories (example)
VALID_CATEGORIES = {"FRUIT", "VEGETABLE", "GRAIN", "DAIRY", "UNKNOWN"}

def validate_record(record: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Validates a single parsed record against the schema and constraints."""
    for key, expected_type in EXPECTED_SCHEMA.items():
        if key not in record:
            return False, f"Missing key: '{key}'"
        if not isinstance(record[key], expected_type):
            return False, f"Invalid type for '{key}': Expected {expected_type.__name__}, got {type(record[key]).__name__}"

    # Specific field validation
    if record['value'] < -1000 or record['value'] > 10000:
        return False, f"Value {record['value']} out of reasonable range (-1000 to 10000)"
    
    if record['category'] not in VALID_CATEGORIES:
        logger.warning(f"Category '{record['category']}' not in standard list {VALID_CATEGORIES}. Treating as UNKNOWN.")
        record['category'] = "UNKNOWN" # Standardize unknown categories
        
    # Example: Ensure timestamp is not in the future (allowing for some clock skew)
    if record['timestamp'] > datetime.datetime.now() + datetime.timedelta(minutes=5):
        return False, f"Timestamp {record['timestamp']} is in the future"
        
    return True, None

def parse_raw_data(raw_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Parses and cleans the raw data, including validation and type conversion."""
    logger.info(f"Parsing {len(raw_data)} raw records.")
    parsed_data = []
    skipped_records = 0
    validation_errors = 0

    for i, raw_record in enumerate(raw_data):
        try:
            # Basic parsing and cleaning
            cleaned_name = capitalize_words(sanitize_string(raw_record.get('name', '')))
            record_id_str = raw_record.get('id')
            record_value_str = raw_record.get('value')
            record_category_raw = raw_record.get('category', 'Unknown')
            record_ts_str = raw_record.get('timestamp', datetime.datetime.now().isoformat()) # Default timestamp

            if record_id_str is None or record_value_str is None:
                raise KeyError("Missing essential keys 'id' or 'value'")

            # Attempt type conversions
            parsed_record = {
                'id': int(record_id_str),
                'name': cleaned_name,
                'value': float(record_value_str),
                'category': record_category_raw.upper().strip(), # Standardize category format
                'timestamp': datetime.datetime.fromisoformat(record_ts_str.replace('Z', '+00:00')) # Handle ISO format
            }
            
            # Apply complex field name transformation (example)
            # Let's imagine the source had 'item_id' instead of 'id' sometimes
            if 'item_id' in raw_record and 'id' not in raw_record:
                 parsed_record['id'] = int(raw_record['item_id'])
            
            # Convert keys to camelCase if needed (demonstration)
            # camel_case_record = {snake_to_camel(k): v for k, v in parsed_record.items()}
            # We'll stick to snake_case for consistency here, but this shows usage

            # Validate the parsed record
            is_valid, error_msg = validate_record(parsed_record)
            if is_valid:
                parsed_data.append(parsed_record)
            else:
                logger.warning(f"Skipping invalid record #{i+1}: {error_msg}. Original: {raw_record}")
                validation_errors += 1
                skipped_records += 1

        except KeyError as e:
            logger.warning(f"Skipping record #{i+1} due to missing key: {e}. Original: {raw_record}")
            skipped_records += 1
        except ValueError as e:
            logger.warning(f"Skipping record #{i+1} due to parsing/conversion error: {e}. Original: {raw_record}")
            skipped_records += 1
        except Exception as e:
            logger.error(f"Unexpected error parsing record #{i+1}: {e}. Original: {raw_record}", exc_info=True)
            skipped_records += 1
    
    logger.info(f"Successfully parsed {len(parsed_data)} records.")
    logger.info(f"Skipped {skipped_records} records ({validation_errors} due to validation failures). ")
    return parsed_data

class DataParser:
    def __init__(self):
        self.logger = setup_logger(f"{__name__}.DataParser")

    def parse(self, data_source: str) -> List[Dict[str, Any]]:
        self.logger.info(f"Initiating parsing process for source: {data_source}")
        loader = DataLoader(data_source)
        raw_data = loader.load()
        
        # Add example modification based on source (could be more complex)
        if data_source == "legacy_system":
            self.logger.info("Applying legacy data transformations...")
            # Hypothetical: maybe legacy system used different column names
            transformed_raw_data = []
            for rec in raw_data:
                 new_rec = {
                     'id': rec.get('legacyId', rec.get('id')),
                     'name': rec.get('itemName', rec.get('name')),
                     'value': rec.get('itemValue', rec.get('value')),
                     'category': rec.get('itemCat', rec.get('category', 'Unknown')),
                     'timestamp': rec.get('creationDate', rec.get('timestamp'))
                 }
                 transformed_raw_data.append({k: v for k, v in new_rec.items() if v is not None}) # Keep only non-null
            raw_data = transformed_raw_data

        parsed_data = parse_raw_data(raw_data)
        self.logger.info("Parsing process completed.")
        return parsed_data 