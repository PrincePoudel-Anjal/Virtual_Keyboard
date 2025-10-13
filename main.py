import cv2
import numpy as np
import sys
import mediapipe as mp



from HandTracker import hand_TRACKER

# Class of Buttons
class Button:
    def __init__(self,label,pos1,pos2):
        self.label = label
        self.pos1 = pos1
        self.pos2 = pos2

    def draw_rectangle(self,image,color):
        cv2.rectangle(image, self.pos1,self.pos2, color, 5)
    def puttext(self,image,x,y):
         cv2.putText(image,self.label,(x+5,y+40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)

def hand_detection(image,Draw,mphands,hands,draw):
    positionx = 0
    positiony = 0

    rgbimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgbimage)
    frame_shape = rgbimage.shape
    if Draw == True:
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                for index, landmark in enumerate(hand.landmark):
                    h, w, no_of_colors = frame_shape
                    if index == 8:
                        positionx, positiony = int(landmark.x * w), int(landmark.y * h)


            draw.draw_landmarks(image, hand, mphands.HAND_CONNECTIONS)
    create_buttons(image,positionx,positiony)




# Creating the button
def create_buttons(image,px,py):
    color = (255, 0, 0)
    keys = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"]
    ]

    y = 200
    button = [0] * 30
    count = 0
    for row, i in enumerate(keys):
        x = 250
        y = y + 55
        for j in i:
            button[count] = Button(j, (x, y), (x + 50, y + 50))
            button[count].puttext(image, x, y)
            x += 50 + 5
            if x<=px<=x+50 and y<=py<=y+50:
                button[count].draw_rectangle(image, (255,255,0))
            else:
                button[count].draw_rectangle(image, color)

            count += 1



# main

ret = True
video = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode = False,min_detection_confidence= 0.2,min_tracking_confidence=0.2)
draw = mp.solutions.drawing_utils

while ret == True:
    ret, image = video.read()
    image = cv2.resize(image, (1000, 700))
    image = cv2.flip(image, 1)
    hand_detection(image,True,mphands,hands,draw)
    cv2.imshow('Frame', image)
    cv2.waitKey(1)
