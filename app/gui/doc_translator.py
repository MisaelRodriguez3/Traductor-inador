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
from .widgets.choose_motor import ChooseMotor
from app.core.translator import TranslationManager
from app.core.constants import LANGUAGES
from app.utils.error_handler import handle_error
from app.utils.style_loader import load_stylesheet
    
class DocTranslatorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(load_stylesheet('doc_translator.qss', 'screens'))
        self.choose_motor = ChooseMotor('doc')
        self.motor = self.choose_motor.motor
        self.tm = TranslationManager(self.motor)
        self.current_file = None
        self.languages = LANGUAGES
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        layout.addWidget(self.choose_motor)
        # Selector de idiomas
        lang_layout = QHBoxLayout()
        
        self.combo_from = QComboBox()
        self.combo_to = QComboBox()
        for lang in self.languages:
            self.combo_from.addItem(lang)
            self.combo_to.addItem(lang)
        self.combo_from.setCurrentText('Español')
        self.combo_to.setCurrentText("Inglés")

        lang_layout.addWidget(QLabel("Idioma de origen: "))
        lang_layout.addWidget(self.combo_from)
        lang_layout.addStretch()


        lang_layout.addWidget(QLabel("Idioma de destino:"))
        lang_layout.addWidget(self.combo_to)
        lang_layout.addStretch()

        # Botones
        self.select_btn = QPushButton("Seleccionar DOCX")
        self.select_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        
        self.translate_btn = QPushButton("Traducir Documento")
        self.translate_btn.setEnabled(False)
        self.translate_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))

        # Info de archivo
        self.file_label = QLabel("Ningún documento seleccionado")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("color: #666; font-style: italic;")

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # Diseño
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.translate_btn)
        
        layout.addLayout(lang_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.file_label)
        layout.addWidget(self.progress_bar)
        layout.addStretch()
        
        self.setLayout(layout)

    def connect_signals(self):
        self.select_btn.clicked.connect(self.select_document)
        self.translate_btn.clicked.connect(self.start_translation)

    def select_document(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Seleccionar documento",
            "",
            "Word Documents (*.docx)"
        )
        
        if file_path:
            self.current_file = file_path
            self.file_label.setText(f"Documento seleccionado: {file_path.split('/')[-1]}")
            self.translate_btn.setEnabled(True)

    def start_translation(self):
        try:
            if not self.current_file:
                return
            if not self.choose_motor.motor_available:
                raise Unauthorized()
            save_dialog = QFileDialog()
            save_path, _ = save_dialog.getSaveFileName(
                self,
                "Guardar documento traducido",
                "",
                "Word Documents (*.docx)"
            )

            if not save_path:
                return
            
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setEnabled(False)

            # Configurar parámetros
            lang_from = self.languages[self.combo_from.currentText()]
            lang_to = self.languages[self.combo_to.currentText()]

            # Ejecutar en un hilo separado
            self.worker_thread = QThread()
            self.worker = DocumentWorker(
                self.current_file,
                save_path,
                lang_from,
                lang_to,
                self.tm
            )

            self.worker.moveToThread(self.worker_thread)
            self.worker.progress_updated.connect(self.update_progress)
            self.worker.finished.connect(self.on_translation_finished)
            self.worker.error_occurred.connect(self.show_error)

            self.worker_thread.started.connect(self.worker.process)
            self.worker_thread.start()
        except Exception as e:
            handle_error(e, self)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_translation_finished(self, output_path):
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.progress_bar.setVisible(False)
        self.setEnabled(True)
        QMessageBox.information(
            self,
            "Traducción completada",
            f"Documento guardado en:\n{output_path}"
        )

    def show_error(self, error: Exception):
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.progress_bar.setVisible(False)
        self.setEnabled(True)
        handle_error(error, self)  # Mostrar el error correctamente
