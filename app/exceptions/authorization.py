class AuthorizationError(Exception):
    """Base exception for authorization-related errors in the application.
    
    This exception serves as the parent class for all authorization-related errors.
    Should be subclassed to create specific authorization failure exceptions.
    
    Attributes:
        message: Explanation of the error (inherited from Exception)
    
    Example:
        >>> raise AuthorizationError("Generic auth error")
        AuthorizationError: Generic auth error
    """

class Unauthorized(AuthorizationError):
    """Exception raised when API authentication credentials are invalid or missing.
    
    This exception should be raised when:
    - API keys are not configured
    - Provided credentials are expired
    - Authentication tokens are invalid
    
    Attributes:
        message (str): Human-readable description of the authorization failure
    
    Example:
        >>> raise Unauthorized("No valid API keys found in configuration")
        Unauthorized: No valid API keys found in configuration
    
    Note:
        Inherits from AuthorizationError to allow grouped exception handling
        of all authorization-related issues
    """