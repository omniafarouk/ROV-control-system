import sys

import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

from Calibration import calibration
from DepthComputation import depthComputation
from Disparity import disparity
from Rectification import rectification


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.choice = None
        self.setWindowTitle("Choose Data Set")
        self.setGeometry(300, 200, 400, 200)

        button1 = QPushButton("DataSet 1")
        button1.clicked.connect(self.button1_clicked)

        button2 = QPushButton("Dataset 2")
        button2.clicked.connect(self.button2_clicked)

        button3 = QPushButton("Dataset 3")
        button3.clicked.connect(self.button3_clicked)

        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        self.setLayout(layout)
        self.show()

    def button1_clicked(self):
        cam1 = np.array([[4396.869, 0, 1353.072],
                         [0, 4396.869, 989.702],
                         [0, 0, 1]])

        cam2 = np.array([[4396.869, 0, 1538.86],
                         [0, 4396.869, 989.702],
                         [0, 0, 1]])
        left_image = "./excess/im0_0.png"
        right_image = "./excess/im0_1.png"
        vmin = 17
        vmax = 619
        baseline = 144.094
        ndisp = 176
        self.start_program(left_image, right_image, cam1, cam2, vmin, vmax, baseline, ndisp)

    def button2_clicked(self):
        cam1 = np.array([[4396.869, 0, 1353.072],
                         [0, 4396.869, 989.702],
                         [0, 0, 1]])

        cam2 = np.array([[4396.869, 0, 1538.86],
                         [0, 4396.869, 989.702],
                         [0, 0, 1]])
        left_image = "./excess/im1_0.png"
        right_image = "./excess/im1_1.png"
        vmin = 17
        vmax = 619
        baseline = 144.049
        ndisp = 640
        self.start_program(left_image, right_image, cam1, cam2, vmin, vmax, baseline, ndisp)

    def button3_clicked(self):
        cam1 = np.array([[5299.313, 0, 1263.818],
                         [0, 5299.313, 977.763],
                         [0, 0, 1]])

        cam2 = np.array([[5299.313, 0, 1438.004],
                         [0, 5299.313, 977.763],
                         [0, 0, 1]])

        left_image = "./excess/im2_0.png"
        right_image = "./excess/im2_1.png"
        vmin = 54
        vmax = 147
        baseline = 177.288
        ndisp = 250
        self.start_program(left_image, right_image, cam1, cam2, vmin, vmax, baseline, ndisp)

    def start_program(self, left_image_path, right_image_path, Cam1, Cam2, vmin, vmax, baseline, ndisp):
        left_image = cv2.imread(left_image_path)
        right_image = cv2.imread(right_image_path)
        self.hide()
        calibrate = calibration(left_image, right_image, Cam1, Cam2)
        calibrate.create()
        rectify = rectification(calibrate)
        rectify.create()
        disparity_process = disparity(vmin, vmax, ndisp, rectify)
        disparity_process.create()
        depth_computing_proccess = depthComputation(disparity_process, Cam1, baseline)
        # depth_computing_proccess.create()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
