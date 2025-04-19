class DocxProcessorError(Exception):
    """Excepción base para errores del procesador de documentos"""

class DocumentProcessingError(DocxProcessorError):
    """Error en el procesamiento del documento"""