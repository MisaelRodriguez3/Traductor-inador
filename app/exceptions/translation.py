class TranslationError(Exception):
    """Error base para traducciones."""


class TranslationServiceUnavailable(TranslationError):
    """Error si el servicio externo no responde o no está disponible."""


class TranslationFailed(TranslationError):
    """Error si la traducción falla o la respuesta no es válida."""
