from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("NOT SILC")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # params panel, GB can't add widget
        self.buttonsPanel = QGroupBox("Initial params")
        self.layout.addWidget(self.buttonsPanel)
        self.buttonsLayout = QVBoxLayout()
        self.buttonsPanel.setLayout(self.buttonsLayout)

        # home button
        self.labelHome = QLabel("Set zero",self)
        self.buttonsLayout.addWidget(self.labelHome)
        self.buttonHome = QPushButton("Home", self)
        self.buttonsLayout.addWidget(self.buttonHome)

        # combo box ball size
        self.labelBallSize = QLabel("Tamaño bola", self)
        self.buttonsLayout.addWidget(self.labelBallSize)
        self.comboBoxBallSize = QComboBox()
        self.comboBoxBallSize.addItems(["Small", "Medium", "Large"])
        self.buttonsLayout.addWidget(self.comboBoxBallSize)

        # ball height
        self.labelBallHeight = QLabel("Altura bola", self)
        self.buttonsLayout.addWidget(self.labelBallHeight)
        self.buttonBallHeight = QPushButton("Medir altura", self)
        self.buttonsLayout.addWidget(self.buttonBallHeight)

        # distance 
        self.labelDistance = QLabel("Distancia bola-roca", self)
        self.buttonsLayout.addWidget(self.labelDistance)
        self.inputDistance = QLineEdit("", self)
        self.buttonsLayout.addWidget(self.inputDistance)

        # table
        self.table= QTabWidget()

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 4)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("log file \n ...") # aqui puee ir la consola?

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.table.addTab(tab1, "&Table")
        self.table.addTab(tab2, "Text &Edit")

        self.layout.addWidget(self.table, 0, 1)


