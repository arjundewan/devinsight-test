import re

def sanitize_string(text: str) -> str:
    """Removes non-alphanumeric characters from a string."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).strip()

def capitalize_words(text: str) -> str:
    """Capitalizes the first letter of each word in a string."""
    return ' '.join(word.capitalize() for word in text.split())

def reverse_string(text: str) -> str:
    """Reverses a string."""
    return text[::-1]

def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """Truncates a string if it exceeds the maximum length."""
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - len(suffix)] + suffix

def is_palindrome(text: str, case_sensitive: bool = False) -> bool:
    """Checks if a string is a palindrome (reads the same forwards and backwards)."""
    processed_text = sanitize_string(text) # Use existing util
    if not case_sensitive:
        processed_text = processed_text.lower()
    
    if not processed_text: # Empty or only symbols
        return False 
        
    return processed_text == processed_text[::-1]

def count_substring(text: str, sub: str) -> int:
    """Counts non-overlapping occurrences of a substring."""
    if not sub:
        return 0
    return text.count(sub)

def extract_emails(text: str) -> list[str]:
    """Extracts potential email addresses from a string using a simple regex."""
    # Basic regex, not fully RFC compliant but good for common cases
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_regex, text)

def snake_to_camel(snake_str: str) -> str:
    """Converts snake_case string to camelCase."""
    components = snake_str.split('_')
    # Capitalize the first letter of each component except the first one
    # and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])

def camel_to_snake(camel_str: str) -> str:
    """Converts camelCase string to snake_case."""
    # Add underscore before uppercase letters (if not first char) and convert to lower
    snake_str = re.sub('(?<!^)(?=[A-Z])', '_', camel_str).lower()
    return snake_str 