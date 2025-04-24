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
from .widgets.choose_engine import ChooseEngine
from app.core.config import Config
from app.core.constants import Engine
from app.validators.validators import is_not_empty
from app.utils.style_loader import load_stylesheet

class ConfigView(QWidget):
    """Application configuration panel with theme settings and API management.
    
    Provides UI components for:
    - Dark/light theme selection
    - API key configuration for translation services
    - Translation engine selection per feature section
    
    Attributes:
        api_fields (dict[str, QLineEdit]): Dictionary mapping engine names to input fields
        switch (Switch): Theme toggle switch widget
        choose_engine (ChooseEngine): Engine selection component
    """

    api_fields: dict[str, QLineEdit]

    def __init__(self) -> None:
        """Initializes configuration view with styled components."""
        super().__init__()
        self.setStyleSheet(load_stylesheet('config.qss', 'screens'))
        self.api_fields = {}
        self.init_ui()

    def init_ui(self) -> None:
        """Sets up UI layout and components."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(50, 20, 50, 20)

        # Theme Section
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout()
        
        theme_control = QHBoxLayout()
        theme_control.addWidget(QLabel("Dark Mode:"))
        self.switch = Switch()
        self.switch.stateChanged.connect(self.change_theme)
        self.switch.setChecked(Config.get('theme') == 'dark')
        theme_control.addWidget(self.switch)
        theme_control.addStretch()
        
        theme_group.setLayout(theme_layout)
        theme_layout.addLayout(theme_control)
        layout.addWidget(theme_group)

        # API Configuration Section
        api_group = QGroupBox("API Settings")
        api_layout = QVBoxLayout()

        # Create input fields for each engine requiring API keys
        for engine in Engine:
            if engine == Engine.MY_MEMORY:
                continue  # Skip MyMemory which doesn't require API key
            field = QLineEdit()
            self.api_fields[engine.name] = field
            self._create_api_field(api_layout, 
                                 f"{engine.name.replace('_', ' ').title()} API:", 
                                 field)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # Engine Selection
        self.choose_engine = ChooseEngine(is_config=True)
        layout.addWidget(self.choose_engine)

        # Action Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save Changes")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.save_settings)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.load_info()

    def load_info(self) -> None:
        """Loads persisted configuration values into UI components."""
        for engine, line_edit in self.api_fields.items():
            key = f"{engine}_api"
            value = Config.get(key) or ""
            if is_not_empty(value):
                line_edit.setText(value)

    def _create_api_field(self, 
                         layout: QVBoxLayout, 
                         label_text: str, 
                         field: QLineEdit) -> None:
        """Creates a labeled input field row.
        
        Args:
            layout (QVBoxLayout): Parent layout to add components
            label_text (str): Field description text
            field (QLineEdit): Input component to display
        """
        h_layout = QHBoxLayout()
        label = QLabel(label_text)
        field.setPlaceholderText(f"Enter {label_text.split(':')[0].lower()}")
        h_layout.addWidget(label)
        h_layout.addWidget(field, stretch=3)
        layout.addLayout(h_layout)

    def save_settings(self) -> None:
        """Persists modified settings to configuration store.
        
        Saves changes only for modified values and shows success notification.
        """
        changes = False
        
        # Save API keys
        for engine, line_edit in self.api_fields.items():
            key = f"{engine}_api"
            new_value = line_edit.text()
            prev_value = Config.get(key)
            
            if new_value != prev_value and (is_not_empty(new_value) or prev_value):
                Config.set(key, new_value)
                changes = True

        # Save engine selections
        if self.choose_engine.changes:
            self.choose_engine.save_section_engine()
            changes = True

        if changes:
            self._show_success_message()

    def change_theme(self) -> None:
        """Handles theme toggle state changes."""
        theme = 'dark' if self.switch.isChecked() else 'light'
        app = QApplication.instance()
        
        if theme == 'light':
            app.setStyleSheet(load_stylesheet('base.qss'))
        else:
            app.setStyleSheet(load_stylesheet('dark.qss', 'theme'))
            
        Config.set("theme", theme)

    def _show_success_message(self) -> None:
        """Displays save confirmation dialog centered in parent."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Success")
        msg.setText("Settings saved successfully!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setStyleSheet(load_stylesheet('alerts.qss', 'widgets'))
        msg.adjustSize()
        
        # Center dialog relative to parent
        parent_center = self.geometry().center()
        msg_geometry = msg.frameGeometry()
        msg_geometry.moveCenter(parent_center)
        msg.move(msg_geometry.center())
        
        msg.exec()