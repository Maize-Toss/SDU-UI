from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect

class BatteryIndicator(QWidget):
    def __init__(self, battery_level=100):
        super().__init__()

        self.battery_level = battery_level
        self.bars = 4

        self.setFixedSize(40, 80)

    def set_battery_level(self, battery_level):
        if 0 <= battery_level <= 100:
            self.battery_level = battery_level
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define colors for different battery levels
        if self.battery_level >= 75:
            color = QColor(0, 255, 0)  # Green
        elif self.battery_level >= 50:
            color = QColor(255, 255, 0)  # Yellow
        elif self.battery_level >= 25:
            color = QColor(255, 165, 0)  # Orange
        else:
            color = QColor(255, 0, 0)  # Red

        painter.setBrush(color)

        # Calculate the height of each bar based on battery level
        bar_height = self.height() // self.bars

        # Draw battery bars
        for i in range(self.bars - self.battery_level // 25):
            rect = QRect(10, i * bar_height, 20, bar_height)
            painter.drawRect(rect)
