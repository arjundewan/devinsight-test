from typing import List, Dict, Any

from src.utils.helpers import get_current_timestamp, setup_logger, format_data, generate_report_summary
from src.data_processing.parser import DataParser
from src.calculations.core import (
    calculate_total_value, 
    calculate_weighted_average, 
    calculate_value_statistics, 
    find_most_common_categories,
    AdvancedCalculator
)

logger = setup_logger(__name__)

def format_statistics(stats: Dict[str, float]) -> str:
    """Formats the statistics dictionary into a readable string."""
    if stats['count'] == 0:
        return "  N/A (No valid data)"
    lines = [
        f"    Count:   {stats['count']}",
        f"    Min:     {stats['min']:.2f}",
        f"    Max:     {stats['max']:.2f}",
        f"    Mean:    {stats['mean']:.2f}",
        f"    Std Dev: {stats['std_dev']:.2f}"
    ]
    return "\n".join(lines)
    
def format_common_categories(categories: List[tuple]) -> str:
    """Formats the list of common categories."""
    if not categories:
        return "  N/A"
    lines = [f"    - {cat} ({count})" for cat, count in categories]
    return "\n".join(lines)

class ReportGenerator:
    def __init__(self, data_source: str = "dummy", report_config: Dict = None):
        self.data_source = data_source
        self.parser = DataParser()
        # Example: Configure calculator based on external config
        default_config = {'calculator_exponent': 1.5, 'top_n_categories': 3}
        if report_config:
            default_config.update(report_config)
            
        self.calculator = AdvancedCalculator(exponent=default_config['calculator_exponent'])
        self.top_n = default_config['top_n_categories']
        self.logger = setup_logger(f"{__name__}.ReportGenerator")
        self.logger.info(f"ReportGenerator initialized with config: {default_config}")

    def generate_summary_report(self) -> str:
        self.logger.info(f"Generating summary report for data source: {self.data_source}")
        
        report_data = {}
        notes_list = []

        try:
            # 1. Parse data
            parsed_data = self.parser.parse(self.data_source)
            report_data['processed_records'] = len(parsed_data)
            if not parsed_data:
                self.logger.warning("No data parsed, cannot generate full report.")
                notes_list.append("No data available for analysis.")
                # Use the generate_report_summary helper for a minimal report
                return generate_report_summary(
                    title="Data Analysis Summary Report", 
                    data_points={'Status': 'Failed - No Data', 'Source': self.data_source},
                    notes="\n".join(notes_list)
                )

            # 2. Perform calculations
            report_data['total_value'] = f"{calculate_total_value(parsed_data):.2f}"
            report_data['weighted_average_by_id'] = f"{calculate_weighted_average(parsed_data, weight_key='id'):.2f}"
            
            # Calculate statistics
            value_stats = calculate_value_statistics(parsed_data, value_key='value')
            report_data['value_statistics'] = format_statistics(value_stats)
            
            # Find common categories
            common_categories = find_most_common_categories(parsed_data, category_key='category', top_n=self.top_n)
            report_data['most_common_categories'] = format_common_categories(common_categories)
            
            # Perform transformation (optional, maybe based on config)
            # transformed_data = self.calculator.transform_values(parsed_data)
            # report_data['sample_transformed_record'] = format_data(transformed_data[0]) if transformed_data else 'N/A'

            # 3. Generate formatted report using helper
            report_title = "Data Analysis Summary Report"
            final_report = generate_report_summary(
                title=report_title,
                data_points=report_data,
                notes="\n".join(notes_list)
            )
            
            # Log success and return
            self.logger.info("Summary report generated successfully.")
            return final_report

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}", exc_info=True)
            # Generate a failure report using the helper
            return generate_report_summary(
                title="Data Analysis Summary Report",
                data_points={'Status': 'Failed - Error', 'Source': self.data_source},
                notes=f"An error occurred during report generation: {e}"
            ) 