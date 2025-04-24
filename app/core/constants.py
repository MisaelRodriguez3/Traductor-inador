from enum import StrEnum

class Engine(StrEnum):
    """Represents available translation engines as string enumeration.
    
    Provides validated engine identifiers for translation service selection.
    Enum values match configuration keys and internal service references.

    Members:
        MY_MEMORY: MyMemory Translation service
        MAGIC_LOOPS: Custom Magic Loops API
        DEEPL: DeepL API service
        GOOGLE: Google Cloud Translation API

    Example:
        >>> Engine.DEEPL
        <Engine.DEEPL: 'deepl'>
        >>> Engine('google')
        <Engine.GOOGLE: 'google'>
    """
    MY_MEMORY = "my_memory"
    MAGIC_LOOPS = "magic_loops"
    DEEPL = "deepl"
    GOOGLE = "google"

LANGUAGES = {
    "Español": "es",
    "Inglés": "en", 
    "Italiano": "it",
    "Francés": "fr",
    "Alemán": "de",
    "Portugués": "pt",
    "Japonés": "ja",
}
"""Mapping of display names to language codes for UI and translations.

Contains language names in Spanish (keys) with corresponding ISO 639-1 codes (values).
Should be used for user-facing language selection while internal systems use codes.

Example:
    >>> LANGUAGES["Español"]
    'es'
    >>> list(LANGUAGES.keys())
    ['Español', 'Inglés', 'Italiano', ...]

Note:
    Can be extended with additional languages following the same pattern:
    {"Display Name": "iso-code"}
"""