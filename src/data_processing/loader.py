import csv
import io
from typing import List, Dict

from src.utils.helpers import setup_logger

logger = setup_logger(__name__)

def load_dummy_data() -> List[Dict[str, str]]:
    """Loads sample data from a hardcoded CSV string."""
    logger.info("Loading dummy data.")
    # Simulate reading from a file
    csv_data = "id,name,value\n1,Apple,10\n2,Banana,20\n3,Cherry,30\n4,Date Fruit,40"
    
    data = []
    try:
        # Use io.StringIO to treat the string as a file
        f = io.StringIO(csv_data)
        reader = csv.DictReader(f)
        data = list(reader)
        logger.info(f"Successfully loaded {len(data)} records.")
    except Exception as e:
        logger.error(f"Failed to load dummy data: {e}")
        raise
    return data

class DataLoader:
    def __init__(self, source: str):
        self.source = source
        self.logger = setup_logger(f"{__name__}.DataLoader")

    def load(self) -> List[Dict[str, str]]:
        self.logger.info(f"Loading data from {self.source}")
        if self.source == "dummy":
            return load_dummy_data()
        else:
            self.logger.warning(f"Source '{self.source}' not implemented, returning empty list.")
            return [] 