import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSound
import json 
import serial
import threading
import subprocess
import time
import select
import battery as bat

class CornholeGameUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the list of files in the folder
        files = os.listdir('/home/sdu/git/SDU-UI/audio/')
        # Get the number of files
        self.sound_files = files
        self.num_soundtracks = len(files)
        self.sound_index = 0

        print(self.sound_files)
        print(self.num_soundtracks)
        print(self.sound_index)

        # Create a Serial object for /dev/rfcomm0
        self.ser0 = serial.Serial('/dev/rfcomm0', 9600)  # Adjust the baud rate as needed
        self.ser1 = serial.Serial('/dev/rfcomm1', 9600)  # Adjust the baud rate as needed

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
        self.team1_score_label = QLabel("0")
        self.team1_score_label.setAlignment(Qt.AlignCenter)
        self.team1_score_label.setStyleSheet("font-size: 200px; color: red;")

        # Create labels for displaying battery levels
        self.battery_cbu0 = QLabel("Battery 0: 100%")
        self.battery_cbu1 = QLabel("Battery 1: 100%")

        # Set the alignment and styles for battery labels
        self.battery_cbu0.setAlignment(Qt.AlignCenter)
        self.battery_cbu0.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.battery_cbu1.setAlignment(Qt.AlignCenter)
        self.battery_cbu1.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")

        self.battery_widget0 = bat.BatteryIndicator(battery_level=100, cbu=0)
        self.battery_widget1 = bat.BatteryIndicator(battery_level=100, cbu=1)
        # layout.addWidget(battery_widget)

        self.vs_label = QLabel("vs")
        self.vs_label.setAlignment(Qt.AlignCenter)
        self.vs_label.setStyleSheet("font-size: 100px; color: black;")

        self.team2_score_label = QLabel("0")
        self.team2_score_label.setAlignment(Qt.AlignCenter)
        self.team2_score_label.setStyleSheet("font-size: 200px; color: blue;")

        # layout_left.addWidget(self.team1_label)
        layout_left.addWidget(self.team1_score_label)

        # Add the battery labels to the central layout above the "vs" label
        layout_center.addWidget(self.battery_cbu0)
        layout_center.addWidget(self.battery_widget0, alignment=Qt.AlignCenter)
        layout_center.addWidget(self.battery_cbu1)
        layout_center.addWidget(self.battery_widget1, alignment=Qt.AlignCenter)

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

        self.stop_event = threading.Event()

        self.monitor_thread0 = threading.Thread(target=self.listen_bluetooth0)
        self.monitor_thread1 = threading.Thread(target=self.listen_bluetooth1)

        self.monitor_thread0.start()
        self.monitor_thread1.start()

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            self.stop_event.set()

            self.monitor_thread0.join()
            self.monitor_thread1.join()
            
            event.accept()
        else:
            event.ignore()

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
    
    def update_battery_level(self, cbu_id, battery_level):
        print("update battery " + str(cbu_id) + " to " + str(battery_level))
        # color = ""
        # if battery_level >= 70:
        #     color = "green"
        # elif battery_level < 70 and battery_level > 20:
        #     color = "orange"
        # else:
        #     color = "red"

        # print(color)

        if cbu_id == 0:
            self.battery_widget0.set_battery_level(float(battery_level))
            self.battery_cbu0.setText(f"Battery 0: {battery_level}%")
        elif cbu_id == 1:
            self.battery_widget1.set_battery_level(float(battery_level))
            self.battery_cbu1.setText(f"Battery 1: {battery_level}%")

        return 0
    
    def update_display_state(self, data, cbu_id):
            battery_level = float(data["battery"]) 
            team1d = int(data["team1d"])
            team2d = int(data["team2d"]) 

            print("STATE: ")
            print(battery_level)
            print(team1d)
            print(team2d)

            # check input
            assert (team1d >= 0 or team2d >= 0)

            # compute delta
            diff = abs(team1d - team2d)
            # update the state for highest scoring team
            if team1d > team2d:
                new_score = int(self.team1_score_label.text()) + diff
                self.team1_score_label.setText(str(new_score))
            elif team2d > team1d:
                new_score = int(self.team2_score_label.text()) + diff
                self.team2_score_label.setText(str(new_score))

            # update battery level
            self.update_battery_level(cbu_id, battery_level)

    # Function to call when /dev/rfcomm0 is written
    def listen_bluetooth0(self):
        print("listener 0 started...")

        while not self.stop_event.is_set():
            # try:
            while self.ser0.in_waiting:
                result = self.ser0.readline().decode('utf-8').replace('\x00', '').strip()
                print("Original data:", repr(result))
                print("String length:", len(result))
                try:
                    data = json.loads(result)
                    self.update_display_state(data, 0)
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", e)
                    print("Original data:", result)
                except Exception as e:
                    print("Exception:", e)
            # except Exception as e:
            #     print("Serial port error:", e)
            return

    # Function to call when /dev/rfcomm1 is written
    def listen_bluetooth1(self):
        print("listener 1 started...")
        # try:
        while not self.stop_event.is_set():
            while self.ser1.in_waiting:
                result = self.ser1.readline().decode('utf-8').replace('\x00', '').strip()
                print("Original data:", repr(result))
                print("String length:", len(result))
                try:
                    data = json.loads(result)
                    self.update_display_state(data, 1)
                except json.JSONDecodeError as e:
                    print("JSON decoding error:", e)
                    print("Original data:", result)
                except Exception as e:
                    print("Exception:", e)
        # except Exception as e:
        #     print("Serial port error:", e)


    def update_scores(self, team1_score, team2_score):
        self.team1_score_label.setText(str(team1_score))
        self.team2_score_label.setText(str(team2_score))

    def send_state(self, cbu, end_round):
        uiState = self.get_ui_state(end_round)
        json_object = json.dumps(uiState, indent = 4)  
        self.write_to_rfcomm(json_object, cbu)
    
    def get_filename(self, index):
        if index >= self.num_soundtracks:
            index = 0

        filename = self.sound_files[index]
        self.sound_index = index + 1 

        return "./audio/" + filename
    
    def end_round_button_clicked(self):
                # Soundtrack tracker
        filename = self.get_filename(self.sound_index)
        QSound.play(filename)  # Replace "audio.wav" with the path to your sound file

        # message_box = QMessageBox()
        # message_box.setWindowTitle("Maize Toss")
        # message_box.setText("End of Round")
        # message_box.setIcon(QMessageBox.Information)
        # message_box.exec_()
        time.sleep(11)

        # Create a new thread and pass the function and its arguments
        send_thread = threading.Thread(target=self.send_state, args=(2, True))
        # Start the thread to execute the send function
        send_thread.start()

    def update_score(self, team, value):
        send_val = False # used for debugging
        if team == 1:
            current_score = int(self.team1_score_label.text())
            new_score = current_score + value
            if (new_score < 0):
                new_score = 0
                send_val = False
            self.team1_score_label.setText(str(new_score))
        elif team == 2:
            current_score = int(self.team2_score_label.text())
            new_score = current_score + value
            if (new_score < 0):
                new_score = 0
                send_val = False
            self.team2_score_label.setText(str(new_score))
        
        if send_val:
            # Create a new thread and pass the function and its arguments
            send_thread = threading.Thread(target=self.send_state, args=(2, False))
            # Start the thread to execute the send function
            send_thread.start()

    def enlarge_component(self, button):
        button.setMinimumSize(100,50)
        button_font = button.font()
        button_font.setPointSize(18)  # Set the font size (adjust as needed)
        button.setFont(button_font)

    def get_ui_state(self, end_of_round):
        # get ui state and compress it into json
        data = {
            "team1": {
                "score": int(self.team1_score_label.text()),
                "state": 0
            },
            "team2": {
                "score": int(self.team2_score_label.text()),
                "state": 0
            },
            "end_of_round": end_of_round
        }
        return data
    
    def pad_packet(self, send_data):
        msg_len = len(send_data)
        padding = 256 - msg_len

        return send_data + " "*padding
    
    def write_to_rfcomm(self, data, cbu):
        # send data over bluetooth
        print("Sending data:")
        send_data = self.pad_packet(data)

        if cbu == 0 or cbu == 2:
            print("to cbu 0")
            print(len(send_data))
            with open("/dev/rfcomm0",'w') as bt:
                bt.write(send_data)

        if cbu == 1 or cbu == 2:
            print("to cbu 1")
            with open("/dev/rfcomm1",'w') as bt:
                bt.write(send_data)

        if cbu > 2 and cbu < 0:
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
