from docx import Document
from typing import Optional, Callable
from .watermark import add_watermark

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
        """Procesa un documento DOCX completo con traducción y marca de agua."""
        doc = Document(input_path)
        
        all_paragraphs = self._extract_all_paragraphs(doc)
        total_paragraphs = len(all_paragraphs)
        
        for idx, paragraph in enumerate(all_paragraphs, 1):
            self._translate_paragraph(paragraph, lang_from, lang_to)
            self._update_progress(progress_callback, idx, total_paragraphs)
        
        add_watermark(doc, "DOCX Translator")
        doc.save(output_path)

    def _extract_all_paragraphs(self, doc: Document) -> list:
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

        original_runs = paragraph.runs
        combined_text = self._combine_runs_text(original_runs)
        translated_text = self._translate_text(combined_text, lang_from, lang_to)
        
        self._update_paragraph_runs(original_runs, translated_text)

    def _combine_runs_text(self, runs) -> str:
        """Combina el texto de todos los runs del párrafo."""
        return ''.join(run.text for run in runs)

    def _translate_text(self, text: str, lang_from: str, lang_to: str) -> str:
        """Traduce texto en chunks manejables."""
        if not text.strip():
            return text

        chunks = self._split_into_chunks(text)
        return ''.join(self.translator.translate(chunk, lang_from, lang_to) for chunk in chunks)

    def _split_into_chunks(self, text: str) -> list[str]:
        """Divide el texto en chunks del tamaño especificado."""
        return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]

    def _update_paragraph_runs(self, original_runs, translated_text: str) -> None:
        """Actualiza los runs del párrafo con el texto traducido."""
        if not translated_text:
            return

        chunks = self._calculate_run_chunks(len(original_runs), len(translated_text))
        current_position = 0
        
        for run, chunk_size in zip(original_runs, chunks):
            run.text = translated_text[current_position:current_position + chunk_size]
            current_position += chunk_size

    def _calculate_run_chunks(self, num_runs: int, text_length: int) -> list[int]:
        """Calcula la distribución de caracteres por run."""
        chunk_size, remainder = divmod(text_length, num_runs)
        return [chunk_size + 1 if i < remainder else chunk_size for i in range(num_runs)]

    def _update_progress(
        self,
        callback: Optional[Callable[[int, int], None]],
        processed: int,
        total: int
    ) -> None:
        """Actualiza el progreso si hay un callback registrado."""
        if callback:
            callback(processed, total)