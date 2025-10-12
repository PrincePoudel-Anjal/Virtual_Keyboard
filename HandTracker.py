import cv2
import mediapipe as mp
import time

class hand_TRACKER:
    def __init__(self,mode = False,no_of_hands = 2,detection_conf = 0.3,tracking_conf=0.3):
        self.mode = mode
        self.no_of_hands = no_of_hands
        self.detection_conf = detection_conf
        self.min_tracking_confidence = tracking_conf

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(static_image_mode= self.mode,max_num_hands= no_of_hands,min_tracking_confidence=tracking_conf,min_detection_confidence=detection_conf)
        self.draw = mp.solutions.drawing_utils

    def track(self,Draw,print_positions):
        video = cv2.VideoCapture(0)
        previoustime = 0
        currenttime = 0
        rate = True
        while rate == True:
            rate, video_frame = video.read()
            rgbimage = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgbimage)
            frame_shape = rgbimage.shape
            if Draw == True:

                if result.multi_hand_landmarks:  # Checks for landmark
                    for hand in result.multi_hand_landmarks:
                        currenttime = time.time()
                        fps = 1/ (currenttime - previoustime)
                        previoustime = currenttime
                        cv2.putText(video_frame, str(int(fps)), (29, 50), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2,
                                    (0, 0, 255), 4)

                        self.draw.draw_landmarks(video_frame, hand, self.mphands.HAND_CONNECTIONS)
                        if print_positions == True:
                            self.print_positions(result,frame_shape)



    def print_positions(self,result,frame_shape):
        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                for index, landmark in enumerate(hand.landmark):
                    h, w, no_of_colors = frame_shape
                    positionx, positiony = int(landmark.x * w), int(landmark.y * h)
                    print("index:", index, "\t", positionx, positiony)





# hand_tracker = hand_TRACKER(mode = True)
# result,frame_shape = hand_tracker.track(Draw=True,print_positions = True)










