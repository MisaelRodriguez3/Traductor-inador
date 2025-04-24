def is_not_empty(text: str) -> bool:
    """Check if a string contains meaningful content after whitespace removal.
    
    Determines if the input string is non-empty when leading/trailing whitespace
    is removed. Useful for validating user input where whitespace-only entries
    should be considered empty.

    Args:
        text (str): Input string to validate. Accepts any string including empty strings.

    Returns:
        bool: True if the stripped text has length > 0, False otherwise.

    Examples:
        >>> is_not_empty("  Hello  ")
        True
        >>> is_not_empty("   ")
        False
        >>> is_not_empty("")
        False
        >>> is_not_empty("Important data")
        True

    Note:
        Equivalent to `bool(text.strip())` but more readable and intentional
        in contexts requiring validation of meaningful content
    """
    return bool(text.strip())

#Combinar con pydantic para hacer validaciones mas complejas (futura mejora)