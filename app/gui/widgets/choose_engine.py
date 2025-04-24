from typing import Literal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QGroupBox, QHBoxLayout, QSizePolicy
from app.core.constants import Engine
from app.core.config import Config

class ChooseEngine(QWidget):
    """UI component for selecting translation engines with configuration support.
    
    Provides different interface modes:
    - Compact mode: Single engine selector for specific sections
    - Configuration mode: Multi-section engine configuration panel
    
    Attributes:
        SECTIONS (list[str]): Supported application sections requiring engine configuration
        section_combos (dict[str, QComboBox]): Mapping of section names to QComboBox widgets
        changes (bool): Flag indicating unsaved configuration changes
    """
    
    SECTIONS = ['text', 'doc']  # Available configuration sections

    def __init__(self, section: Literal['text', 'doc'] | None = None, is_config: bool = False):
        """Initializes engine selector in either normal or configuration mode.
        
        Args:
            section (Literal['text', 'doc']): Active section for compact mode. One of ['text', 'doc']
            is_config (bool): True to enable multi-section configuration interface
        
        Note:
            Compact mode shows single selector, config mode shows all sections
        """
        super().__init__()
        self.section = section
        self.section_combos = {}  # Section-to-combo mapping
        self.changes = False  # Configuration change flag
        self.init_ui() if not is_config else self.init_config_ui()

    def init_ui(self) -> None:
        """Initializes compact UI with single engine selector."""
        layout = QHBoxLayout()
        self.combo_engine = QComboBox()
        
        # Populate with formatted engine names
        for engine in Engine:
            engine_name = engine.name.replace('_', ' ').title()
            self.combo_engine.addItem(engine_name)
        
        # Set initial value from config
        combo_value = Config.get(f'engine_{self.section}') or 'My Memory'
        self.combo_engine.setCurrentText(combo_value)
        self.combo_engine.currentTextChanged.connect(self.save_section_engine)

        layout.addWidget(QLabel('Translation Engine: '))
        layout.addWidget(self.combo_engine)
        self.setLayout(layout)

    def init_config_ui(self) -> None:
        """Initializes configuration UI with multiple section selectors."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        global_group = QGroupBox("Translation Engines")
        global_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        group_layout = QVBoxLayout()

        # Create selector for each section
        for section in self.SECTIONS:
            section_layout = QHBoxLayout()
            combo = QComboBox()
            
            for engine in Engine:
                engine_name = engine.name.replace('_', ' ').title()
                combo.addItem(engine_name)

            # Initialize from config
            saved_engine = Config.get(f"engine_{section}")
            combo.setCurrentText(saved_engine if saved_engine else 'My Memory')
            combo.currentTextChanged.connect(self._changes)
            self.section_combos[section] = combo

            section_layout.addWidget(QLabel(f"{section.title()} Translator"))
            section_layout.addWidget(combo)
            group_layout.addLayout(section_layout)

        global_group.setLayout(group_layout)
        layout.addWidget(global_group)
        self.setLayout(layout)

    def _changes(self) -> None:
        """Internal slot for tracking configuration modifications."""
        self.changes = True

    def save_section_engine(self) -> None:
        """Persists engine selections to application configuration."""
        if self.section:  # Compact mode
            engine = self.combo_engine.currentText()
            Config.set(f'engine_{self.section}', engine)
        else:  # Config mode
            for section, combo in self.section_combos.items():
                engine = combo.currentText()
                Config.set(f'engine_{section}', engine)

    @property
    def engine(self) -> Engine:
        """Currently selected translation engine.
        
        Returns:
            Engine: Engine enum value for the selected translation service
            
        Note:
            Falls back to My Memory if no selection exists
        """
        engine = Config.get(f'engine_{self.section}') or 'My Memory'
        return Engine[engine.replace(' ', '_').upper()]
    
    @property
    def engine_available(self) -> bool:
        """Verifies engine availability through API configuration.
        
        Returns:
            bool: True if engine is My Memory or has valid API config.
            False for configured engines missing API credentials
        """
        api = Config.get(f'{self.engine}_api')
        return api is not None or self.engine == Engine.MY_MEMORY