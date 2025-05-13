import datetime
import logging

def get_current_timestamp() -> str:
    """Returns the current timestamp as a string."""
    return datetime.datetime.now().isoformat()

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """Sets up a basic logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger

def format_data(data: dict) -> str:
    """A simple function to format dictionary data for display."""
    items = [f"  {k}: {v}" for k, v in data.items()]
    return "{\n" + "\n".join(items) + "\n}"

def deprecated_function_example():
    """This is an example of a deprecated function."""
    # In a real scenario, you would use the @deprecated decorator or similar
    # from a library like 'deprecated' or 'deprecation'.
    # For this example, we'll just print a warning.
    import warnings
    warnings.warn(
        "deprecated_function_example is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2
    )
    # Simulate some old logic
    return "This function is old."

class ConfigManager:
    """A simple class to manage configuration settings from a dictionary."""
    def __init__(self, config_dict: dict):
        self._config = config_dict
        self.logger = setup_logger(f"{__name__}.ConfigManager")
        self.logger.info("ConfigManager initialized.")

    def get_setting(self, key: str, default=None):
        """Retrieves a setting by key."""
        self.logger.debug(f"Attempting to retrieve setting: {key}")
        value = self._config.get(key, default)
        if value is default and default is not None:
            self.logger.warning(f"Setting '{key}' not found, using default value: {default}")
        elif value is None and default is None:
            self.logger.warning(f"Setting '{key}' not found and no default was provided.")
        return value

    def set_setting(self, key: str, value):
        """Sets a configuration value."""
        self.logger.debug(f"Setting '{key}' to '{value}'")
        self._config[key] = value

    def list_settings(self):
        """Lists all current settings."""
        self.logger.debug("Listing all settings.")
        return list(self._config.keys())

    def __repr__(self):
        return f"<ConfigManager settings_count={len(self._config)}>"

def complex_data_transformation(input_list: list) -> list:
    """
    An example of a more complex data transformation.
    - Filters out non-numeric types.
    - Squares numbers.
    - Converts to string and prefixes with 'ID_'.
    """
    processed_list = []
    for item in input_list:
        if isinstance(item, (int, float)):
            squared = item * item
            processed_list.append(f"ID_{str(squared)}")
        # Silently ignore other types for this example
    return processed_list

def generate_report_summary(title: str, data_points: dict, notes: str = "") -> str:
    """Generates a formatted string summary."""
    summary = f"--- {title.upper()} ---\n"
    summary += f"Timestamp: {get_current_timestamp()}\n\n"
    for key, value in data_points.items():
        summary += f"- {key.replace('_', ' ').capitalize()}: {value}\n"
    if notes:
        summary += f"\nNotes:\n{notes}\n"
    summary += "--- END OF SUMMARY ---"
    return summary 