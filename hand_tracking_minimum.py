#importing the required modules

import cv2
import time #to check the frame rate
import mediapipe as mp

#Creating the video object
cap = cv2.VideoCapture(0)

#A formality to before using this module
mpHands = mp.solutions.hands

#Creating object called Hands
hands = mpHands.Hands()

#Module used for drawing lines between the landmarks
mpDraw = mp.solutions.drawing_utils

#Tracking prev and current time for tracking fps
pTime = 0
cTime = 0


while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Converting the channel of the img from BGR to RGB
    results = hands.process(imgRGB)

    #Checking if something is detected or not
    print(results.multi_hand_landmarks)

    #Extracting landmarks of multiple hands if present
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):

                #print(id, lm)
                h, w, c = img.shape # height, weidth, channel of the img
                cx, cy = int(lm.x * w), int(lm.y * h) # finding the positions in pixel instead of ratios
                print(id, cx, cy)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED) # Drawing the circle

            # we are using img not imgRGB because we are displaying BGR image
            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)  # `mpHands.HAND_CONNECTIONS` : draws the connections


    cTime = time.time() # Gives us the current time
    fps = 1/(cTime - pTime)
    pTime = cTime

    #Displaying on the screen
    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)