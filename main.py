import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.gui.main_window import MainWindow
from app.utils.style_loader import load_stylesheet
from app.utils.get_resource import resource_path
from app.utils.error_handler import handle_error

def main():
    try:
        app = QApplication(sys.argv)
        icon = resource_path('app/assets/icono.ico')
        app.setWindowIcon(QIcon(icon))
        app.setApplicationName('Traductor-inador')
        app.setStyleSheet(load_stylesheet('base.qss'))
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    main()