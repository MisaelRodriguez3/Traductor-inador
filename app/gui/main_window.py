from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from .text_translator import TextTranslatorTab
from .doc_translator import DocTranslatorTab
from .config import ConfigView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self._setup_ui()
        
    def _setup_ui(self):
        self.tabs = QTabWidget()
        self.text_translator_tab = TextTranslatorTab()
        self.doc_translator_tab = DocTranslatorTab()
        self.config_tab = ConfigView()
        
        self.tabs.addTab(self.text_translator_tab, "Text Translator")
        self.tabs.addTab(self.doc_translator_tab, "Document Translator")
        self.tabs.addTab(self.config_tab, "Configuración")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)