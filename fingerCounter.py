import cv2
import os
import time

cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
x = 0
while True:

    _, img = cap.read()
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('y'):
        cv2.imwrite(f'c{x}.png', img)
        x+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()

