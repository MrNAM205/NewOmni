from dateutil.parser import parse
import re

def normalize_date(date_str: str) -> str | None:
    """
    Parses a date string and returns it in YYYY-MM-DD format.
    Returns None if parsing fails.
    """
    if not date_str:
        return None
    try:
        # The parser can be quite slow, so we can add some fast-path regex checks
        # for common formats if performance becomes an issue.
        dt = parse(date_str)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def normalize_amount(amount_str: str) -> float | None:
    """
    Converts a string amount (e.g., '1,234.56') to a float.
    Returns None if conversion fails.
    """
    if not amount_str:
        return None
    try:
        # Remove commas and convert to float
        return float(re.sub(r'[,\s]', '', amount_str))
    except (ValueError, TypeError):
        return None
