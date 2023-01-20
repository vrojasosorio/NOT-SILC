# Dependencies
from MainWindow import MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from io import BytesIO
from array import array

from MotorCommand import MotorCommand
from vars import *

from re import sub
from struct import *

import random
import datetime
import serial

class Worker(QObject):
    finished = pyqtSignal()
    response = pyqtSignal(tuple)
    
    def __init__(self):
        super(Worker, self).__init__()
        self.arduino = serial.Serial('/dev/ttyACM1', 9600)
        self.machine = MotorCommand()
        
        # estructura del mensaje
        self.struct_fmt = '<BH'
        self.struct_len = calcsize(self.struct_fmt)
    
    def work(self):
        try:
            while True:
                if self.arduino.in_waiting > 0:
                    msg = self.arduino.read(self.struct_len)
                    rxCom = unpack(self.struct_fmt, msg)
                    self.response.emit(rxCom)

        except Exception as e:
            print(e)
        
        self.finished.emit()

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
    
    def sendCMD(self, cmd, data=0):
        self.worker.machine.cmd = cmd
        self.worker.machine.data = data
        
        self.send_command()


    def send_command(self):
        buff = BytesIO()
        self.worker.machine.serialize(buff)

        packet = bytearray(buff.getvalue())
        packet_str = array('B', packet).tostring()
   
        self.write_serial(packet_str)

    def write_serial(self, data):
        """
        Write in the serial port.
        """
        #print(self.cmd)
        #print("Hex: {}".format(to_hex(data)))
        self.worker.arduino.flushInput()
        self.worker.arduino.flushOutput()
        self.worker.arduino.write(data)
        
    
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
        self.main.buttonHome.setEnabled(False)
        self.sendCMD(SET_AT_ZERO)
        self.serialHandler()

    # dato muestra
    def actionBallSizeBox(self):
        pass

    # adjust distance between ball and rock
    def actionBallHeightButton(self):
        self.main.labelHeightValue.setText(str(round(random.random(),3)))
        self.sendCMD(M2, MEASURE_DISTANCE)
        self.sendCMD(M2,SET_DISTANCE)

    # confirm experiments data
    def actionConfirmButton(self):
        self.validate()

    # drop ball
    def actionLaunchButton(self):
        self.main.buttonLaunch.setEnabled(False)
        self.sendCMD(M1, DROP_BALL)
        self.loadData()
        self.main.buttonLaunch.setEnabled(True)
        
    def actionSaveButton(self):
        # este botón no va, aca se debería cargar la row sola cuandoe l arduino dice q ta bien
        pass

    def actionFinishButton(self):
        # llamada a función q exporta un csv
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
        self.worker.response.connect(self.arduinoStatus)
        self.thread.start()
    
    def arduinoStatus(self, response):
        print(response)
        cmd = response[0]
        #self.worker.finished.emit()

        if cmd == HOME:
            self.showMessage("Action Complete","Toi en el home xsia","relleno")     
            self.main.buttonHome.setEnabled(True)       
        else:
            print("No entré al if")
        return

    def disablePanel(self):
        self.main.inputOrigin.setEnabled(False)
        self.main.inputType.setEnabled(False)

        self.main.inputIterations.setEnabled(False)
        self.main.buttonHome.setEnabled(False)
        self.main.comboBoxBallSize.setEnabled(False)
        self.main.buttonRockHeight.setEnabled(False)
        self.main.inputDistance.setEnabled(False)
    
    def enablePanel(self):
        self.main.inputOrigin.setEnabled(True)
        self.main.inputType.setEnabled(True)
        
        self.main.inputIterations.setEnabled(True)
        self.main.buttonHome.setEnabled(True)
        self.main.comboBoxBallSize.setEnabled(True)
        self.main.buttonRockHeight.setEnabled(True)
        self.main.inputDistance.setEnabled(True)

    def showMessage(self, title, text, information):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def checkBallSize(self):
        if self.main.comboBoxBallSize.currentText() == "":
            self.validation = False
            self.main.validationDetails += "Seleccionar tamaño bola \n"
    
    def checkRockHeight(self):
        if self.main.labelHeightValue.text() == "":
            self.validation = False
            self.main.validationDetails += "Medir altura \n"
    
    def checkInputDistance(self):
        pass # revisar que los caracteres sean soolo numeros y no otras cosas


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
            msg.setDetailedText(self.main.validationDetails)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

        self.main.validationDetails = ""

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