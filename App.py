# Dependencies
from MainWindow import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from MotorCommand import MotorCommand
from vars import *

from re import sub
from struct import *

import random
import datetime
import serial

class Worker(QObject):
    finished = pyqtSignal()
    response = pyqtSignal()
    bufferUpdated = pyqtSignal(tuple)

    def __init__(self):
        self.arduino = serial.Serial('/dev/ttyACM0', 9600)
        self.machine = MotorCommand()
        
        # estructura del mensaje
        self.struct_fmt = '<Bh'
        self.struct_len = calcsize(self.struct_fmt)
    
    def work(self):
        try:
            if self.arduino.inWaiting():
                msg = self.arduino.read(self.struct_len)
                #print(msg.decode())
                if len(msg) != 0:
                    rxCom = unpack(self.struct_fmt, msg)
                    self.bufferUpdated.emit(rxCom)
                    #print(type(rxCom))

        except Exception as e:
            print(e)

class App(QApplication):
    # constructor
    def __init__(self, *args):
        QApplication.__init__(self, *args)

        # main objects 
        #self.main = None
        self.worker = Worker()

        # main window
        self.main = MainWindow(self)
        self.configureWidgetsActions()

        # status 
        self.isExperimentRunning = False
        self.isAtZero = False
        self.isMoving = False
    
        self.main.show()
    
    def sendCMD(self, id_actuador, cmd):
        pass
    
    def configureWidgetsActions(self):
        self.main.buttonHome.clicked.connect(self.actionHomeButton)
        self.main.comboBoxBallSize.currentIndexChanged.connect(self.actionBallSizeBox)
        self.main.buttonRockHeight.clicked.connect(self.actionBallHeightButton)

        self.main.buttonConfirm.clicked.connect(self.actionConfirmButton)
        self.main.buttonLaunch.clicked.connect(self.actionLaunchButton)
        self.main.buttonSave.clicked.connect(self.actionSaveButton)
        self.main.buttonFinish.clicked.connect(self.actionFinishButton)

    def move(self):
        pass
    
    def brake(self):
        pass
    
    def actionHomeButton(self):
        self.sendCMD(M1, SET_AT_ZERO)
        self.main.buttonHome.setEnabled(False)

    # dato muestra
    def actionBallSizeBox(self):
        pass

    # adjust distance between ball and rock
    def actionBallHeightButton(self):
        self.sendCMD(M2, MEASURE_DISTANCE)
        self.sendCMD(M2,SET_DISTANCE)

    # confirm experiments data
    def actionConfirmButton(self):
        self.disablePanel()

    # drop ball
    def actionLaunchButton(self):
        self.main.buttonLaunch.setEnabled(False)
        self.sendCMD(M1, DROP_BALL)
        
    def actionSaveButton(self):
        pass

    def actionFinishButton(self):
        # llamada a función q exporta un csv
        pass

    # llamada al worker
    def serialHandler(self):
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.response.connect(self.arduinoStatus)
        self.thread.start()
    
    def arduinoStatus(self, response):
        if response == 0:
            return
        else:
            return


    def transformText(self, text):
        text = sub(r"(_|-)+.", " ", text).title().replace(" ", "")
        return "".join([text[0].lower(), text[1:]])
    
    def transformDate(self):
        now = datetime.datetime.now()
        return now.strftime("%Y%m%d%H%M%S")

    def experimentNaming(self):
        sampleOrigin = self.transformText(self.main.inputOrigin.text())
        sampleType = self.transformText(self.main.inputType.text())
        sampleDate = self.transformDate()
        return sampleDate + "_" + sampleOrigin + "_" + sampleType

    def loadData(self):
        if self.main.inputIterations.text() == "":
            self.main.inputIterations.setText("1")

        if  self.main.iterations < int(self.main.inputIterations.text()): 
            rowPosition = self.main.tableWidget.rowCount()
            self.main.tableWidget.insertRow(rowPosition)

            self.main.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(self.main.comboBoxBallSize.currentText()))
            self.main.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(self.main.labelHeightValue.text()))
            self.main.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(self.main.inputDistance.text()))
            self.main.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(self.experimentNaming())) #hash distintivo x exp
            self.main.iterations += 1
        
    def onMedirAltura(self):
        self.main.labelHeightValue.setText(str(round(random.random(),3)))

    def actionButtonLaunch(self):
        # aki tiene q pasar toda la accion con el arduino 
        # en resumen: soltar la bola 
        # recibe un feedback del arduino q el experimento salió bien y permite "savearlo"
        pass


    def checkBallSize(self):
        if self.main.comboBoxBallSize.currentText() == "":
            self.validation = False
            self.validationDetails += "Seleccionar tamaño bola \n"
    
    def checkRockHeight(self):
        if self.main.labelHeightValue.text() == "":
            self.validation = False
            self.validationDetails += "Medir altura \n"
    
    def checkInputDistance(self):
        pass # revisar que los caracteres sean soolo numeros y no otras cosas

    def disablePanel(self):
        self.main.inputIterations.setEnabled(False)
        self.main.buttonHome.setEnabled(False)
        self.main.comboBoxBallSize.setEnabled(False)
        self.main.buttonRockHeight.setEnabled(False)
        self.main.inputDistance.setEnabled(False)

    def validate(self):
        self.validation = True
        self.checkRockHeight()
        self.checkBallSize()
        
        if self.validation == True:
            self.main.buttonConfirm.setEnabled(False)
            self.disablePanel()
            self.main.buttonLaunch.setEnabled(True)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This is a message box")
            msg.setInformativeText("This is additional information")
            msg.setWindowTitle("MessageBox demo")
            msg.setDetailedText(self.validationDetails)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        self.validationDetails = ""
