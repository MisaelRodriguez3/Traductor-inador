from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QApplication,
    QGroupBox
)
from PyQt6.QtCore import Qt
from .widgets.switch import Switch
from .widgets.choose_motor import ChooseMotor
from app.core.config import Config
from app.core.constants import Motor
from app.validators.validators import is_not_empty
from app.utils.style_loader import load_stylesheet

class ConfigView(QWidget):
    api_fields: dict[str, QLineEdit]

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(load_stylesheet('config.qss', 'screens'))
        self.api_fields = {}
        self.init_ui()

    def init_ui(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(50, 20, 50, 20)

        # Sección de Tema
        theme_group = QGroupBox("Apariencia")
        theme_layout = QVBoxLayout()
        
        theme_control = QHBoxLayout()
        theme_control.addWidget(QLabel("Modo oscuro:"))
        self.switch = Switch()
        self.switch.stateChanged.connect(self.change_theme)
        self.switch.setChecked(True if Config.get('theme') == 'dark' else False)
        theme_control.addWidget(self.switch)
        theme_control.addStretch()
        
        theme_layout.addLayout(theme_control)
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)

        # Sección de APIs
        api_group = QGroupBox("Configuración de APIs")
        api_layout = QVBoxLayout()

        # Campos de entrada para cada motor con API
        for motor in Motor:
            if motor == Motor.MY_MEMORY:
                continue
            field: QLineEdit = QLineEdit()
            self.api_fields[motor.name] = field
            self._create_api_field(api_layout, f"{motor.replace('_', ' ').title()} API:", field)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        self.choose_motor = ChooseMotor(is_config=True)
        layout.addWidget(self.choose_motor)

        # Botones
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Guardar cambios")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_settings)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_info()

    def load_info(self) -> None:
        """Carga los valores almacenados previamente"""
        for motor, line_edit in self.api_fields.items():
            key: str = f"{motor}_api"
            value: str = Config.get(key) or ""
            if is_not_empty(value):
                line_edit.setText(value)

    def _create_api_field(self, layout: QVBoxLayout, label_text: str, field: QLineEdit) -> None:
        """Crea un campo con etiqueta y entrada alineados"""
        h_layout: QHBoxLayout = QHBoxLayout()
        label: QLabel = QLabel(label_text)
        field.setPlaceholderText(f"Ingrese {label_text.split(':')[0].lower()}")
        h_layout.addWidget(label)
        h_layout.addWidget(field, stretch=3)
        layout.addLayout(h_layout)

    def save_settings(self) -> None:
        """Guarda los valores si cambiaron"""
        changes: bool = False
        for motor, line_edit in self.api_fields.items():
            key: str = f"{motor}_api"
            new_value: str = line_edit.text()
            prev_value: str | None = Config.get(key)
            if new_value != prev_value and (is_not_empty(new_value) or prev_value):
                Config.set(key, new_value)
                changes = True
        if self.choose_motor.changes:
                self.choose_motor.save_section_motor()
                changes = True
        if changes:
            self._show_success_message()

    def change_theme(self):
        theme = 'dark' if self.switch.isChecked() else 'light'
        app = QApplication.instance()
        if theme == 'light':
            app.setStyleSheet(load_stylesheet('base.qss'))
            Config.set("theme", 'light')
        else:
            Config.set("theme", 'dark')
            app.setStyleSheet(load_stylesheet('dark.qss', 'theme'))

    def _show_success_message(self) -> None:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Éxito")
        msg.setText("¡Configuración guardada correctamente!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet(load_stylesheet('alerts.qss', 'widgets'))
        msg.adjustSize()
        parent_center = self.geometry().center()
        msg_geometry = msg.frameGeometry()
        msg_geometry.moveCenter(parent_center)
        msg.move(msg_geometry.center())
        msg.exec()
