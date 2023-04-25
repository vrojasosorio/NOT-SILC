# -*- coding: utf-8 -*-

from App import App
from PyQt5.Qt import *

# Operating system
import sys
import time

def main(args):
    global app

    app = App(args)
    app.setStyle('Fusion') #Fusion Windows Oxygen

    app.exec_()

if __name__ == "__main__":
    main(sys.argv)