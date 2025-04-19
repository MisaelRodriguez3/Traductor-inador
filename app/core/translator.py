from app.services.translation_api import TranslationService
from .constants import Motor
from .docx_processor import DocxProcessor

class TranslationManager:
    def __init__(self, motor: Motor = Motor.MY_MEMORY):
        self.service = TranslationService(motor)
        self.chunk_size = 200  if motor == Motor.MY_MEMORY else 5000
        
    def translate_text(self, text, lang_from, lang_to):
        return self.service.translate(text, lang_from, lang_to)
        
    def translate_document(self, input_path, output_path, lang_from, lang_to, progress_callback=None):
        processor = DocxProcessor(self.service, chunk_size=self.chunk_size)
        processor.process_document(input_path, output_path, lang_from, lang_to, progress_callback)