from PyQt6.QtCore import Qt, QVariantAnimation, QPoint, pyqtSignal, QEasingCurve
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget

class Switch(QWidget):
    """Custom toggle switch widget with smooth animation.
    
    Features:
    - Animated thumb movement with easing
    - Material design-inspired styling
    - Click interaction handling
    - State change notifications
    
    Attributes:
        stateChanged (pyqtSignal): Signal emitted on toggle state change
            Emits: bool - New checked state
            
    Example:
        >>> switch = Switch()
        >>> switch.stateChanged.connect(handle_state_change)
        >>> switch.setChecked(True)
    """

    stateChanged = pyqtSignal(bool)  #: Signal emitted when switch state changes

    def __init__(self, parent: QWidget | None = None):
        """Initializes switch widget with default styling and animation.
        
        Args:
            parent (QWidget, optional): Parent widget container. Defaults to None.
        """
        super().__init__(parent)
        self.setFixedSize(70, 34)
        self._checked = False
        self._thumb_position = 4
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Configure animation
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(200)  # ms
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value: int) -> None:
        """Animation update handler for thumb position.
        
        Args:
            value (int): Current animation value (x-position offset)
        """
        self._thumb_position = value
        self.update()

    def toggle(self) -> None:
        """Inverts current switch state with animation."""
        self.setChecked(not self._checked)

    def setChecked(self, checked: bool) -> None:
        """Sets switch state with animated transition.
        
        Args:
            checked: New boolean state for the switch
            
        Emits:
            stateChanged: When state is different from current
        """
        if checked != self._checked:
            self._checked = checked
            target = 36 if checked else 4  # Position calculation
            self.animation.stop()
            self.animation.setStartValue(self._thumb_position)
            self.animation.setEndValue(target)
            self.animation.start()
            self.stateChanged.emit(self._checked)

    def isChecked(self) -> bool:
        """Gets current switch state.
        
        Returns:
            bool: True if switch is checked/active
        """
        return self._checked

    def paintEvent(self, event) -> None:
        """Custom painting of switch elements.
        
        Implements:
        - Rounded background with state-based color
        - Circular thumb with elevation effect
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        bg_color = QColor("#2ecc71" if self._checked else "#e0e0e0")
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 17, 17)
        
        # Thumb
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QPoint(int(self._thumb_position) + 14, 17), 12, 12)

    def mousePressEvent(self, event) -> None:
        """Handles mouse click events to toggle state."""
        self.toggle()
        super().mousePressEvent(event)