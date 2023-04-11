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
import cv2


class Worker(QObject):
    #finished = pyqtSignal()

    def __init__(self, window):
        super(Worker, self).__init__()
        self.pixels = window.pixels

    def drawingFunc(self):
        while(True):
            print(pyautogui.position())
            x, y = pyautogui.position()

            if (x <= 800 & y<=480):
                print("drawing!")
                window.pixels[x,y] = (255,255,255)
                window.newDrawing.save("new_drawing", format="png")
                image = cv2.imread(r'C:\Users\laure\Desktop\College\Pitt\S6\Junior_Design\finalProject_juniorDesign\new_drawing')
                cv2.imshow('new_drawing', image)
                cv2.waitKey(1)
   
            time.sleep(1)


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
        self.newDrawing = Image.new(mode="RGB", size=(800, 480), color="white")
        
        self.pixels = self.newDrawing.load()

        #TEMPTEMPTEMP
        image = cv2.imread(r'C:\Users\laure\Desktop\College\Pitt\S6\Junior_Design\finalProject_juniorDesign\new_drawing')
        cv2.imshow('new_drawing', image)

    #Function that connects the worker class to the main thread
    def drawingFunc(self):
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.drawingFunc())
        self.thread.start()


    #Pulls up the color selection menu
    def colorSelect(self):
        # opening color dialog
        color = QColorDialog.getColor()
        colorHex = color.name()
        self.currColor.setText(colorHex)
        
        #getting the hex value into RGB format
        red = (16 * int(colorHex[1],16)) + (int(colorHex[2],16))
        green = (16 * int(colorHex[3],16)) + (int(colorHex[4],16))
        blue = (16 * int(colorHex[5],16)) + (int(colorHex[6],16))

        for i in range(800):
            for j in range(480):
                self.pixels[i,j] = (red,green,blue)
        self.newDrawing.save("new_drawing", format="png")
        self.show()
        return color
 

#Showing window and executing app
app = QApplication(sys.argv)
window = MainWindow()
window.show() 
app.exec()






