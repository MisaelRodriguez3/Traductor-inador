class AuthorizationError(Exception):
    """Error base para errores de autorización"""

class Unauthorized(AuthorizationError):
    """Sin claves de api válidas"""