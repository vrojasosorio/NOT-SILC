# Dependencies
from MainWindow import MainWindow
from PyQt5.Qt import *

class App(QApplication):
    # constructor
    def __init__(self):
        super().__init__()

        # main objects in window
        self.main = None

        # main window
        self.main = MainWindow(self)
    
    def sendCMD(self, id_actuador, cmd, ):
        pass
    
    def configureWidgetsActions(self):
        self.main.buttonHome.clicked.connect()
        self.main.comboBoxBallSize.currentIndexChanged.connect()
        self.main.buttonBallHeight.clicked.connect()
        #self.main.inputDistance
    
    def actionHomeButton(self):
        pass