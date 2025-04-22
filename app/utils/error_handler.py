from PyQt6.QtWidgets import QMessageBox
from .style_loader import load_stylesheet
import app.exceptions.translation as te
import app.exceptions.authorization as ae
import app.exceptions.document as de

def show_error(message: str, parent=None, title="Error", is_critical = True):
    msg = QMessageBox(parent)
    msg.setStyleSheet(load_stylesheet('alerts.qss', 'widgets'))
    if is_critical:
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
    else:
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Advertencia")
    
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    
    msg.adjustSize()
    msg.exec()

def handle_error(e: Exception, parent=None):
    match e:
        case te.TranslationServiceUnavailable():
            show_error(str(e), parent)
        case te.TranslationFailed():
            show_error(str(e), parent, is_critical=False)
        case te.TranslationError():
            show_error(str(e), parent)
        case ae.Unauthorized():
            show_error('La API no esta configurada', parent)
        case de.DocumentNotFound():
            show_error(str(e), parent)
        case de.DocumentReadError():
            show_error(str(e), parent)
        case de.DocumentWriteError():
            show_error(str(e), parent)
        case de.ParagraphTranslationError():
            show_error(str(e), parent)
        case TimeoutError():
            show_error("Tiempo de espera agotado. Verifica tu conexión a internet.", parent)
        case Exception():
            print('exc')
            show_error(str(e), parent)
        case _:
            show_error(f"Ocurrió un error inesperado: {str(e)}", parent)