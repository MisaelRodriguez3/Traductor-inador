class TranslationError(Exception):
    """Base exception for all translation-related errors.
    
    This exception serves as the parent class for translation failures.
    Should be subclassed to create specific translation error types.
    
    Attributes:
        message (str): Explanation of the error (inherited from Exception)
    
    Example:
        >>> raise TranslationError("Generic translation failure")
        TranslationError: Generic translation failure
    """

class TranslationServiceUnavailable(TranslationError):
    """Exception raised when external translation service is unreachable.
    
    Common scenarios:
    - Network connectivity issues
    - Service downtime
    - API rate limits exceeded
    - Invalid service endpoint
    
    Attributes:
        message (str): Human-readable description with path details
    
    Example:
        >>> raise TranslationServiceUnavailable("DeepL API timeout")
        TranslationServiceUnavailable: DeepL API timeout
    
    Note:
        Typically indicates temporary issues that may resolve with retries
    """
    def __init__(self, message: str = "Translation service unavailable"):
        super().__init__(message)

class TranslationFailed(TranslationError):
    """Exception raised when translation process returns invalid results.
    
    Common causes:
    - Malformed API response
    - Unsupported language pair
    - Content parsing errors
    - Invalid response formatting
        
    Attributes:
        message (str): Human-readable description with path details
    
    Example:
        >>> raise TranslationFailed("Missing 'translations' in API response")
        TranslationFailed: Missing 'translations' in API response
    
    Note:
        Often indicates permanent issues requiring code/data changes
    """
    def __init__(self, message: str = "Translation process failed"):
        super().__init__(message)