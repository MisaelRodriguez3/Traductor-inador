from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QTextEdit, 
    QPushButton, 
    QLabel, 
    QComboBox
)
from .widgets.choose_motor import ChooseMotor
from app.core.translator import TranslationManager
from app.core.constants import LANGUAGES
from app.exceptions.authorization import Unauthorized
from app.utils.error_handler import handle_error
from app.utils.style_loader import load_stylesheet
import re


class TextTranslatorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_stylesheet('text_translator.qss', 'screens'))
        self.choose_motor = ChooseMotor('text')
        self.motor = self.choose_motor.motor
        self.tm = TranslationManager(self.motor)
        self.languages = LANGUAGES
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(self.choose_motor)

        # Texto a traducir
        layout.addWidget(QLabel("Texto a traducir:"))
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Escribe aquí el texto original...")
        layout.addWidget(self.input_text)

        # Selección de idiomas
        lang_layout = QHBoxLayout()

        self.combo_from = QComboBox()
        self.combo_to = QComboBox()
        for lang in self.languages:
            self.combo_from.addItem(lang)
            self.combo_to.addItem(lang)

        self.combo_from.setCurrentText("Español")
        self.combo_to.setCurrentText("Inglés")

        lang_layout.addWidget(QLabel("De:"))
        lang_layout.addWidget(self.combo_from)
        lang_layout.addWidget(QLabel("A:"))
        lang_layout.addWidget(self.combo_to)

        layout.addLayout(lang_layout)

        # Botón traducir
        self.button_translate = QPushButton("Traducir")
        self.button_translate.clicked.connect(self.translate_text)
        layout.addWidget(self.button_translate)

        # Resultado
        layout.addWidget(QLabel("Traducción:"))
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        self.setLayout(layout)


    def translate_text(self):
        try:
            original_text = self.input_text.toPlainText()
            if not original_text.strip():
                self.result.setText("Por favor, escribe un texto.")
                return

            lang_from = self.languages[self.combo_from.currentText()]
            lang_to = self.languages[self.combo_to.currentText()]

            if not self.choose_motor.motor_available:
                raise Unauthorized()

            # Dividir por líneas (frases completas) y conservar saltos de línea
            lines = original_text.splitlines(keepends=True)
            translated_lines = []

            for line in lines:
                # Separar espacios iniciales y finales
                leading_spaces = re.match(r'^\s*', line).group()
                trailing_spaces = re.match(r'.*?(\s*)$', line).group(1)

                stripped_line = line.strip()
                if stripped_line:
                    translated = self.tm.translate_text(
                        text=stripped_line,
                        lang_from=lang_from,
                        lang_to=lang_to
                    )
                    translated_line = f"{leading_spaces}{translated}{trailing_spaces}"
                else:
                    translated_line = line  # línea vacía o solo espacios

                translated_lines.append(translated_line)

            result_text = ''.join(translated_lines)
            self.result.setText(result_text)

            print(original_text)
            print(result_text)

        except Exception as e:
            handle_error(e, self)
