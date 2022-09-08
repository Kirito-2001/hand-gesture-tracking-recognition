import cv2
import time
import numpy as np
import hand_tracking_module as htm # uso modulo
import math

# import for volumes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#################
widthCamera, highCamera = 630, 480
##############

cap = cv2.VideoCapture(0)
cap.set(3, widthCamera)
cap.set(4, highCamera)

previousTime = 0

detector = htm.handDetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
# print(volumeRange) # to see the range --> (-65.25, 0.0, 0.03125)
maximVolume = volumeRange[1]
minimVolume = volumeRange[0]

vol = 0;
volumeBar = 0
volumePercentage = 0
while True:
    success, img = cap.read()

    img = detector.findHands(img)

    landmarkList = detector.findPosition(img, draw=False)
    if len(landmarkList) != 0:
        # print(landmarkList[4], landmarkList[8])

        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2 # coordinate per centro

        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        # lunghezza segmento
        lenght = math.hypot(x2-x1, y2-y1)/10 # lenght è in dm, ==> facciamo /10
        #print(lenght)

        # now change the value basing on the lenght
        # i know hand range is 10-30
        vol = np.interp(lenght, [3, 30.5], [minimVolume, maximVolume])  # converto valori min e max della lenght in volume
        volumeBar = np.interp(lenght, [3, 30.5], [400, 150]) # 400 e 150 settati giu nel rectangle
        volumePercentage = np.interp(lenght, [3, 30.5], [0, 100]) # 400 e 150 settati giu nel rectangle

        volume.SetMasterVolumeLevel(vol, None)

        #cambio colore sotto un certo range
        if lenght < 8:
            cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (cx, cy), 6, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        cv2.putText(img, f' {(int(volumePercentage))}%', (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volumeBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime

    cv2.putText(img, f'FPS: {(int(fps))}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)