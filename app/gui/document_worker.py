from PyQt6.QtCore import pyqtSignal, QObject
from app.core.translator import TranslationManager

class DocumentWorker(QObject):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal(str)
    error_occurred = pyqtSignal(Exception)

    def __init__(self, input_path, output_path,lang_from, lang_to, translation_manager: TranslationManager):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.tm = translation_manager

    def process(self):
        try:
            self.tm.translate_document(
                input_path=self.input_path,
                output_path=self.output_path,
                lang_from=self.lang_from,
                lang_to=self.lang_to,
                progress_callback=lambda p, t: self.progress_updated.emit(int((p/t)*100))
            )
            
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error_occurred.emit(e)