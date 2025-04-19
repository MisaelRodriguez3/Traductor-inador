from enum import StrEnum

class Motor(StrEnum):
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