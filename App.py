# Dependencies
from MainWindow import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from io import BytesIO
from array import array

from MotorCommand import MotorCommand
from vars import *


from re import sub, match
from struct import *

import random
import datetime
import serial
import time

try:
    arduino = serial.Serial('COM3', 115200)
    #arduino = serial.Serial('/dev/ttyACM0', 115200)
except Exception as e:
    raise e

class Worker(QObject):
    finished = pyqtSignal()
    response = pyqtSignal(tuple)
    
    def __init__(self):
        super(Worker, self).__init__()
        
        # estructura del mensaje
        self.struct_fmt = '<BH'
        self.struct_len = calcsize(self.struct_fmt)
    
    def read_cmd(self,f):
        """
        :param f: file handler or serial file
        :return: (3 bytes)
        """
        return unpack(self.struct_fmt, bytearray(f.read(self.struct_len)))
    
    def work(self):
        try:
            while True:
                if arduino.in_waiting > 0:
                    rxCom = arduino.read_cmd(self.struct_len)
                    
                    self.response.emit(rxCom)

        except Exception as e:
            print(e)
        
        self.finished.emit()

class App(QApplication):
    # constructor
    def __init__(self, *args):
        QApplication.__init__(self, *args)


        # main objects 
        self.main = None
        self.worker = Worker()

        # main window
        self.main = MainWindow(self)
        self.configureWidgetsActions()

        # status 
        self.isExperimentRunning = False
        self.isAtZero = False
        self.isMoving = False

        self.main.center()
        self.main.show()
    
    def sendCMD(self, cmd, data):
        arduino.write(pack('<BH',cmd,data))      
    
    def configureWidgetsActions(self):
        self.main.comboBoxBallSize.currentIndexChanged.connect(self.actionBallSizeBox)
        self.main.buttonConfirm.clicked.connect(self.actionConfirmButton)

        self.main.buttonTake.clicked.connect(self.actionTakeButton)
        self.main.buttonHold.clicked.connect(self.actionHoldButton)
        self.main.buttonAdjust.clicked.connect(self.actionAdjustButton)

        self.main.buttonLaunch.clicked.connect(self.actionLaunchButton)
        self.main.buttonReset.clicked.connect(self.actionResetButton)
        self.main.buttonFinish.clicked.connect(self.actionFinishButton)
    
    # dato muestra
    def actionBallSizeBox(self):
        pass

    def actionTakeButton(self):
        self.main.buttonTake.setEnabled(False)
        self.sendCMD(TAKE_BALL, 0)
        self.serialHandler()
    
    def actionHoldButton(self):
        self.main.buttonHold.setEnabled(False)
        self.sendCMD(HOLD_BALL, 0)
        self.serialHandler()


    # adjust distance between ball and rock
    def actionAdjustButton(self):
        distance = self.main.inputDistance.text()
        if self.checkInputDistance(distance):
            self.sendCMD(SET_DISTANCE, int(distance))
            self.serialHandler()

    # drop ball
    def actionLaunchButton(self):
        #self.validate()
        self.main.buttonLaunch.setEnabled(False)
        self.sendCMD(DROP_BALL, 0)
        self.serialHandler()

    def actionResetButton(self):
        pass

    # confirm experiments data
    def actionConfirmButton(self):
        if not self.validate():
            self.showWarningMessage("fsdf","sdf",self.main.validationDetails)

            self.main.validationDetails = ""
        else:
            self.main.inputOrigin.setEnabled(False)
            self.main.inputType.setEnabled(False)
            self.main.comboBoxBallSize.setEnabled(False)

    def actionFinishButton(self):
        self.main.buttonTake.setEnabled(True)
        pass

    # llamada al worker
    def serialHandler(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.thread.wait)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.response.connect(self.arduinoResponse)
        self.thread.start()
    
    def arduinoResponse(self, response):
        
        cmd = response[0]
        print(cmd)

        if cmd == TAKEN:
            self.showConfirmMessage("Confirm action","The ball is set in place?")
            # esto está peligroso 
            while self.reply == QMessageBox.No: 
                time.sleep(3)
                self.showConfirmMessage("Confirm action","The ball is set in place?")
                break
            self.main.buttonHold.setEnabled(True)
            return       

        elif cmd == HELD:
            self.showMessage("Action Complete","Valve and motor are off")    
            self.main.inputDistance.setEnabled(True) 
            self.main.buttonAdjust.setEnabled(True)
            return  

        elif cmd == DROPPED:    
            self.loadData()
            self.main.buttonLaunch.setEnabled(True)
            return  
               
        elif cmd == SETTED:
            self.main.buttonLaunch.setEnabled(True)
            return
        
        else:
            print("NOT_SILC")
            return

        return

    def disablePanel(self):
        self.main.inputOrigin.setEnabled(False)
        self.main.inputType.setEnabled(False)
        self.main.comboBoxBallSize.setEnabled(False)

        self.main.buttonTake.setEnabled(False)
        self.main.buttonHold.setEnabled(False)
        self.main.inputDistance.setEnabled(False)
    
    def enablePanel(self):
        self.main.inputOrigin.setEnabled(True)
        self.main.inputType.setEnabled(True)
        self.main.comboBoxBallSize.setEnabled(True)
        
        self.main.buttonTake.setEnabled(True)
        self.main.buttonHold.setEnabled(True)
        self.main.inputDistance.setEnabled(True)

    def showMessage(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def showWarningMessage(self, title, text, details):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def showConfirmMessage(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No )
        self.reply = msg.exec_()


    def checkBallSize(self):
        if not self.main.comboBoxBallSize.currentText():
            self.validation = False
            self.main.validationDetails += "Seleccionar tamaño bola \n"
    
    def checkSampleOrigin(self):
        if not self.main.inputOrigin.text():
            self.validation = False
            self.main.validationDetails += "no hay origen \n"
    
    def checkSampleType(self):
        if not self.main.inputType.text():
            self.validation = False
            self.main.validationDetails += "no hay tipo \n"
    
    def checkInputDistance(self,input):
        if not input:
            self.showWarningMessage("Incomplete","The distance needs to be defined")
        elif not bool(match('^[0-9]+$', input)):
            self.showWarningMessage("Wrong parameter", "The distance must only contain numbers")
        elif int(input) > 350:
            self.showWarningMessage("Wrong parameter", "The maximum distance is 350mm")
        else:
            return True

    def validate(self):
        self.validation = True
        self.checkSampleOrigin()
        self.checkSampleType()
        self.checkBallSize()
        
        return self.validation


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
        if self.main.inputOrigin == "" or self.main.inputType == "":
            self.main.inputOrigin == " "
            self.main.inputType == " "

        rowPosition = self.main.tableWidget.rowCount()
        self.main.tableWidget.insertRow(rowPosition)

        self.main.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(self.main.comboBoxBallSize.currentText()))
        self.main.tableWidget.setItem(rowPosition, 1, QTableWidgetItem("hola"))
        self.main.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(self.main.inputDistance.text()))
        self.main.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(self.experimentNaming())) #hash distintivo x exp
        self.main.iterations += 1

