import sys
import logging

# Add src directory to Python path
# This is sometimes needed for imports to work correctly when running main.py directly
# Note: Better practice often involves proper packaging or using `python -m src.main`
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.reporting.generator import ReportGenerator
from src.utils.helpers import setup_logger

# Setup a main logger for the application entry point
logger = setup_logger("MainApp", level=logging.DEBUG) # Set to DEBUG to see all logs

def run_application():
    """Runs the main application logic."""
    logger.info("Application starting.")
    
    try:
        report_generator = ReportGenerator(data_source="dummy")
        summary_report = report_generator.generate_summary_report()
        
        print("\n--- Generated Report ---")
        print(summary_report)
        print("--- End of Report ---")
        
        logger.info("Application finished successfully.")
        
    except Exception as e:
        logger.critical(f"An unhandled error occurred in the main application: {e}", exc_info=True)
        sys.exit(1) # Exit with an error code

if __name__ == "__main__":
    run_application() 