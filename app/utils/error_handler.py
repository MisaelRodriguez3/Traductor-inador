from PyQt6.QtWidgets import QMessageBox
from .style_loader import load_stylesheet
import app.exceptions.translation as te
import app.exceptions.authorization as ae

def show_error(message: str, parent=None, title="Error", is_critical = True):
    msg = QMessageBox(parent)
    msg.setStyleSheet(load_stylesheet('alerts.qss', 'widgets'))
    if is_critical:
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error Crítico" if not title else title)
    else:
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Advertencia" if not title else title)
    
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    
    msg.adjustSize()
    msg.exec()

def handle_error(e: Exception, parent=None):
    match e:
        case te.TranslationServiceUnavailable():
            show_error("El servicio de traducción no está disponible.", parent)
        case te.TranslationFailed():
            show_error("La traducción falló. Verifica el texto o el idioma.", parent, is_critical=False)
        case TimeoutError():
            show_error("Tiempo de espera agotado. Verifica tu conexión a internet.", parent)
        case ae.Unauthorized():
            show_error('La API no esta configurada', parent)
        case Exception():
            show_error(str(e), parent)  
        case _:
            show_error(f"Ocurrió un error inesperado: {str(e)}", parent)
