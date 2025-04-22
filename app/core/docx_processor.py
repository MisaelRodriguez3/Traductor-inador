from typing import Optional, Callable
from docx import Document
from app.utils.error_handler import handle_error
from app.exceptions.document import (
    DocumentNotFound,
    DocumentReadError,
    DocumentWriteError,
    ParagraphTranslationError,
)

class DocxProcessor:
    def __init__(self, translator, chunk_size: int = 200):
        self.translator = translator
        self.chunk_size = chunk_size

    def process_document(
        self,
        input_path: str,
        output_path: str,
        lang_from: str,
        lang_to: str,
        progress_callback: Callable[[int, int], None] | None = None
    ) -> None:
        """Procesa un documento DOCX completo con traducción."""
        try:
            doc = Document(input_path)
        except FileNotFoundError:
            raise DocumentNotFound(f"No se encontró el archivo: {input_path}")
        except Exception as e:
            raise DocumentReadError(f"No se pudo leer el documento: {e}")
        
        all_paragraphs = self._extract_all_paragraphs(doc)
        total_paragraphs = len(all_paragraphs)
        
        for idx, paragraph in enumerate(all_paragraphs, 1):
            try:
                self._translate_paragraph(paragraph, lang_from, lang_to)
            except Exception as e:
                raise ParagraphTranslationError(f"Error en el párrafo {idx}: {e}")
            self._update_progress(progress_callback, idx, total_paragraphs)
        try:
            doc.save(output_path)
        except Exception as e:
            raise DocumentWriteError(f"No se pudo guardar el archivo: {e}")


    def _extract_all_paragraphs(self, doc) -> list:
        """Extrae todos los párrafos del documento, incluyendo los de las tablas."""
        main_paragraphs = list(doc.paragraphs)
        table_paragraphs = [
            para
            for table in doc.tables
            for row in table.rows
            for cell in row.cells
            for para in cell.paragraphs
        ]
        return main_paragraphs + table_paragraphs

    def _translate_paragraph(self, paragraph, lang_from: str, lang_to: str) -> None:
        """Traduce un párrafo manteniendo el formato original."""
        if not paragraph.text.strip():
            return

        for run in paragraph.runs:
            original_text = run.text
            if not original_text.strip():
                continue

            chunks = self._split_into_chunks(original_text, self.chunk_size)
            translated_chunks = []

            for chunk in chunks:
                translated_chunk = self.translator.translate(chunk, lang_from, lang_to)
                translated_chunks.append(translated_chunk)

            run.text = ''.join(translated_chunks)

    def _split_into_chunks(self, text: str, max_chunk_size: int) -> list[str]:
        """Divide el texto en chunks del tamaño especificado, evitando cortar palabras."""
        chunks = []
        words = text.split(' ')
        current_chunk = ""

        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_chunk_size:
                current_chunk += word + ' '
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + ' '

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _update_progress(
        self,
        callback: Optional[Callable[[int, int], None]],
        processed: int,
        total: int
    ) -> None:
        """Actualiza el progreso si hay un callback registrado."""
        if callback:
            callback(processed, total)