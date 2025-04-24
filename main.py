import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.gui.main_window import MainWindow
from app.utils.style_loader import load_stylesheet
from app.utils.get_resource import resource_path
from app.utils.error_handler import handle_error

def main() -> None:
    """Main entry point for the translation application.
    
    Initializes and configures the GUI application with:
    - Application metadata and branding
    - Styling configuration
    - Error handling setup
    - Main window presentation

    Raises:
        Exception: Any unhandled errors during startup will be passed to handle_error()
    """
    try:
        # Initialize Qt application
        app = QApplication(sys.argv)
        
        # Configure application properties
        app.setWindowIcon(QIcon(resource_path('app/assets/icono.ico')))
        app.setApplicationName('Traductor-inador')
        app.setStyleSheet(load_stylesheet('base.qss'))  # Load core styles
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        # Start event loop and handle exit status
        sys.exit(app.exec())
        
    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    main()