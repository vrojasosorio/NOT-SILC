from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import random

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.iterations = 0
        self.validationDetails = ""
        self.validation = False
        self.setupUI()
        self.clicks()
    
    def setupUI(self):
        self.setWindowTitle("NOT SILC")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # experiment info
        self.descriptionPanel = QGroupBox("Description")
        self.descriptionPanel.setFixedSize(200,150)
        self.layout.addWidget(self.descriptionPanel)
        self.descriptionLayout = QGridLayout()
        self.descriptionPanel.setLayout(self.descriptionLayout)

        # params panel, GB can't add widget
        self.buttonsPanel = QGroupBox("Initial params")
        self.buttonsPanel.setFixedSize(200,350)
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
        self.labelOrigin = QLabel("Origen de la muestra", self)
        self.descriptionLayout.addWidget(self.labelOrigin) 
        self.inputOrigin = QLineEdit("", self)
        self.descriptionLayout.addWidget(self.inputOrigin) 

        # tipo de muestra
        self.labelSampleType = QLabel("Tipo de la muestra", self)
        self.descriptionLayout.addWidget(self.labelSampleType) 
        self.inputSampleType = QLineEdit("", self)
        self.descriptionLayout.addWidget(self.inputSampleType) 

        # iterations
        self.labelIterations = QLabel("Número de repeticiones", self)
        self.buttonsLayout.addWidget(self.labelIterations) 
        self.inputIterations = QLineEdit("", self)
        self.buttonsLayout.addWidget(self.inputIterations) 

        # home button
        self.labelHome = QLabel("Set zero",self)
        self.buttonsLayout.addWidget(self.labelHome)
        self.buttonHome = QPushButton("Home", self)
        self.buttonsLayout.addWidget(self.buttonHome)

        # ball size
        self.labelBallSize = QLabel("Tamaño bola", self)
        self.buttonsLayout.addWidget(self.labelBallSize)
        self.comboBoxBallSize = QComboBox()
        self.comboBoxBallSize.addItems(["","Small", "Medium", "Large"])
        self.buttonsLayout.addWidget(self.comboBoxBallSize)

        # rock height
        self.labelRockHeight = QLabel("Altura rock", self)
        self.buttonsLayout.addWidget(self.labelRockHeight)
        self.buttonRockHeight = QPushButton("Medir altura", self)
        self.buttonsLayout.addWidget(self.buttonRockHeight)
        self.labelHeightValue = QLabel("", self)
        self.buttonsLayout.addWidget(self.labelHeightValue)
        
        # distance 
        self.labelDistance = QLabel("Distancia bola-roca", self)
        self.buttonsLayout.addWidget(self.labelDistance)
        self.inputDistance = QLineEdit("", self)
        self.buttonsLayout.addWidget(self.inputDistance)

        # confirm
        self.buttonConfirm= QPushButton("Confirm", self)
        self.controlLayout.addWidget(self.buttonConfirm, 0, 0)
        #self.buttonConfirm.setEnabled(False)

        # launch
        self.buttonLaunch= QPushButton("Launch", self)
        self.controlLayout.addWidget(self.buttonLaunch, 0, 1)
        self.buttonLaunch.setEnabled(False)

        # save
        self.buttonSave = QPushButton("Save", self)
        self.controlLayout.addWidget(self.buttonSave, 1, 0)
        self.buttonSave.setEnabled(False)

        # Finish
        self.buttonFinish = QPushButton("Finish", self)
        self.controlLayout.addWidget(self.buttonFinish, 1, 1)
        self.buttonFinish.setEnabled(False)

        # table
        self.table= QTabWidget()

        tab1 = QWidget()
        self.tableWidget = QTableWidget(0, 4)
        columns = ["Ball size", "Rock size", "Distance", "Data"]
        self.tableWidget.setHorizontalHeaderLabels(columns)

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
        self.table.setFixedSize(415,450)

        self.layout.addWidget(self.table, 0, 1, 2, 1)
    
    def loadData(self):
        if self.inputIterations.text() == "":
            self.inputIterations.setText("1")

        if  self.iterations < int(self.inputIterations.text()): 
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(self.comboBoxBallSize.currentText()))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(self.labelHeightValue.text()))
            self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(self.inputDistance.text()))
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(str(round(random.random(),5)))) #hash distintivo x exp
            self.iterations += 1
        
    def onMedirAltura(self):
        self.labelHeightValue.setText(str(round(random.random(),3)))

    def actionButtonLaunch(self):
        # aki tiene q pasar toda la accion con el arduino 
        # en resumen: soltar la bola 
        # recibe un feedback del arduino q el experimento salió bien y permite "savearlo"
        self.buttonSave.setEnabled(True)


    def clicks(self):
        self.buttonSave.clicked.connect(self.loadData)
        self.buttonRockHeight.clicked.connect(self.onMedirAltura)
        self.buttonConfirm.clicked.connect(self.validate)
        self.buttonLaunch.clicked.connect(self.actionButtonLaunch)

    def checkBallSize(self):
        if self.comboBoxBallSize.currentText() == "":
            self.validation = False
            self.validationDetails += "Seleccionar tamaño bola \n"
    
    def checkRockHeight(self):
        if self.labelHeightValue.text() == "":
            self.validation = False
            self.validationDetails += "Medir altura \n"
    
    def checkInputDistance(self):
        pass # revisar que los caracteres sean soolo numeros y no otras cosas

    def checkHeightValue(self):
        return self.labelHeightValue != ""
             

    def disablePanel(self):
        self.inputIterations.setEnabled(False)
        self.buttonHome.setEnabled(False)
        self.comboBoxBallSize.setEnabled(False)
        self.buttonRockHeight.setEnabled(False)
        self.inputDistance.setEnabled(False)

    def validate(self):
        self.validation = True
        self.checkRockHeight()
        self.checkBallSize()
        
        if self.validation == True:
            self.buttonConfirm.setEnabled(False)
            self.disablePanel()
            self.buttonLaunch.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This is a message box")
            msg.setInformativeText("This is additional information")
            msg.setWindowTitle("MessageBox demo")
            msg.setDetailedText(self.validationDetails)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()





