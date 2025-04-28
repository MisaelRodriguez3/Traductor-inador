from PyQt6.QtCore import pyqtSignal, QObject
from app.core.translator import TranslationManager

class DocumentWorker(QObject):
    """Background worker for document translation tasks.
    
    Handles document processing in a separate thread and emits status signals.
    
    Signals:
        progress_updated (pyqtSignal): Emits translation progress percentage (0-100)
        finished (pyqtSignal): Emits output path when translation completes successfully
        error_occurred (pyqtSignal): Emits any exceptions during processing
    
    Args:
        input_path (str): Source document file path
        output_path (str): Target document save path
        lang_from (str): Source language code (ISO 639-1)
        lang_to (str): Target language code (ISO 639-1)
        translation_manager (TranslationManager): Configured TranslationManager instance
        skip_pages (set[int]): Set of pages to ignore in translation
    
    Example:
        >>> worker = DocumentWorker(
        ...     "input.docx",
        ...     "output.docx",
        ...     "es",
        ...     "en",
        ...     TranslationManager()
        ... )
        >>> worker.progress_updated.connect(handle_progress)
    """
    
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(str)
    error_occurred = pyqtSignal(Exception)

    def __init__(
        self,
        input_path: str,
        output_path: str,
        lang_from: str,
        lang_to: str,
        translation_manager: TranslationManager,
        skip_pages: set[int]
    ):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.tm = translation_manager
        self.skip_pages = skip_pages

    def process(self) -> None:
        """Executes the document translation process.
        
        Performs:
        1. Document loading and parsing
        2. Paragraph-by-paragraph translation
        3. Translated document saving
        
        Emits:
            progress_updated: During paragraph processing
            finished: On successful completion
            error_occurred: For any processing exceptions
            
        Note:
            Runs in a background thread - no direct UI operations
        """
        try:
            self.tm.translate_document(
                input_path=self.input_path,
                output_path=self.output_path,
                lang_from=self.lang_from,
                lang_to=self.lang_to,
                progress_callback=lambda p, t: self.progress_updated.emit(int((p/t)*100)),
                skip_pages=self.skip_pages
            )
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error_occurred.emit(e)