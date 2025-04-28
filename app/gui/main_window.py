from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QScrollArea
from .text_translator import TextTranslatorTab
from .doc_translator import DocTranslatorTab
from .config import ConfigView

class MainWindow(QMainWindow):
    """Main application window with tabbed interface for different translation features.   
    
    Provides access to:
    - Text translation interface
    - Document translation interface
    - Application configuration panel

    Attributes:
        tabs (QTabWidget): Container for application feature tabs
        text_translator_tab (TextTranslatorTab): Text translation component
        doc_translator_tab (DocTranslatorTab): Document translation component
        config_tab (ConfigView): Settings configuration component
    """

    def __init__(self) -> None:
        """Initializes main window with default geometry and UI components."""
        super().__init__()
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Configures window layout and tabbed interface.
        
        Private method that:
        - Creates tab container widget
        - Initializes feature components
        - Sets up main window layout
        """
        self.tabs = QTabWidget()
        
        # Initialize application features
        self.text_translator_tab = self._create_scrollable_tab(TextTranslatorTab())
        self.doc_translator_tab = self._create_scrollable_tab(DocTranslatorTab())
        self.config_tab = self._create_scrollable_tab(ConfigView())

        # Add tabs with translated titles
        self.tabs.addTab(self.text_translator_tab, "Text Translator")
        self.tabs.addTab(self.doc_translator_tab, "Document Translator")
        self.tabs.addTab(self.config_tab, "Configuration")

        # Set up main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _create_scrollable_tab(self, widget: QWidget) -> QScrollArea:
        """Create a scrolling tab without visible borders.

        Args:
            widget (QWidget): Tab to apply scroll

        Returns:
            QScrollArea: A scrolling tab
        """
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("custom_scroll")
        
        scroll_area.setWidget(widget)
        return scroll_area