from PyQt6.QtWidgets import QLabel, QScrollArea


class NewViewGui:
    def __init__(self, name, state):
        self.QScrollArea = None
        self.name = name
        self.state = state
        self.label = QLabel()
        self.label.setScaledContents(True)
        self.label.setObjectName(name)
        self.createScrollBar()

    def createScrollBar(self):
        self.QScrollArea = QScrollArea()
        self.QScrollArea.setWidgetResizable(True)
        self.QScrollArea.setWidget(self.label)
