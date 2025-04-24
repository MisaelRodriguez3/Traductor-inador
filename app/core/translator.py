from typing import Callable
from app.services.translation_api import TranslationService
from .constants import Engine
from .docx_processor import DocxProcessor

class TranslationManager:
    """Orchestrates text and document translation operations.
    
    Provides a unified interface for both simple text translations and complex
    document processing with format preservation.

    Attributes:
        service (TranslationService): Configured translation service instance
        chunk_size (int): Optimal text chunk size for the selected engine

    Example:
        >>> manager = TranslationManager(Engine.DEEPL)
        >>> text = manager.translate_text("Hello", "en", "es")
        >>> manager.translate_document("doc.docx", "translated.docx", "en", "es")
    """

    def __init__(self, engine: Engine = Engine.MY_MEMORY):
        """Initializes translation manager with specified engine.
        
        Args:
            engine (Engine): Translation service to use. Defaults to MyMemory.
        
        Note:
            Automatically sets optimal chunk sizes:
            - 200 chars for MyMemory (API limits)
            - 5000 chars for other services
        """
        self.service = TranslationService(engine)
        self.chunk_size = 200 if engine == Engine.MY_MEMORY else 5000
        
    def translate_text(self, text: str, lang_from: str, lang_to: str) -> str:
        """Translates a text string using the configured service.
        
        Args:
            text (str): Input text to translate
            lang_from (str): Source language code
            lang_to (str): Target language code

        Returns:
            str: Translated text as string

        Raises:
            TranslationServiceUnavailable: Service connection issues
            TranslationFailed: Invalid translation response
        """
        return self.service.translate(text, lang_from, lang_to)
        
    def translate_document(
        self, 
        input_path: str, 
        output_path: str, 
        lang_from: str, 
        lang_to: str, 
        progress_callback: Callable[[int, int], None] | None = None
    ) -> None:
        """Processes and translates a DOCX document.
        
        Args:
            input_path (str): Source document path
            output_path (str): Destination document path
            lang_from (str): Source language code
            lang_to (str): Target language code
            progress_callback (Callable[[int, int], None], optional): Optional progress reporting function
                Parameters: (processed_paragraphs, total_paragraphs)

        Raises:
            DocumentNotFound: Missing input file
            DocumentReadError: Document parsing failure
            DocumentWriteError: Output file creation failure
            ParagraphTranslationError: Translation error in content
        """
        processor = DocxProcessor(self.service, chunk_size=self.chunk_size)
        processor.process_document(input_path, output_path, lang_from, lang_to, progress_callback)