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
  
        # calling method    
        self.setWindowTitle("DoodleBob")

        self.color = [0,0,255]


    #Pulls up the color selection menu
    def colorSelect(self):
        # opening color dialog
        self.color = QColorDialog.getColor()
        colorHex = self.color.name()
        self.currColor.setText(colorHex)
        
        #getting the hex value into RGB format
        red = (16 * int(colorHex[1],16)) + (int(colorHex[2],16))
        green = (16 * int(colorHex[3],16)) + (int(colorHex[4],16))
        blue = (16 * int(colorHex[5],16)) + (int(colorHex[6],16))

        self.color = [red,green,blue]

        self.show()
        return self.color
   
    def erase(self):
        self.color = [0,0,0]
    
 

def draw_circle(event,x,y,flags,param):
    cv.circle(img,(x,y),5,param[0],-1)

def clear():
    p2 = 0, 512    
    p3 = 512, 0
    cv.rectangle(img, p2, p3, (0,0,0), cv.FILLED)
    

app = QApplication(sys.argv)
window = MainWindow()

img = np.zeros((512,512,3), np.uint8)

#functions that connect to the functions in the MainWindow of the user interface
window.menu.clicked.connect(window.colorSelect)
window.erasePush.clicked.connect(window.erase)
window.clearPush.clicked.connect(clear)

while(1):
    #if (window.clearPush.clicked == True):
    #    print("true")
    #    img = np.zeros((512,512,3), np.uint8)
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
