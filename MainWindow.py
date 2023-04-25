from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.iterations = 0
        self.validationDetails = ""
        self.validation = False
 
        self.setupUI()
    
    def setupUI(self):
        self.setWindowTitle("NOT SILC")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # experiment info
        self.descriptionPanel = QGroupBox("Description")
        self.descriptionPanel.setFixedSize(200,225)
        self.layout.addWidget(self.descriptionPanel)
        self.descriptionLayout = QGridLayout()
        self.descriptionPanel.setLayout(self.descriptionLayout)

        # params panel, GB can't add widget
        self.buttonsPanel = QGroupBox("Initial parameters")
        self.buttonsPanel.setFixedSize(200,210)
        self.layout.addWidget(self.buttonsPanel)
        self.buttonsLayout = QGridLayout()
        self.buttonsPanel.setLayout(self.buttonsLayout)


        # control panel
        self.controlPanel = QGroupBox("Control of experiments")
        self.controlPanel.setFixedSize(200,100)
        self.layout.addWidget(self.controlPanel)
        self.controlLayout = QGridLayout()
        self.controlPanel.setLayout(self.controlLayout)

        # origin
        self.labelOrigin = QLabel("Sample's origin", self)
        self.descriptionLayout.addWidget(self.labelOrigin, 0, 0, 1, 2) 
        self.inputOrigin = QLineEdit("", self)
        self.descriptionLayout.addWidget(self.inputOrigin, 1, 0, 1, 2) 

        # tipo de muestra
        self.labelType = QLabel("Type of sample", self)
        self.descriptionLayout.addWidget(self.labelType, 2, 0, 1, 2) 
        self.inputType = QLineEdit("", self)
        self.descriptionLayout.addWidget(self.inputType, 3, 0, 1, 2) 

        # ball size
        self.labelBallSize = QLabel("Size of ball", self)
        self.descriptionLayout.addWidget(self.labelBallSize, 4, 0, 1, 2)
        self.comboBoxBallSize = QComboBox()
        self.comboBoxBallSize.addItems(["","Small", "Medium", "Large"])
        self.descriptionLayout.addWidget(self.comboBoxBallSize, 5, 0, 1, 2)

        # description buttons
        self.buttonConfirm = QPushButton("Confirm", self)
        self.descriptionLayout.addWidget(self.buttonConfirm, 6, 0)

        self.buttonEdit = QPushButton("Edit", self)
        self.descriptionLayout.addWidget(self.buttonEdit, 6, 1) 

        # chupa buttons
        self.labelHome = QLabel("Chupa ACTIONS XD",self)
        self.buttonsLayout.addWidget(self.labelHome)
        self.buttonLoad = QPushButton("Load ball", self)
        self.buttonsLayout.addWidget(self.buttonLoad)
       
        # set distance 
        self.labelDistance = QLabel("Release Height", self)
        self.buttonsLayout.addWidget(self.labelDistance)
        self.inputDistance = QLineEdit("", self)
        self.buttonsLayout.addWidget(self.inputDistance)
        self.inputDistance.setEnabled(False)

        # adjust distance
        self.buttonAdjustDist = QPushButton("Set distance", self)
        self.buttonsLayout.addWidget(self.buttonAdjust)
        self.buttonAdjustDist.setEnabled(False)

        # confirm
        self.buttonReset= QPushButton("RESET", self)
        self.controlLayout.addWidget(self.buttonReset, 0, 0)

        # launch
        self.buttonLaunch= QPushButton("LAUNCH", self)
        self.controlLayout.addWidget(self.buttonLaunch, 0, 1)
        #self.buttonLaunch.setEnabled(False)

        # Finish
        self.buttonFinish = QPushButton("Finish", self)
        self.controlLayout.addWidget(self.buttonFinish, 1, 0, 1, 2)
        self.buttonFinish.setEnabled(True)

        # table
        self.table= QTabWidget()

        tab1 = QWidget()
        self.tableWidget = QTableWidget(0, 4)
        columns = ["Ball size", "Rock size", "Distance", "Register"]
        self.tableWidget.setHorizontalHeaderLabels(columns)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)       
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("log file \n ...") # aqui puee ir la consola?

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.table.addTab(tab1, "&Table")
        self.table.addTab(tab2, "&Console")
        self.table.setFixedSize(500,525)

        self.layout.addWidget(self.table, 0, 1, 3, 1)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())








