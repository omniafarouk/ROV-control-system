import pathlib

import cv2
from PyQt6.QtCore import QObject, QEvent, Qt

import Camera_State
import sys

from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget, QMessageBox

from FIleExplorerDialogue import FileDialogue
from New_View import NewViewGui
from CreateViewThread import Create_view


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.left_video_path = None
        self.right_video_path = None
        while self.left_video_path is None:
            self.left_video_path = self.Select_video_path("Left")
            if self.left_video_path is not None:
                try:
                    self.left_video_path = self.fix_video_path(self.left_video_path)
                    print(f"left path after pathlib is {self.left_video_path}")
                except Exception as e:
                    print(f"error occurred during fixing path {e}")
                    self.left_video_path = None
            else:
                print("repeat reading left video path")

        while self.right_video_path is None:
            self.right_video_path = self.Select_video_path("Right")
            if self.right_video_path is not None:
                try:
                    self.right_video_path = self.fix_video_path(self.right_video_path)
                    print(f"right path after pathlib is {self.right_video_path}")
                except Exception as e:
                    print(f"error occurred during fixing path{e}")
                    self.right_video_path = None
            else:
                print("repeat reading right video path")

        print("creating instance")
        # Create an instance of a QLabel class to show left view and its scroll bar
        self.left_view_gui = NewViewGui("Left View", Camera_State.CameraState.NORMAL)
        self.left_view_gui.label.installEventFilter(self)
        print(f"done{self.left_view_gui.label.objectName()}")

        print("creating right")
        # Create an instance of a QLabel class to show right view
        self.right_view_gui = NewViewGui("Right View", Camera_State.CameraState.NORMAL)
        self.right_view_gui.label.installEventFilter(self)
        print(f"done 2 {self.right_view_gui.label.objectName()}")

        # Create an instance of a QLabel class to show stitched view
        self.stitched_view_gui = NewViewGui("Stitched View", Camera_State.CameraState.NORMAL)
        self.stitched_view_gui.label.installEventFilter(self)

        # Set the UI elements for this Widget class.
        self.__SetupUI()

        print("starting left thread")
        # Create an instance of CaptureIpCameraFramesWorker.
        self.left_path_array = [self.left_video_path]
        self.Left_view_thread = Create_view(self.left_path_array, "Left View", self.left_view_gui)

        print("starting right thread")
        # Create an instance of CaptureIpCameraFramesWorker.
        self.right_path_array = [self.right_video_path]
        self.Right_view_thread = Create_view(self.right_path_array, "Right View", self.right_view_gui)

        # Create an instance of CaptureIpCameraFramesWorker.
        self.stitched_videos = [self.left_video_path, self.right_video_path]
        self.Stitched_view_thread = Create_view(self.stitched_videos, "Stitched View", self.stitched_view_gui)

        # Start the thread getIpCameraFrameWorker_1.
        print("starting thread 1")
        self.Left_view_thread.start()

        print("starting thread 2 ")
        # Start the thread getIpCameraFrameWorker_2.
        self.Right_view_thread.start()

        print("starting thread 3")
        # Start the thread getIpCameraFrameWorker_3.
        self.Stitched_view_thread.start()

    def Select_video_path(self, side):
        reply = QMessageBox.question(self, 'Select File',
                                     f'do you want to continue to select {side} Video Path?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            window = FileDialogue()
            video_path = FileDialogue().Open_File_dialogue()
            window.show()
            print(f"path before fixing is {video_path}")
            return video_path

        else:
            return None
    def handle_video_path(self, path_tuple):
        video_path, _ = path_tuple
        return pathlib.Path(video_path[0])

    def fix_video_path(self, video_path):
        new_path = self.handle_video_path(video_path)
        video_path_string = str(new_path)
        fixed_path = video_path_string.replace("/", "\\\\")
        return fixed_path

    def __SetupUI(self) -> None:
        # Create an instance of a QGridLayout layout.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(self.left_view_gui.QScrollArea, 0,0)
        grid_layout.addWidget(self.right_view_gui.QScrollArea, 0, 1)
        grid_layout.addWidget(self.stitched_view_gui.QScrollArea, 1, 0)

        # Create a widget instance.
        self.widget = QWidget(self)
        self.widget.setLayout(grid_layout)

        # Set the central widget.
        self.setCentralWidget(self.widget)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'black';}")
        # Set window title.
        self.setWindowTitle("Camera System")

    @QtCore.pyqtSlot()
    def Showview1(self, frame: QImage) -> None:
        self.left_view_gui.label.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def Showview2(self, frame: QImage) -> None:
        self.right_view_gui.label.setPixmap(QPixmap.fromImage(frame))

    @QtCore.pyqtSlot()
    def Showview3(self, frame: QImage) -> None:
        self.stitched_view_gui.label.setPixmap(QPixmap.fromImage(frame))

    # Override method for class MainWindow.

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QEvent.Type.MouseButtonDblClick:
            if source.objectName() == self.left_view_gui.name:
                print("in event 1")
                if self.left_view_gui.state == Camera_State.CameraState.NORMAL:
                    self.right_view_gui.QScrollArea.hide()
                    self.stitched_view_gui.QScrollArea.hide()
                    self.left_view_gui.state = Camera_State.CameraState.MAXIMIZED
                else:
                    self.right_view_gui.QScrollArea.show()
                    self.stitched_view_gui.QScrollArea.show()
                    self.left_view_gui.state = Camera_State.CameraState.NORMAL
            elif source.objectName() == self.right_view_gui.name:
                print("in event 2")
                if self.right_view_gui.state == Camera_State.CameraState.NORMAL:
                    self.left_view_gui.QScrollArea.hide()
                    self.stitched_view_gui.QScrollArea.hide()
                    self.right_view_gui.state = Camera_State.CameraState.MAXIMIZED
                else:
                    self.left_view_gui.QScrollArea.show()
                    self.stitched_view_gui.QScrollArea.show()
                    self.right_view_gui.state = Camera_State.CameraState.NORMAL
            elif source.objectName() == self.stitched_view_gui.name:
                #
                if self.stitched_view_gui.state == Camera_State.CameraState.NORMAL:
                    self.left_view_gui.QScrollArea.hide()
                    self.right_view_gui.QScrollArea.hide()
                    self.stitched_view_gui.state = Camera_State.CameraState.MAXIMIZED
                else:
                    self.left_view_gui.QScrollArea.show()
                    self.right_view_gui.QScrollArea.show()
                    self.stitched_view_gui.state = Camera_State.CameraState.NORMAL
            else:
                return super(MainWindow, self).eventFilter(source, event)
            return True
        else:
            return super(MainWindow, self).eventFilter(source, event)

    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, 'Exit Application',
                                     'Are you sure you want to exit?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Perform cleanup
            self.cleanup_resources()
            event.accept()  # Accept the event and close the window
        else:
            event.ignore()  # Ignore the close event, keep the application open
        event.accept()

    def cleanup_resources(self):
        # Stop all threads
        # If thread view1 is running, then exit it.
        if self.Left_view_thread.isRunning():
            self.Left_view_thread.ReleaseALlCaptures()
            self.Left_view_thread.quit()
        # If thread view2 is running, then exit it.
        if self.Right_view_thread.isRunning():
            self.Right_view_thread.ReleaseALlCaptures()
            self.Right_view_thread.quit()
        # If thread view3 is running, then exit it.
        if self.Stitched_view_thread.isRunning():
            self.Stitched_view_thread.ReleaseALlCaptures()
            self.Stitched_view_thread.quit()
        print("Resources have been cleaned up, and threads have been stopped.")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
