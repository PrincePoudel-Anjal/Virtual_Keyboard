import cv2
import numpy as np
import mediapipe as mp
import math

text = ""

def find_distance(image,p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    length = math.hypot(x2-x1,y2-y1)
    if image is not None:
        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
        
    return length, image

# Class of Buttons
class Button:
    def __init__(self,label,pos1,pos2):
        self.label = label
        self.pos1 = pos1
        self.pos2 = pos2

    def draw_rectangle(self,image,color):
        cv2.rectangle(image, self.pos1,self.pos2, color, 10)
    def puttext(self,image,x,y):
         cv2.putText(image,self.label,(x+5,y+40),cv2.FONT_HERSHEY_PLAIN,3,(47,255,173),3)

def hand_detection(image,Draw,mphands,hands,draw):
    positionx = [0] * 20
    positiony = [0] * 20
    Area = 0


    rgbimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgbimage)
    frame_shape = rgbimage.shape
    if Draw == True:
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                for index, landmark in enumerate(hand.landmark):
                    h, w, no_of_colors = frame_shape
                    if index == 8:
                        positionx[index], positiony[index] = int(landmark.x * w), int(landmark.y * h)
                    if index == 12:
                        positionx[12], positiony[12] = int(landmark.x * w), int(landmark.y * h)
                    if index == 4:
                        positionx[4], positiony[4] = int(landmark.x * w), int(landmark.y * h)
                    if index == 9:
                        positionx[9], positiony[9] = int(landmark.x * w), int(landmark.y * h)

                    draw.draw_landmarks(image, hand, mphands.HAND_CONNECTIONS)
    area = 3.14 * (positionx[9]-positionx[4]) * (positionx[9]-positionx[4])

    create_buttons(image,positionx,positiony,area)

# Creating the button
def create_buttons(image,px,py,area):
    global text
    color = (255,0,0)
    keys = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M"]
    ]

    y = 100
    button = [0] * 30
    count = 0
    cv2.rectangle(image, (150, 500), (500 + 200, 600), (128, 128, 128), -1) #Writing Box


    for row, i in enumerate(keys):
        x = 150
        y = y + 55
        for j in i:
            button[count] = Button(j, (x, y), (x + 50, y + 50))
            button[count].puttext(image, x, y)

            if x<=px[8]<=x+50 and y<=py[8]<=y+50:
                button[count].draw_rectangle(image, (255,255,10))
                length,image = find_distance(image,(px[8],py[8]),(px[12],py[12]))

                print(area," ",length)

                if  area <10000:
                    cv2.circle(image, (px[9], py[9]), py[9]-py[12], (0, 255, 0), 2)  #BBox Object detection
                    if 18<length<21:
                        cv2.waitKey(150)
                        text = text + j



            else:
                button[count].draw_rectangle(image, color)
            x += 50 + 5
            cv2.putText(image, text, (150, 570), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), thickness=7)

            count += 1

# main
ret = True
video = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands(static_image_mode = False,min_detection_confidence= 0.8,min_tracking_confidence=0.8)
draw = mp.solutions.drawing_utils


while ret == True:
    ret, image = video.read()
    image = cv2.resize(image, (1000, 700))
    image = cv2.flip(image, 1)
    hand_detection(image,True,mphands,hands,draw)
    cv2.imshow('Frame', image)
    cv2.waitKey(1)
#Conclusion: Main->hand_detection->CreateButtons
