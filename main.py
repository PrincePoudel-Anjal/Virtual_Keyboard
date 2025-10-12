import cv2
import numpy as np
import sys


from HandTracker import hand_TRACKER

# Class of Buttons
class Button:
    def __init__(self,label,pos1,pos2):
        self.label = label
        self.pos1 = pos1
        self.pos2 = pos2

    def draw_rectangle(self,image):
        cv2.rectangle(image, self.pos1,self.pos2, (255, 0, 0), 5)
    def puttext(self,image,x,y):
         cv2.putText(image,self.label,(x+5,y+40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)


# Creating the button
def create_buttons(image):
    keys = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"]
    ]

    y = 400
    button = [0] * 30
    count = 0
    for row, i in enumerate(keys):
        x = 250
        y = y + 55
        for j in i:
            button[count] = Button(j, (x, y), (x + 50, y + 50))
            button[count].puttext(image, x, y)
            x += 50 + 5
            button[count].draw_rectangle(image)

            count += 1



ret = True
video = cv2.VideoCapture(0)

while ret == True:
    ret,image = video.read()
    image = cv2.resize(image,(1000, 700))
    image = cv2.flip(image,1)
    create_buttons(image)










