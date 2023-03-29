import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QColor
from pathlib import *
from PIL import Image
import time
import pyautogui


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def drawingFunc(self):
        while(True):
            print(pyautogui.position())


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("doodleBob.ui", self)
  
        # calling method    
        self.setWindowTitle("DoodleBob")

        #functions that connect to the functions to the let the user change the color and that let the user draw
        self.draw.clicked.connect(self.drawingFunc)
        self.menu.clicked.connect(self.colorSelect)

        #creating a blank white image that will be the base for the drawing screen
        newDrawing = Image.new(mode="RGB", size=(800, 480),
                        color="white")
  
        newDrawing.save("new_drawing", format="png")
        pixels = newDrawing.load()

    #Function that connects the worker class to the main thread
    def drawingFunc(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.drawingFunc)
        self.thread.start()


    #Pulls up the color selection menu
    def colorSelect(self):
        # opening color dialog
        color = QColorDialog.getColor()
        self.currColor.setText(color.name())
        self.show()
        return color
 

#Showing window and executing app
app = QApplication(sys.argv)
window = MainWindow()
window.show() 
app.exec()






