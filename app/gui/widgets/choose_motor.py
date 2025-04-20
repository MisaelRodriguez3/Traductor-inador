from typing import Literal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QGroupBox, QHBoxLayout, QSizePolicy
from app.core.constants import Motor
from app.core.config import Config

class ChooseMotor(QWidget):
    SECTIONS = ['text', 'doc']  # Las secciones disponibles

    def __init__(self, section: Literal['text', 'doc'] | None = None, is_config: bool = False):
        super().__init__()
        self.section = section
        self.section_combos = {}  # Diccionario de combos por sección
        self.changes = False
        self.init_ui() if not is_config else self.init_config_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.combo_motor = QComboBox()
        for motor in Motor:
            motor_name = motor.name.replace('_', ' ').title()
            self.combo_motor.addItem(motor_name)
        
        # Establecer el valor del combo de motor, por defecto 'My memory' si no está guardado
        combo_value = Config.get(f'motor_{self.section}') or 'My Memory'
        self.combo_motor.setCurrentText(combo_value)
        self.combo_motor.currentTextChanged.connect(self.save_section_motor)

        layout.addWidget(QLabel('Motor de traducción: '))
        layout.addWidget(self.combo_motor)
        self.setLayout(layout)

    def init_config_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        # Combo global
        global_group = QGroupBox("Motores de traducción")
        global_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # Política horizontal
            QSizePolicy.Policy.Fixed       # Política vertical
        )
        group_layout = QVBoxLayout()


        # Combos por sección
        for section in self.SECTIONS:
            section_layout = QHBoxLayout()
            combo = QComboBox()
            for motor in Motor:
                motor_name = motor.name.replace('_', ' ').title()
                combo.addItem(motor_name)

            # Establecer el motor guardado para cada sección
            saved_motor = Config.get(f"motor_{section}")
            combo.setCurrentText(saved_motor if saved_motor else 'My Memory')
            combo.currentTextChanged.connect(self._changes)
            self.section_combos[section] = combo

            section_layout.addWidget(QLabel(f"{section.title()} Translator"))
            section_layout.addWidget(combo)
            group_layout.addLayout(section_layout)

        global_group.setLayout(group_layout)
        layout.addWidget(global_group)

        self.setLayout(layout)

    def _changes(self):
        self.changes = True


    def save_section_motor(self):
        if self.section:
            motor = self.combo_motor.currentText()
            Config.set(f'motor_{self.section}', motor)
        else:
            for section, combo in self.section_combos.items():
                motor = combo.currentText()
                Config.set(f'motor_{section}', motor)

    @property
    def motor(self) -> Motor:
        """Devuelve el motor seleccionado para la sección o el global si no hay uno definido."""
        motor = Config.get(f'motor_{self.section}') or 'My Memory'
        return Motor[motor.replace(' ', '_').upper()]
    
    @property
    def motor_available(self):
        api = Config.get(f'{self.motor}_api')
        if api is None and self.motor != Motor.MY_MEMORY:
            return False
        return True
