from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("NOT SILC")

        self.layout = QVBoxLayout()
        self.label = QLabel("Hola Mundito",self)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
