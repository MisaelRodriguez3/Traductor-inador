from typing import Literal
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QSizePolicy)
from PyQt6.QtGui import QIntValidator
from app.utils.style_loader import load_stylesheet

class RangeField(QWidget):
    """Range field with horizontal expansion."""
    
    def __init__(self, parent: QWidget | None=None):
        """Initializes range field widget with default styling.
        Args:
            parent (QWidget | None, optional): _description_. Defaults to None.
        """
        super().__init__(parent)
        self.setStyleSheet(load_stylesheet('range.qss', 'widgets'))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.init_ui()
        self._setup_validators()
        self._connect_signals()
        
    def init_ui(self):
        """Initializes UI of the widget range."""
        # Field 'Start'
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Start")
        self.start_input.setObjectName('range_input')
        
        # Field 'End'
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("End")
        self.end_input.setObjectName('range_input')
        
        # Delete Button
        self.delete_btn = QPushButton("X")
        self.delete_btn.setToolTip("Eliminar rango")
        self.delete_btn.setObjectName('delete_button')
        
        # Layout
        self.layout.addWidget(QLabel("Rango:"))
        self.layout.addWidget(self.start_input, stretch=1)
        self.layout.addWidget(QLabel("-"))
        self.layout.addWidget(self.end_input, stretch=1)
        self.layout.addWidget(self.delete_btn)

    def _setup_validators(self):
        """Numerical validators"""
        validator = QIntValidator(1, 9999)
        self.start_input.setValidator(validator)
        self.end_input.setValidator(validator)

    def _connect_signals(self):
        """Connect validation signals"""
        self.start_input.textChanged.connect(self.validate_inputs)
        self.end_input.textChanged.connect(self.validate_inputs)

    def validate_inputs(self):
        """Validate entries and update status"""
        start_text = self.start_input.text()
        end_text = self.end_input.text()

        try:
            start_val = int(start_text) if start_text else 0
            end_val = int(end_text) if end_text else start_val
        except ValueError:
            self._mark_invalid('both')
            return

        if start_val <= 0 and end_val <= 0:
            self._mark_invalid('both')
        elif start_val <= 0:
            self._mark_invalid('start')
        elif end_val < start_val:
            self._mark_invalid('end')
        else:
            self._mark_invalid(None)
        
    def _mark_invalid(self, input: Literal['start', 'end', 'both'] | None):
        """Dynamically highlights invalid fields"""
        def update_field(field: QLineEdit, has_error: bool):
            field.setProperty('fieldType', 'error' if has_error else '')
            field.style().unpolish(field)
            field.style().polish(field)

        match input:
            case 'start':
                update_field(self.start_input, True)
                update_field(self.end_input, False)
            case 'end':
                update_field(self.start_input, False)
                update_field(self.end_input, True)
            case 'both':
                update_field(self.start_input, True)
                update_field(self.end_input, True)
            case None:
                update_field(self.start_input, False)
                update_field(self.end_input, False)