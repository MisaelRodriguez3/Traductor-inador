from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QTextEdit, 
    QPushButton, 
    QLabel, 
    QComboBox
)
from .widgets.choose_engine import ChooseEngine
from app.core.translator import TranslationManager
from app.core.constants import LANGUAGES
from app.exceptions.authorization import Unauthorized
from app.utils.error_handler import handle_error
from app.utils.style_loader import load_stylesheet
import re

class TextTranslatorTab(QWidget):
    """Text translation interface component for real-time text conversion.
    
    Provides a GUI for:
    - Selecting translation engine
    - Choosing source/target languages
    - Inputting text and viewing translations
    - Format-preserving translations with whitespace handling

    Attributes:
        choose_engine (ChooseEngine): Translation engine selector component
        tm (TranslationManager): Translation manager instance
        languages (dict[str, str]): Available languages mapping (display name to code)
    """

    def __init__(self):
        """Initializes text translator tab with UI components and translation service."""
        super().__init__()
        self.setStyleSheet(load_stylesheet('text_translator.qss', 'screens'))
        self.choose_engine = ChooseEngine('text')
        self.engine = self.choose_engine.engine
        self.tm = TranslationManager(self.engine)
        self.languages = LANGUAGES
        self.init_ui()

    def init_ui(self) -> None:
        """Initializes and arranges UI components in the layout."""
        layout = QVBoxLayout()

        # Engine selection
        layout.addWidget(self.choose_engine)

        # Input text area
        layout.addWidget(QLabel("Source Text:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text to translate...")
        layout.addWidget(self.input_text)

        # Language selection
        lang_layout = QHBoxLayout()
        self.combo_from = QComboBox()
        self.combo_to = QComboBox()
        
        # Populate language dropdowns
        for lang in self.languages:
            self.combo_from.addItem(lang)
            self.combo_to.addItem(lang)

        # Set default languages
        self.combo_from.setCurrentText("Español")
        self.combo_to.setCurrentText("Inglés")

        lang_layout.addWidget(QLabel("From:"))
        lang_layout.addWidget(self.combo_from)
        lang_layout.addWidget(QLabel("To:"))
        lang_layout.addWidget(self.combo_to)
        layout.addLayout(lang_layout)

        # Translation controls
        self.button_translate = QPushButton("Translate")
        self.button_translate.clicked.connect(self.translate_text)
        layout.addWidget(self.button_translate)

        # Results display
        layout.addWidget(QLabel("Translation:"))
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        self.setLayout(layout)

    def translate_text(self) -> None:
        """Executes text translation while preserving formatting.
        
        Processes input text line-by-line, maintaining:
        - Leading/trailing whitespace
        - Empty lines
        - Line break positions
        
        Raises:
            Unauthorized: If selected engine lacks API configuration
            Exception: Propagates any translation errors to handler
        """
        try:
            original_text = self.input_text.toPlainText()
            if not original_text.strip():
                self.result.setText("Please enter text to translate.")
                return

            lang_from = self.languages[self.combo_from.currentText()]
            lang_to = self.languages[self.combo_to.currentText()]

            if not self.choose_engine.engine_available:
                raise Unauthorized()

            # Preserve line structure and whitespace
            lines = original_text.splitlines(keepends=True)
            translated_lines = []

            for line in lines:
                # Capture leading/trailing whitespace
                leading_spaces = re.match(r'^\s*', line).group()
                trailing_spaces = re.search(r'\s*$', line).group()
                
                stripped_line = line.strip()
                if stripped_line:
                    translated = self.tm.translate_text(
                        text=stripped_line,
                        lang_from=lang_from,
                        lang_to=lang_to
                    )
                    translated_line = f"{leading_spaces}{translated}{trailing_spaces}"
                else:
                    translated_line = line  # Preserve empty lines

                translated_lines.append(translated_line)

            result_text = ''.join(translated_lines)
            self.result.setText(result_text)

        except Exception as e:
            handle_error(e, self)