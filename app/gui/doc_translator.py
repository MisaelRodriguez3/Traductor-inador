from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QFileDialog, 
    QLabel, 
    QComboBox, 
    QProgressBar, 
    QMessageBox, 
    QStyle
)
from PyQt6.QtCore import QThread, Qt
from app.exceptions.authorization import Unauthorized
from .document_worker import DocumentWorker
from .widgets.choose_engine import ChooseEngine
from .widgets.skip_pages import SkipPages
from app.core.translator import TranslationManager
from app.core.constants import LANGUAGES
from app.utils.error_handler import handle_error
from app.utils.style_loader import load_stylesheet
    
class DocTranslatorTab(QWidget):
    """Document translation interface component for handling DOCX files.
    
    Provides a GUI for:
    - Selecting translation engine
    - Choosing source/target languages
    - File selection and translation execution
    - Progress monitoring
    
    Attributes:
        choose_engine (ChooseEngine): Translation engine selector component
        tm (TranslationManager): Translation manager instance
        current_file(str | None): Path to currently selected document
        languages (dict[str, str]): Available languages mapping (display name to code)
    """

    def __init__(self):
        """Initializes document translator tab with default configuration."""
        super().__init__()
        self.setStyleSheet(load_stylesheet('doc_translator.qss', 'screens'))
        self.choose_engine = ChooseEngine('doc')
        self.engine = self.choose_engine.engine
        self.tm = TranslationManager(self.engine)
        self.skip_pages = SkipPages()
        self.current_file = None
        self.languages = LANGUAGES
        self.init_ui()
        self.connect_signals()

    def init_ui(self) -> None:
        """Initializes UI layout and components."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Engine selection
        layout.addWidget(self.choose_engine)

        # Language selection
        lang_layout = QHBoxLayout()
        self.combo_from = QComboBox()
        self.combo_to = QComboBox()
        
        for lang in self.languages:
            self.combo_from.addItem(lang)
            self.combo_to.addItem(lang)
            
        self.combo_from.setCurrentText('Español')
        self.combo_to.setCurrentText("Inglés")

        lang_layout.addWidget(QLabel("Source Language: "))
        lang_layout.addWidget(self.combo_from)
        lang_layout.addStretch()
        lang_layout.addWidget(QLabel("Target Language:"))
        lang_layout.addWidget(self.combo_to)
        lang_layout.addStretch()

        # File controls
        self.select_btn = QPushButton("Select DOCX")
        self.select_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        
        self.translate_btn = QPushButton("Translate Document")
        self.translate_btn.setEnabled(False)
        self.translate_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))

        # File info
        self.file_label = QLabel("No document selected")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("color: #666; font-style: italic;")

        # Progress indicator
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # Layout assembly
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.translate_btn)
        
        layout.addLayout(lang_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.file_label)
        layout.addWidget(self.skip_pages)
        layout.addWidget(self.progress_bar)
        layout.addStretch()
        
        self.setLayout(layout)

    def connect_signals(self) -> None:
        """Connects UI element signals to handler methods."""
        self.select_btn.clicked.connect(self.select_document)
        self.translate_btn.clicked.connect(self.start_translation)

    def select_document(self) -> None:
        """Handles document selection through file dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Document",
            "",
            "Word Documents (*.docx)"
        )
        
        if file_path:
            self.current_file = file_path
            self.file_label.setText(f"Selected document: {file_path.split('/')[-1]}")
            self.translate_btn.setEnabled(True)

    def start_translation(self) -> None:
        """Initiates document translation process in background thread.
        
        Raises:
            Unauthorized: If selected engine lacks required API configuration
            Exception: Propagates any errors during setup
        """
        try:
            if not self.current_file:
                return
            if not self.choose_engine.engine_available:
                raise Unauthorized()
                
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Translated Document",
                "",
                "Word Documents (*.docx)"
            )

            if not save_path:
                return
            
            # Initialize progress UI
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setEnabled(False)

            # Configure translation parameters
            lang_from = self.languages[self.combo_from.currentText()]
            lang_to = self.languages[self.combo_to.currentText()]
            skip_pages = self.skip_pages.skip_pages

            # Start background worker
            self.worker_thread = QThread()
            self.worker = DocumentWorker(
                self.current_file,
                save_path,
                lang_from,
                lang_to,
                self.tm,
                skip_pages
            )

            # Connect worker signals
            self.worker.progress_updated.connect(self.update_progress)
            self.worker.finished.connect(self.on_translation_finished)
            self.worker.error_occurred.connect(self.show_error)

            self.worker.moveToThread(self.worker_thread)
            self.worker_thread.started.connect(self.worker.process)
            self.worker_thread.start()

        except Exception as e:
            handle_error(e, self)

    def update_progress(self, value: int) -> None:
        """Updates progress bar with current translation progress.
        
        Args:
            value (int): Percentage completion (0-100)
        """
        self.progress_bar.setValue(value)

    def on_translation_finished(self, output_path: str) -> None:
        """Handles successful translation completion.
        
        Args:
            output_path (str): Path to generated translated document
        """
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.progress_bar.setVisible(False)
        self.setEnabled(True)
        QMessageBox.information(
            self,
            "Translation Complete",
            f"Document saved at:\n{output_path}"
        )
    def show_error(self, error: Exception) -> None:
        """Handles translation errors from worker thread.
        
        Args:
            error (Exception): Exception raised during translation
        """
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.progress_bar.setVisible(False)
        self.setEnabled(True)
        handle_error(error, self)