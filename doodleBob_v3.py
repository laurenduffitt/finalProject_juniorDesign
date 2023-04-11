import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QColor
from pathlib import *
import numpy as np
import cv2 as cv

class Worker(QObject):
    #finished = pyqtSignal()

    def __init__(self):
        super(Worker, self).__init__()
        self.img = np.zeros((512,512,3), np.uint8)

    def draw_circle(event,x,y,flags,param,self):
        cv.circle(self.img,(x,y),5,(0,0,255),-1)
        print("in da function!!")
       
    def draw_circle_link(self):
        cv.namedWindow('image')
        cv.setMouseCallback('image',self.draw_circle)

        while(1):
            cv.imshow('image',self.img)
            cv.waitKey(1)
            print("in da loop")
        cv.destroyAllWindows()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("doodleBob.ui", self)
  
        # calling method    
        self.setWindowTitle("DoodleBob")

        #functions that connect to the functions to the let the user change the color and that let the user draw
        self.menu.clicked.connect(self.colorSelect)
        self.draw.clicked.connect(self.draw_circle)

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

        color = (red,green,blue)

        self.show()
        return color
    
    def draw_circle(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.draw_circle_link())
        self.thread.start()
 

def draw_circle(event,x,y,flags,param):
        cv.circle(img,(x,y),5,(0,0,255),-1)

img = np.zeros((512,512,3), np.uint8)
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)

app = QApplication(sys.argv)
window = MainWindow()
window.show() 
app.exec()

while(1):
    cv.imshow('image',img)
    cv.waitKey(1)
cv.destroyAllWindows()

