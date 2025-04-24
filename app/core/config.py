from PyQt6.QtCore import QSettings

class Config:
    """Manages application configuration using QSettings for persistent storage.
    
    Provides a centralized interface for storing/retrieving settings across sessions.
    Uses platform-appropriate storage locations handled by Qt.

    Attributes:
        _settings (QSettings): QSettings instance initialized with organization/app names
    """
    _settings: QSettings = QSettings("Mictla Projects", 'Traductor-inador')

    @classmethod
    def get(cls, key: str, default: str | None = None) -> str | None:
        """Retrieves a configuration value by key.
        
        Args:
            key (str): Setting name to retrieve
            default (str, optional): Fallback value if key doesn't exist

        Returns:
            (str, optional): Stored value as string, or default if not found

        Example:
            >>> Config.get('last_used_language', 'en')
            'es'
        """
        return cls._settings.value(key, default)

    @classmethod
    def set(cls, key: str, value: str , optional) -> None:
        """Stores or updates a configuration value.
        
        Args:
            key (str): Setting name to update
            value (str): Value to store. Deletes key if None or empty

        Example:
            >>> Config.set('max_threads', '4')
        """
        if not value:
            cls.delete(key)
        else:   
            cls._settings.setValue(key, value)

    @classmethod
    def delete(cls, key: str) -> None:
        """Removes a configuration entry.
        
        Args:
            key (str): Setting name to remove

        Example:
            >>> Config.delete('temp_api_key')
        """
        cls._settings.remove(key)

    @classmethod
    def get_api_url(cls, engine: str) -> str | None:
        """Gets API key for specified translation engine.
        
        Args:
            engine (str): Translation service identifier. Supported values:
                - 'deepl': DeepL API key
                - 'google': Google Cloud API key 
                - 'magic_loops': Custom service endpoint

        Returns:
            (str, optional): Stored API key/URL or None if not configured

        Example:
            >>> Config.get_api_url('deepl')
            'your_api_key_here'

        Note:
            Key mapping can be extended for new services
        """
        key_map = {
            "deepl": "deepl_api",
            "google": "google_api",
            "magic_loops": "magic_loops_api"
        }
        return cls.get(key_map.get(engine, ""))