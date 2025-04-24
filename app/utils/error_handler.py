from PyQt6.QtWidgets import QMessageBox
from .style_loader import load_stylesheet
import app.exceptions.translation as te
import app.exceptions.authorization as ae
import app.exceptions.document as de

def show_error(message: str, parent=None, title="Error", is_critical=True) -> None:
    """Displays a styled error/warning dialog box to the user.
    
    Creates and shows a modal QMessageBox with application-specific styling
    and appropriate severity icon.

    Args:
        message (str): Main text content to display
        parent (QWidget, optional): Parent widget for dialog positioning.
            Defaults to None.
        title (str, optional): Window title text. Defaults to "Error".
        is_critical (bool, optional): Determines dialog type.
            True for Critical, False for Warning. Defaults to True.

    Example:
        >>> show_error("File not found", self, "Loading Error")
        >>> show_error("Minor issue", is_critical=False)
    """
    msg = QMessageBox(parent)
    msg.setStyleSheet(load_stylesheet('alerts.qss', 'widgets'))
    
    if is_critical:
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
    else:
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Warning")

    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.adjustSize()
    msg.exec()

def handle_error(e: Exception, parent=None) -> None:
    """Handles application exceptions and displays user-friendly messages.
    
    Maps specific exception types to appropriate error dialogs with
    pre-defined messaging and severity levels.

    Args:
        e (Exception): The exception to handle
        parent (QWidget, optional): Parent widget for dialog positioning.
            Defaults to None.

    Handled Exceptions:
        TranslationServiceUnavailable: Critical error
        TranslationFailed: Warning-level error
        TranslationError: Critical error
        Unauthorized: Critical API config error
        DocumentNotFound: Critical file error
        DocumentReadError: Critical file error
        DocumentWriteError: Critical file error
        ParagraphTranslationError: Critical content error
        TimeoutError: Network error warning
        Exception: Fallback for unhandled exceptions

    Example:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     handle_error(e)
    """
    match e:
        case te.TranslationServiceUnavailable():
            show_error(str(e), parent)
        case te.TranslationFailed():
            show_error(str(e), parent, is_critical=False)
        case te.TranslationError():
            show_error(str(e), parent)
        case ae.Unauthorized():
            show_error('API not configured', parent)
        case de.DocumentNotFound():
            show_error(str(e), parent)
        case de.DocumentReadError():
            show_error(str(e), parent)
        case de.DocumentWriteError():
            show_error(str(e), parent)
        case de.ParagraphTranslationError():
            show_error(str(e), parent)
        case TimeoutError():
            show_error("Connection timeout. Check internet.", parent)
        case Exception():
            show_error(str(e), parent)
        case _:
            show_error(f"Unexpected error: {str(e)}", parent)