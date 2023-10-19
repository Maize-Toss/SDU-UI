import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
import json 
import serial

class CornholeGameUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Serial object for /dev/rfcomm0
        # self.ser = serial.Serial('/dev/rfcomm0', 9600)  # Adjust the baud rate as needed

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
        # self.end_round_button.setMinimumSize(100,100)
        # button_font = self.end_round_button.font()
        # button_font.setPointSize(18)  # Set the font size (adjust as needed)
        # self.end_round_button.setFont(button_font)
        self.enlarge_component(self.end_round_button)
        self.end_round_button.clicked.connect(self.end_round_button_clicked)

        # Create a horizontal layout for Team 1's buttons
        layout_team1_buttons = QHBoxLayout()
        self.team1_increment_button = QPushButton("+")
        self.team1_decrement_button = QPushButton("-")
        self.team1_increment_button.clicked.connect(lambda: self.update_score(1, 1))
        self.team1_decrement_button.clicked.connect(lambda: self.update_score(1, -1))
        layout_team1_buttons.addWidget(self.team1_decrement_button)
        layout_team1_buttons.addWidget(self.team1_increment_button)
        self.enlarge_component(self.team1_increment_button)
        self.enlarge_component(self.team1_decrement_button)

        # Create a horizontal layout for Team 2's buttons
        layout_team2_buttons = QHBoxLayout()
        self.team2_increment_button = QPushButton("+")
        self.team2_decrement_button = QPushButton("-")
        self.team2_increment_button.clicked.connect(lambda: self.update_score(2, 1))
        self.team2_decrement_button.clicked.connect(lambda: self.update_score(2, -1))
        layout_team2_buttons.addWidget(self.team2_decrement_button)
        layout_team2_buttons.addWidget(self.team2_increment_button)
        self.enlarge_component(self.team2_increment_button)
        self.enlarge_component(self.team2_decrement_button)


        # Create labels for displaying scores
        # self.team1_label = QLabel("Team 1")
        # self.team1_label.setAlignment(Qt.AlignCenter)
        # self.team1_label.setStyleSheet("font-size: 48px; color: red;")
        self.team1_score_label = QLabel("0")
        self.team1_score_label.setAlignment(Qt.AlignCenter)
        self.team1_score_label.setStyleSheet("font-size: 200px; color: red;")

        self.vs_label = QLabel("vs")
        self.vs_label.setAlignment(Qt.AlignCenter)
        self.vs_label.setStyleSheet("font-size: 100px; color: black;")

        # self.team2_label = QLabel("Team 2")
        # self.team2_label.setAlignment(Qt.AlignCenter)
        # self.team2_label.setStyleSheet("font-size: 48px; color: blue;")
        self.team2_score_label = QLabel("0")
        self.team2_score_label.setAlignment(Qt.AlignCenter)
        self.team2_score_label.setStyleSheet("font-size: 200px; color: blue;")

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

        # Add the button layouts for Team 1 and Team 2 to the main layout
        layout_left.addLayout(layout_team1_buttons)
        layout_right.addLayout(layout_team2_buttons)

    def add_beanbags(self, team):
        # Create a grid layout for the bean bags
        beanbag_widget = QWidget(self)
        beanbag_layout = QGridLayout(beanbag_widget)
        
        # Create and display the bean bag image
        if team == 1:
            beanbag_image = QPixmap("redbag.png")
        else:
            beanbag_image = QPixmap("bluebag.png")

        beanbag_image = beanbag_image.scaled(80, 80, Qt.KeepAspectRatio)
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

    def send_state(self, cbu):
        uiState = self.get_ui_state(True)
        json_object = json.dumps(uiState, indent = 4)  
        self.write_to_rfcomm(json_object, cbu)
    
    def end_round_button_clicked(self):
        QSound.play("bowling_strike.wav")  # Replace "audio.wav" with the path to your sound file

        # message_box = QMessageBox()
        # message_box.setWindowTitle("Maize Toss")
        # message_box.setText("End of Round")
        # message_box.setIcon(QMessageBox.Information)
        # message_box.exec_()
        self.send_state(2)

    def update_score(self, team, value):
        if team == 1:
            current_score = int(self.team1_score_label.text())
            new_score = current_score + value
            if (new_score < 0):
                new_score = 0
            self.team1_score_label.setText(str(new_score))
        elif team == 2:
            current_score = int(self.team2_score_label.text())
            new_score = current_score + value
            if (new_score < 0):
                new_score = 0
            self.team2_score_label.setText(str(new_score))

        self.send_state(2)

    def enlarge_component(self, button):
        button.setMinimumSize(100,50)
        button_font = button.font()
        button_font.setPointSize(18)  # Set the font size (adjust as needed)
        button.setFont(button_font)

    def get_ui_state(self, end_of_round):
        # get ui state and compress it into json
        dict = []
        dict["team1"]["score"] =  int(self.team1_score_label.text())
        dict["team1"]["state"] = 0

        dict["team2"]["score"] =  int(self.team2_score_label.text())
        dict["team2"]["state"] = 0

        dict["end_of_round"] = end_of_round

        return dict
    
    def write_to_rfcomm(self, data, cbu):
        # send data over bluetooth
        if cbu == 0 or cbu == 2:
            with open("/dev/rfcomm0") as bt:
                bt.write(data)
        elif cbu == 1 or cbu == 2:
            with open("dev/rfcomm1") as bt:
                bt.write(data)
        else:
            print("Device not recognized")

        print("Data sent successfully.")

def main():
    app = QApplication(sys.argv)
    game_ui = CornholeGameUI()
    game_ui.show()

    # Example: Update scores
    game_ui.update_scores(0, 0)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
