from PyQt6.QtCore import Qt, QVariantAnimation, QPoint, pyqtSignal, QEasingCurve
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget

class Switch(QWidget):
    stateChanged = pyqtSignal(bool)  

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(70, 34)
        self._checked = False
        self._thumb_position = 4
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.animation = QVariantAnimation(self)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value):
        self._thumb_position = value
        self.update()

    def toggle(self):
        self.setChecked(not self._checked)

    def setChecked(self, checked):
        if checked != self._checked:
            self._checked = checked
            target = 36 if checked else 4
            self.animation.stop()
            self.animation.setStartValue(self._thumb_position)
            self.animation.setEndValue(target)
            self.animation.start()
            self.stateChanged.emit(self._checked)  # 👈 Emitir señal

    def isChecked(self):
        return self._checked

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bg_color = QColor("#2ecc71" if self._checked else "#e0e0e0")
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 17, 17)
        
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QPoint(int(self._thumb_position) + 14, 17), 12, 12)

    def mousePressEvent(self, event):
        self.toggle()
        super().mousePressEvent(event)
