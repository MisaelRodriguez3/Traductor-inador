from typing import Callable
from docx import Document
from app.exceptions.document import (
    DocumentNotFound,
    DocumentReadError,
    DocumentWriteError,
    ParagraphTranslationError,
)

class DocxProcessor:
    """Processes DOCX documents while preserving formatting during translation.
    
    Handles document loading, text extraction, chunked translation, and saving,
    maintaining original document structure and formatting elements.

    Attributes:
        translator (TranslationService): Translation service adapter instance
        chunk_size (int, optional): Maximum character count per translation chunk (default: 200)

    Raises:
        DocumentNotFound: Input file not found
        DocumentReadError: Error reading document contents
        DocumentWriteError: Error saving translated document
        ParagraphTranslationError: Translation failure in specific paragraph
    """

    def __init__(self, translator, chunk_size: int = 200):
        """Initializes processor with translation service and chunk size.
        
        Args:
            translator (TranslationService): Translation service implementing translate() method
            chunk_size (int, optional): Maximum text chunk size for translation API calls
        """
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
        """Processes and translates entire DOCX document.
        
        Args:
            input_path (str): Source document file path
            output_path (str): Destination document file path
            lang_from (str): Source language code (ISO 639-1)
            lang_to (str): Target language code (ISO 639-1)
            progress_callback (Callable[[int, int], None], optional): Optional progress reporting function
                Args: (processed_count, total_count)

        Raises:
            DocumentNotFound: If input file doesn't exist
            DocumentReadError: If document loading fails
            DocumentWriteError: If document saving fails
            ParagraphTranslationError: If any paragraph translation fails
        """
        try:
            doc = Document(input_path)
        except FileNotFoundError:
            raise DocumentNotFound(f"File not found: {input_path}")
        except Exception as e:
            raise DocumentReadError(f"Document read error: {e}")
        
        all_paragraphs = self._extract_all_paragraphs(doc)
        total_paragraphs = len(all_paragraphs)
        
        for idx, paragraph in enumerate(all_paragraphs, 1):
            try:
                self._translate_paragraph(paragraph, lang_from, lang_to)
            except Exception as e:
                raise ParagraphTranslationError(f"Paragraph {idx} error: {e}")
            self._update_progress(progress_callback, idx, total_paragraphs)
            
        try:
            doc.save(output_path)
        except Exception as e:
            raise DocumentWriteError(f"Save failed: {e}")

    def _extract_all_paragraphs(self, doc) -> list:
        """Extracts all document paragraphs including table contents.
        
        Args:
            doc (Document): python-docx Document object
            
        Returns:
            List of all Paragraph objects in document
        """
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
        """Translates paragraph while preserving formatting runs.
        
        Args:
            paragraph (Paragraph): docx Paragraph object
            lang_from (str): Source language code
            lang_to (str): Target language code
        """
        if not paragraph.text.strip():
            return

        for run in paragraph.runs:
            original_text = run.text
            if not original_text.strip():
                continue

            chunks = self._split_into_chunks(original_text, self.chunk_size)
            translated_chunks = [
                self.translator.translate(chunk, lang_from, lang_to)
                for chunk in chunks
            ]
            run.text = ''.join(translated_chunks)

    def _split_into_chunks(self, text: str, max_chunk_size: int) -> list[str]:
        """Splits text into chunks respecting word boundaries.
        
        Args:
            text (str): Input text to split
            max_chunk_size (int): Maximum characters per chunk
            
        Returns:
            list[str]: List of text chunks guaranteed under size limit
        """
        chunks = []
        words = text.split(' ')
        current_chunk = ""

        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_chunk_size:
                current_chunk += f"{word} "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = f"{word} "

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _update_progress(
        self,
        callback: Callable[[int, int], None] | None,
        processed: int,
        total: int
    ) -> None:
        """Executes progress callback if provided.
        
        Args:
            callback (Callable[[int, int], None], optional): Optional progress reporting function
            processed (int): Number of processed items
            total (int): Total number of items
        """
        if callback:
            callback(processed, total)