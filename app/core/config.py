from PyQt6.QtCore import QSettings

class Config:
    _settings: QSettings = QSettings("Mictla Projects",'Traductor-inador')

    @classmethod
    def get(cls, key, default=None) -> str | None:
        return cls._settings.value(key, default)

    @classmethod
    def set(cls, key, value) -> None:
        if not value:
            cls.delete(key)
        else:   
            cls._settings.setValue(key, value)

    @classmethod
    def delete(cls, key) -> None:
        cls._settings.remove(key)

    @classmethod
    def get_api_url(cls, motor: str) -> str | None:
        key_map = {
            "deepl": "deepl_api",
            "google": "google_api",
            "magic_loops": "magic_loops_api"
        }
        return cls.get(key_map.get(motor, ""))