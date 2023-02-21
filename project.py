import cv2
import time
import mediapipe as mp
import HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm. HandDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw = True)
    lmList = detector.findPosition(img, draw = False)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.imshow("Image", img)
    cv2.waitKey(1)
