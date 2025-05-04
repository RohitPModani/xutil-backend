from ...schemas.text_utilities.slug_converter_schema import SlugGenerateRequest, SlugGenerateResponse, Separator, Case
import re

def generate_slug_logic(text: str, separator: str, case: str) -> str:
    """
    Generate a URL-friendly slug from input text.
    
    Args:
        text: Input text to convert
        separator: Separator to use (-, _, .)
        case: Case for the slug (lowercase, uppercase)
    
    Returns:
        A URL-friendly slug
    """
    # Convert to lowercase or uppercase based on case
    text = text.lower() if case == Case.LOWERCASE else text.upper()
    
    # Replace special characters (except separator and spaces) with nothing
    # Escape the separator for regex if it's a dot
    safe_separator = re.escape(separator)
    text = re.sub(rf'[^{safe_separator}a-zA-Z0-9\s]', '', text)  # Keep alphanumeric, spaces, and separator
    
    # Replace spaces with separator
    text = re.sub(r'\s+', separator, text.strip())
    
    # Remove consecutive separators
    text = re.sub(f'{safe_separator}+', separator, text)
    
    # Remove leading/trailing separator
    text = text.strip(separator)
    
    return text