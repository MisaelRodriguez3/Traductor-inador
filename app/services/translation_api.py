import requests
from requests.exceptions import RequestException
from app.core.config import Config
from app.core.constants import Engine
from app.exceptions.translation import (
    TranslationError,
    TranslationServiceUnavailable,
    TranslationFailed,
)

class TranslationService:
    """Text translation service using different translation engines.
    
    Supports multiple providers through dynamic configuration.
    
    Attributes:
        engine (Engine): Translation engine to use (MY_MEMORY|MAGIC_LOOPS|GOOGLE|DEEPL)
    
    Example:
        >>> service = TranslationService(Engine.GOOGLE)
        >>> translated = service.translate("Hello", "en", "es")
    """

    def __init__(self, engine: Engine = Engine.MY_MEMORY) -> None:
        """Initializes the service with specified translation engine.

        Args:
            engine (Engine, optional):Translation engine to use. Defaults to Engine.MY_MEMORY.
        """
        self.engine = engine

    def translate(self, text: str, lang_from: str, lang_to: str) -> str:
        """Translates text using the configured engine.

        Args:
            text (str): Text to translate
            lang_from (str): Source language code (e.g., 'en')
            lang_to (str): Target language code (e.g., 'es')

        Raises:
            TranslationError: If the engine is not supported.
            TimeoutError: If the request exceeds the timeout.
            TranslationServiceUnavailable: If an error occurred in the request.
            TranslationFailed: If there was an error processing the response.

        Returns:
            str: Translated text
        """
        try:
            match self.engine:
                case Engine.MY_MEMORY:
                    return self._from_my_memory(text, lang_from, lang_to)
                case Engine.MAGIC_LOOPS:
                    return self._from_magic_loops(text, lang_from, lang_to)
                case Engine.GOOGLE:
                    return self._from_google_translate(text, lang_from, lang_to)
                case Engine.DEEPL:
                    return self._from_deepl(text, lang_from, lang_to)
                case _:
                    raise TranslationError("Engine no soportado.")
                
        except requests.Timeout:
            raise TimeoutError()
        except RequestException:
            raise TranslationServiceUnavailable("Error en la solicitud.")
        except (KeyError, ValueError):
            raise TranslationFailed("Error procesando respuesta.")

    def _from_my_memory(self, text: str, lang_from: str, lang_to: str) -> str:
        """Translates text using MyMemory Translation API.
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language
            target_lang (str): Target language
        
        Raises:
            TranslationFailed: If API returns non-200 status

        Returns:
            str: Translated text
        """
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={lang_from}|{lang_to}"
        response = requests.get(url, timeout=10)
        data: dict = response.json()

        if data.get("responseStatus") != 200:
            raise TranslationFailed(data.get("responseDetails", "Error desconocido en MyMemory."))

        return data["responseData"]["translatedText"]

    def _from_magic_loops(self, text: str, lang_from: str, lang_to: str) -> str:
        """Translates text using Magic Loops custom API.
        
        Requires configured endpoint URL.
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language
            target_lang (str): Target language
            
        Raises:
            TranslationServiceUnavailable: Missing endpoint configuration
            TranslationFailed: Invalid response structure

        Returns:
            str: Translated text
        """
        url = Config.get_api_url(self.engine)
        if not url:
            raise TranslationServiceUnavailable("URL de Magic Loops no configurada.")

        response = requests.get(
            url,
            json={"text": text, "source": lang_from, "target": lang_to},
            timeout=10,
        )
        data: dict = response.json()

        response = data.get("translatedText")

        if not response:
            raise TranslationFailed("La respuesta no contiene 'translatedText'.")

        return response

    def _from_google_translate(self, text: str, lang_from: str, lang_to: str) -> str:
        """Translates text using Google Cloud Translation API.
        
        Requires valid API key configuration.
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language
            target_lang (str): Target language
            
        Raises:
            TranslationFailed: Invalid response structure
            
        Returns:
            str: Translated text
        """
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            "q": text,
            "source": lang_from,
            "target": lang_to,
            "format": "text",
            "key": Config.get_api_url(self.engine),
        }

        response = requests.post(url, params=params, timeout=10)
        data = response.json()

        if "data" in data and "translations" in data["data"]:
            return data["data"]["translations"][0]["translatedText"]

        raise TranslationFailed("Error en respuesta de Google Translate.")

    def _from_deepl(self, text: str, lang_from: str, lang_to: str) -> str:
        """Translates text using DeepL API.
        
        Requires valid API key configuration.
        
        Args:
            text (str): Text to translate
            source_lang (str): Source language
            target_lang (str): Target language
            
        Raises:
            TranslationFailed: No valid translations in response
            
        Returns:
            str: Translated text
        """
        url = "https://api-free.deepl.com/v2/translate"
        params = {
            "auth_key": Config.get_api_url(self.engine),
            "text": text,
            "source_lang": lang_from.upper(),
            "target_lang": lang_to.upper(),
        }

        response = requests.post(url, data=params, timeout=10)
        data = response.json()

        if "translations" in data:
            return data["translations"][0]["text"]

        raise TranslationFailed("Error en respuesta de DeepL.")