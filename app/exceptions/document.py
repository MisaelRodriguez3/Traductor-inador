class DocumentProcessingError(Exception):
    """Error base para el procesamiento de documentos."""


class DocumentNotFound(DocumentProcessingError):
    """Se lanza cuando no se encuentra el archivo de entrada."""


class DocumentReadError(DocumentProcessingError):
    """Se lanza cuando ocurre un error al leer el documento."""


class DocumentWriteError(DocumentProcessingError):
    """Se lanza cuando ocurre un error al guardar el documento."""


class ParagraphTranslationError(DocumentProcessingError):
    """Error al traducir un párrafo o run del documento."""
