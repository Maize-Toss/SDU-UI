from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect
import math

class BatteryIndicator(QWidget):
    def __init__(self, battery_level=100, cbu=0):
        super().__init__()

        self.battery_level = battery_level
        self.cbu = cbu
        self.bars = 4

        self.setFixedSize(120, 60)  # Adjust the size for both the bars and label

    def set_battery_level(self, battery_level):
        if 0 <= battery_level <= 100:
            self.battery_level = battery_level
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw a box around the battery indicator
        border_rect = QRect(0, 20, self.width(), 20)
        painter.drawRect(border_rect)

        # Define colors for different battery levels
        if self.battery_level > 75:
            self.color = QColor(0, 255, 0)  # Green
            blocks = 4
        elif self.battery_level > 50:
            self.color = QColor(255, 255, 0)  # Yellow
            blocks = 3
        elif self.battery_level > 25:
            self.color = QColor(255, 165, 0)  # Orange
            blocks = 2
        else:
            self.color = QColor(255, 0, 0)  # Red
            blocks = 1

        painter.setBrush(self.color)

        # Calculate the width of each bar based on battery level
        bar_width = self.width() // self.bars

        # Draw battery bars
        for i in range(blocks):
            rect = QRect(self.width() - (i + 1) * bar_width, 20, bar_width, 20)
            painter.drawRect(rect)
    
