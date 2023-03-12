import cv2
import os
import time
import HandTrackingModule as htm

pTime = 0
cap = cv2.VideoCapture(0)
wcam = 640
hcam = 480

cap.set(3, wcam)
cap.set(4, hcam)
x = 0

detector = htm.HandDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    _, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw = False)
    print(lmList)
    if lmList:

        for id in tipIds:
            fingers = []
            if lmList[id][2] < lmList[id - 2][2]:
                print("index finger open")

    cTime = time.time()
    fps=1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

