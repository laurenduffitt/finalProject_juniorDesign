import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QColor
from pathlib import *
import numpy as np
import cv2 as cv


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("doodleBob.ui", self) 
        self.setWindowTitle("DoodleBob")

        #default pen color = red, default background color = black, default 
        self.color = [0,0,255]
        self.backgroundColor = [0,0,0]
        self.penSize = 5

        self.slider.setMinimum(1)
        self.slider.setMaximum(15)


    #Pulls up the color selection menu
    def colorSelect(self):
        # opening color dialog
        self.color = QColorDialog.getColor()
        colorHex = self.color.name()
         
        #getting the hex value into RGB format
        blue = (16 * int(colorHex[1],16)) + (int(colorHex[2],16))
        green = (16 * int(colorHex[3],16)) + (int(colorHex[4],16))
        red = (16 * int(colorHex[5],16)) + (int(colorHex[6],16))

        self.color = [red,green,blue]

        self.show()
        return self.color
   
    def erase(self):
        self.color = self.backgroundColor
    
    def backColor(self):
        self.backgroundColor = window.colorSelect()
    
    def sliderChanged(self):
        self.penSize = self.slider.value()
    

#Begin main function classes

def draw_circle(event,x,y,flags,param):
    sliderSize = window.penSize
    cv.circle(img,(x,y),sliderSize,param[0],-1)

def clear():
    newColor = window.backgroundColor
    p2 = 0, 512    
    p3 = 512, 0
    cv.rectangle(img, p2, p3, (newColor[0],newColor[1],newColor[2]), cv.FILLED)

def background():
    newColor = window.color
    p2 = 0, 512    
    p3 = 512, 0
    cv.rectangle(img, p2, p3, (newColor[0],newColor[1],newColor[2]), cv.FILLED)





#Creating the Qapp file
app = QApplication(sys.argv)
window = MainWindow()

img = np.zeros((512,512,3), np.uint8)

#functions that connect to the functions in the MainWindow of the user interface
window.menu.clicked.connect(window.colorSelect)
window.erasePush.clicked.connect(window.erase)
window.clearPush.clicked.connect(clear)
window.backgroundPush.clicked.connect(window.backColor)
window.backgroundPush.clicked.connect(background)
window.slider.valueChanged.connect(window.sliderChanged)

while(1):
    color = window.color
    red = color[0]
    green = color[1]
    blue = color[2]

    param = [(red,green,blue)]
    cv.namedWindow('image')
    cv.setMouseCallback('image',draw_circle, param)
    cv.imshow('image',img)
    cv.waitKey(1)
    window.show()
    

app.exec()
cv.destroyAllWindows()
