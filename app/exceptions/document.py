class DocumentProcessingError(Exception):
    """Base exception for document processing operations.
    
    This exception serves as the foundation for all document-related errors.
    Should be subclassed to create specific document processing exceptions.
    
    Attributes:
        message (str): Explanation of the error (inherited from Exception)
    
    Example:
        >>> raise DocumentProcessingError("Generic document error")
        DocumentProcessingError: Generic document error
    
    Note:
        Catch this exception to handle all document-related errors generically
    """

class DocumentNotFound(DocumentProcessingError):
    """Raised when the input document file cannot be located.
    
    Typical scenarios:
    - Invalid file path provided
    - File deleted/moved after validation
    - Network drive disconnection
    
    Attributes:
        message (str): Human-readable description with path details
    
    Example:
        >>> raise DocumentNotFound("File not found: /path/to/document.docx")
        DocumentNotFound: File not found: /path/to/document.docx
    """

class DocumentReadError(DocumentProcessingError):
    """Raised when failing to read document contents.
    
    Common causes:
    - Corrupted file structure
    - Unsupported file format
    - Insufficient read permissions
    - File locked by another process
        
    Attributes:
        message (str): Human-readable description with path details
    
    Example:
        >>> raise DocumentReadError("Invalid DOCX format detected")
        DocumentReadError: Invalid DOCX format detected
    """

class DocumentWriteError(DocumentProcessingError):
    """Raised when failing to save document changes.
    
    Typical failure points:
    - Disk full or write permissions
    - Invalid output path
    - File locked for editing
    - Network storage unavailable
        
    Attributes:
        message (str): Human-readable description with path details
    
    Example:
        >>> raise DocumentWriteError("Cannot write to read-only directory")
        DocumentWriteError: Cannot write to read-only directory
    """

class ParagraphTranslationError(DocumentProcessingError):
    """Raised when paragraph translation fails.
    
    Common causes:
    - API translation service failure
    - Invalid text encoding
    - Unsupported language pair
    - Special content formatting issues
        
    Attributes:
        message (str): Human-readable description with path details
    
    Example:
        >>> raise ParagraphTranslationError("Failed to translate paragraph 5")
        ParagraphTranslationError: Failed to translate paragraph 5
    
    Note:
        May contain paragraph index/context in error message
    """