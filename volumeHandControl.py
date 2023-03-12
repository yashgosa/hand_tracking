# importing required modules

import math
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########################
wCam, hCam = 1280, 720
########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon= 0.7)


devices = AudioUtilities.GetSpeakers() #get the speakers (1st render + multimedia) device
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange() # gets the range of volume


minVol = volRange[0]
maxVol = volRange[1]
vol = 0
vol_bar = 400
vol_per = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if lmList:
        # print(lmList[4], lmList[8]) #GEtting the landmarks of thumb and index

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)


        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        if length <= 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        else:
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        vol_bar = np.interp(length, [50, 300], [400, 150])
        vol_per = np.interp(length, [50, 300], [0, 100])


        volume.SetMasterVolumeLevel(vol, None)
        print(int(length), vol)

        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
        cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"{int(vol_per)} %", (40, 450), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 3)


    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"fps: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


