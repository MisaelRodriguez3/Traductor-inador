from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QCheckBox, QSizePolicy)
from PyQt6.QtCore import Qt
from .range import RangeField

class SkipPages(QWidget):
    """Expandable widget for page selection"""

    def __init__(self):
        """Initializes skip pages widget."""
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.ranges: list[RangeField] = []
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        """Initial configuration of the interface"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(8)
        
        # Checkbox for cover page
        self.skip_cover_check = QCheckBox("Ommit Cover Page")
        self.skip_cover_check.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(self.skip_cover_check)
        
        # Container for add button
        btn_container = QWidget()
        btn_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        self.add_range_btn = QPushButton('Add Range')
        btn_layout.addWidget(self.add_range_btn)
        btn_layout.addStretch()
        
        self.main_layout.addWidget(btn_container)
        self.main_layout.addStretch()

    def _connect_signals(self):
        """Connect validation signals"""
        self.add_range_btn.clicked.connect(self._add_range_field)
        self.skip_cover_check.stateChanged.connect(self._handle_cover_page)

    def _handle_cover_page(self, state: int):
        """Handle the status of the cover page"""
        self.skip_cover_check.setChecked(state == Qt.CheckState.Checked)

    def _add_range_field(self):
        """Add a new range field"""
        new_range = RangeField()
        new_range.delete_btn.clicked.connect(lambda: self._remove_range(new_range))
        self.ranges.append(new_range)
        self.main_layout.insertWidget(self.main_layout.count() - 1, new_range)

    def _remove_range(self, range_widget: RangeField):
        """Delete one range field"""
        range_widget.deleteLater()
        self.ranges.remove(range_widget)

    @property
    def skip_pages(self) -> set[int]:
        """Calculate pages to be skipped with validation"""
        pages = set()
        
        if self.skip_cover_check.isChecked():
            pages.add(1)
            
        for range_field in self.ranges:
            
            start = range_field.start_input.text()
            end = range_field.end_input.text()
            
            if not start:
                continue
                
            start_val = int(start)
            end_val = int(end) if end else start_val
            
            if start_val < 1 or end_val < start_val:
                continue
                
            pages.update(range(start_val, end_val + 1))
            
                
        return pages