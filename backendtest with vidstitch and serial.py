from frontendtest import Ui_MainWindow as Ui_MainWindow_main
from MainCameraSystemGUI import MainWindow as CameraSystemMainWindow
from MainStereoVisionWindow import MyWidget
import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
from frontendManual import Ui_ManualControl
from autonomousfrontend import Ui_MainWindow as Ui_MainWindow_auto
import serial
import time
import serial.tools.list_ports


class WebCam(QDialog):
    def __init__(self):
         super().__init__()
         self.setWindowTitle('Web Camera')
         layout = QVBoxLayout()

         #Create and configure QLabel to display webcam feed
         self.videoLabel = QLabel("Press 'show' to show the live webcam!")
         self.videoLabel.setFixedSize(640, 480)  # Set size to match the webcam feed
         layout.addWidget(self.videoLabel)

         # Add "Show" button
         self.showButton = QPushButton("Show")
         self.showButton.clicked.connect(self.startCamera)
         layout.addWidget(self.showButton)

         # Add "Screenshot" button
         self.screenshotButton = QPushButton("Screenshot")
         self.screenshotButton.clicked.connect(self.takeScreenshot)
         layout.addWidget(self.screenshotButton)

         self.setLayout(layout)

         #Initialize video capture and timer
         self.cap = cv2.VideoCapture(0)
         self.timer = QTimer()
         self.timer.timeout.connect(self.updateframe)

    def startCamera(self):
         if not self.timer.isActive():
             self.timer.start(30)  # Update frame every 30 ms

    def updateframe(self):
         rval, frame = self.cap.read()
         if rval:
             rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
             h, w, ch = rgb_image.shape
             qimg = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
             pixmap = QPixmap.fromImage(qimg)
             self.videoLabel.setPixmap(pixmap)

    def takeScreenshot(self):
         if self.cap.isOpened():
             rval, frame = self.cap.read()
             if rval:
                 cv2.imwrite('screenshot.png', frame)

    def closeEvent(self, event):
         self.timer.stop()
         self.cap.release()
         event.accept()


class CarControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Car Control')
        layout = QVBoxLayout()

        # Setting up label
        self.label = QLabel("Car Control")
        layout.addWidget(self.label)

        # Creating and setting up buttons
        self.autonomousButton = QPushButton("Autonomous")
        layout.addWidget(self.autonomousButton)
        self.manualButton = QPushButton("Manual")
        layout.addWidget(self.manualButton)
        self.manualButton.clicked.connect(self.open_manual_control)
        self.autonomousButton.clicked.connect(self.open_autonomous_control)
        self.autonomousButton.clicked.connect(self.Auto_sent)
        self.autonomousButton.clicked.connect(self.update_data)
        self.setLayout(layout)

        self.connectSerial()

    def connectSerial(self):
        try:
            self.ArduinoSerial = serial.Serial('COM5', 9600)  # Adjust the port and baud rate as needed
            print("Serial connection established.")
        except serial.SerialException as e:
            print(f"Error connecting to serial port: {e}")

    def send_command(self, command):
        try:
            self.ArduinoSerial.write(command.encode())
            time.sleep(3)
        except Exception as e:
            print(f"Error sending command '{command}': {e}")

    def open_autonomous_control(self):
        self.autoWindow = QMainWindow()
        self.ui_auto = Ui_MainWindow_auto()
        self.ui_auto.setupUi(self.autoWindow)

    def update_data(self):
        try:
            if self.ArduinoSerial.in_waiting > 0:
                # Split data into id and value
                data_bytes = self.ArduinoSerial.readline()
                data = data_bytes.decode('utf-8')
                id, value = data.strip().split(':', 1)
                print(id)
                # Handle the data based on the id
                if id == 'distance_F':
                    self.ui_auto.forwardReading.setText(value)
                elif id == 'distance_R':
                    self.ui_auto.rightReading.setText(value)
                elif id == 'distance_L':
                    self.ui_auto.leftReading.setText(value)
                elif id == 'current':
                    self.ui_auto.currentReading.setText(value)
                elif id == 'voltage':
                    self.ui_auto.voltageReading.setText(value)
                else:
                    print(f"Unknown data id: {id}")
        except ValueError:
            print(f"Failed to parse data: {data}")

        self.autoWindow.show()

    def open_manual_control(self):
        # setting up manual window
        self.manual_window = QMainWindow()
        self.ui_manual = Ui_ManualControl()
        self.ui_manual.setupUi(self.manual_window)

        # connecting buttons to ide

        self.ui_manual.stopButton.clicked.connect(self.stop_button)
        self.ui_manual.frontButton.clicked.connect(self.front_button)
        self.ui_manual.backButton.clicked.connect(self.back_button)
        self.ui_manual.rightButton.clicked.connect(self.right_button)
        self.ui_manual.leftButton.clicked.connect(self.left_button)
        self.ui_manual.lowSpeed.clicked.connect(self.low_rad_button)
        self.ui_manual.mediumSpeed.clicked.connect(self.medium_rad_button)
        self.ui_manual.highSpeed.clicked.connect(self.high_rad_button)

        # showing manual window
        self.manual_window.show()

    # sending message to arduino

    def Auto_sent(self):
        for i in range(5):
            b = str(i)
            self.send_command('4')

    def upd(self):
        self.update_data()

    def stop_button(self):
        self.send_command('9')
    def front_button(self):
        self.send_command('5')
    def back_button(self):
        self.send_command('6')
    def right_button(self):
        self.send_command('7')
    def left_button(self):
        self.send_command('8')
    def low_rad_button(self):
        self.send_command('1')
    def medium_rad_button(self):
        self.send_command('2')
    def high_rad_button(self):
        self.send_command('3')

    def closeEvent(self, event):
        if hasattr(self, 'ArduinoSerial') and self.ArduinoSerial.is_open:
            self.ArduinoSerial.close()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_MainWindow_main()
        self.ui.setupUi(self)
        self.ui.carcontrolbutton.clicked.connect(self.show_new_window)
        self.ui.liveCamButton.clicked.connect(self.webCamDialogue)
        self.ui.videoStitchButton.clicked.connect(self.video_stitching)
        self.ui.stereoVisionButton.clicked.connect(self.stereo_vision)
    def show_new_window(self):
        self.w = CarControl()
        self.w.show()

    def video_stitching(self):
        self.w = CameraSystemMainWindow()
        self.w.show()
    def stereo_vision(self):
        self.w = MyWidget()
        self.w.show()

    def webCamDialogue(self):
        self.w = WebCam()
        self.w.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
