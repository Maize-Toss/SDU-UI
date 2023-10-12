import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CornholeGameUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cornhole Game")
        self.setGeometry(100, 100, 800, 400)

        # Create a horizontal layout for the main window
        layout = QHBoxLayout()

        # Create a vertical layout for each team's section
        layout_left = QVBoxLayout()
        layout_center = QVBoxLayout()
        layout_right = QVBoxLayout()

        # Create a button
        self.end_round_button = QPushButton("End Round")
        self.end_round_button.clicked.connect(self.end_round_button_clicked)

        # Create labels for displaying scores
        # self.team1_label = QLabel("Team 1")
        # self.team1_label.setAlignment(Qt.AlignCenter)
        # self.team1_label.setStyleSheet("font-size: 48px; color: red;")
        self.team1_score_label = QLabel("1")
        self.team1_score_label.setAlignment(Qt.AlignCenter)
        self.team1_score_label.setStyleSheet("font-size: 80px; color: red;")

        self.vs_label = QLabel("vs")
        self.vs_label.setAlignment(Qt.AlignCenter)
        self.vs_label.setStyleSheet("font-size: 48px; color: black;")

        # self.team2_label = QLabel("Team 2")
        # self.team2_label.setAlignment(Qt.AlignCenter)
        # self.team2_label.setStyleSheet("font-size: 48px; color: blue;")
        self.team2_score_label = QLabel("4")
        self.team2_score_label.setAlignment(Qt.AlignCenter)
        self.team2_score_label.setStyleSheet("font-size: 80px; color: blue;")

        # layout_left.addWidget(self.team1_label)
        layout_left.addWidget(self.team1_score_label)

        layout_center.addWidget(self.vs_label)
        # Add the button to the layout
        layout_center.addWidget(self.end_round_button)

        # layout_right.addWidget(self.team2_label)
        layout_right.addWidget(self.team2_score_label)

        # Add both team layouts to the main layout
        layout.addLayout(layout_left)

        layout.addLayout(layout_center)

        layout.addLayout(layout_right)

        # Create a central widget to hold the layouts
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add the bean bag widget to the main layout
        layout_left.addWidget(self.add_beanbags(1))
        layout_right.addWidget(self.add_beanbags(2))

    def add_beanbags(self, team):
        # Create a grid layout for the bean bags
        beanbag_widget = QWidget(self)
        beanbag_layout = QGridLayout(beanbag_widget)
        
        # Create and display the bean bag image
        if team == 1:
            beanbag_image = QPixmap("redbag.png")
        else:
            beanbag_image = QPixmap("bluebag.png")

        beanbag_image = beanbag_image.scaled(40, 40, Qt.KeepAspectRatio)
        for i in range(1):
            for j in range(4):
                beanbag_label = QLabel()
                beanbag_label.setPixmap(beanbag_image)
                beanbag_layout.addWidget(beanbag_label, i, j)

        # return bean bag widget
        return beanbag_widget

    def update_scores(self, team1_score, team2_score):
        self.team1_score_label.setText(str(team1_score))
        self.team2_score_label.setText(str(team2_score))
    
    def end_round_button_clicked(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Maize Toss")
        message_box.setText("End of Round")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()

def main():
    app = QApplication(sys.argv)
    game_ui = CornholeGameUI()
    game_ui.show()

    # Example: Update scores
    game_ui.update_scores(1, 4)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
