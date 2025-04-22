import requests
from requests.exceptions import RequestException
from app.core.config import Config
from app.core.constants import Motor
from app.exceptions.translation import (
    TranslationError,
    TranslationServiceUnavailable,
    TranslationFailed,
)

class TranslationService:
    def __init__(self, motor: Motor = Motor.MY_MEMORY) -> None:
        self.motor = motor

    def translate(self, text: str, lang_from: str, lang_to: str) -> str:
        try:
            match self.motor:
                case Motor.MY_MEMORY:
                    return self._from_my_memory(text, lang_from, lang_to)
                case Motor.MAGIC_LOOPS:
                    return self._from_magic_loops(text, lang_from, lang_to)
                case Motor.GOOGLE:
                    return self._from_google_translate(text, lang_from, lang_to)
                case Motor.DEEPL:
                    return self._from_deepl(text, lang_from, lang_to)
                case _:
                    raise TranslationError("Motor no soportado.")
                
        except requests.Timeout:
            raise TimeoutError()
        except RequestException:
            raise TranslationServiceUnavailable("Error en la solicitud.")
        except (KeyError, ValueError):
            raise TranslationFailed("Error procesando respuesta.")

    def _from_my_memory(self, text: str, lang_from: str, lang_to: str) -> str:
        url = f"https://api.mymemory.translated.net/get?q={text}&langpair={lang_from}|{lang_to}"
        response = requests.get(url, timeout=10)
        data: dict = response.json()

        if data.get("responseStatus") != 200:
            raise TranslationFailed(data.get("responseDetails", "Error desconocido en MyMemory."))

        return data["responseData"]["translatedText"]

    def _from_magic_loops(self, text: str, lang_from: str, lang_to: str) -> str:
        url = Config.get_api_url(self.motor)
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
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            "q": text,
            "source": lang_from,
            "target": lang_to,
            "format": "text",
            "key": Config.get_api_url(self.motor),
        }

        response = requests.post(url, params=params, timeout=10)
        data = response.json()

        if "data" in data and "translations" in data["data"]:
            return data["data"]["translations"][0]["translatedText"]

        raise TranslationFailed("Error en respuesta de Google Translate.")

    def _from_deepl(self, text: str, lang_from: str, lang_to: str) -> str:
        url = "https://api-free.deepl.com/v2/translate"
        params = {
            "auth_key": Config.get_api_url(self.motor),
            "text": text,
            "source_lang": lang_from.upper(),
            "target_lang": lang_to.upper(),
        }

        response = requests.post(url, data=params, timeout=10)
        data = response.json()

        if "translations" in data:
            return data["translations"][0]["text"]

        raise TranslationFailed("Error en respuesta de DeepL.")