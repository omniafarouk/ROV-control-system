import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QTextEdit


class FileDialogue(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 400, 100)
        self.setWindowTitle("Select Video File")
        self.button = QPushButton('Select File', self)
        self.button.clicked.connect(self.Open_File_dialogue)

        self.fileNameTextBar = QTextEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.fileNameTextBar)
        self.setLayout(self.layout)

    def Open_File_dialogue(self):
        file_filter = 'Video File (*.mp4 *.avi *.mov);; All Files (*)'
        self.response = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select file(s)',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Video File (*.mp4 *.avi *.mov)'
        )
        self.fileNameTextBar.setText(str(self.response))
        return self.response


