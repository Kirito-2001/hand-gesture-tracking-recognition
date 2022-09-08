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
widthCamera, highCamera = 1330, 680
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

        cv2.rectangle(img, (620, 10), (1420, 275), (0, 255, 0), cv2.FILLED)

        # indice-pollice
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

        cv2.putText(img, f' {(int(volumePercentage))}%', (0, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 255), 3)
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 255), 3)
        cv2.rectangle(img, (50, int(volumeBar)), (85, 400), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, f' {lenght} cm', (620, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 255), 3)


        #cambio colore sotto un certo range
        if lenght < 8:
            cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (cx, cy), 6, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volumeBar)), (85, 400), (0, 255, 0), cv2.FILLED)




    # medio-pollice
        a1, b1 = landmarkList[4][1], landmarkList[4][2]
        a2, b2 = landmarkList[12][1], landmarkList[12][2]
        c_x, c_y = (a1 + a2) // 2, (b1 + b2) // 2  # coordinate per centro

        cv2.circle(img, (a1, b1), 8, (215, 0, 0), cv2.FILLED)
        cv2.circle(img, (a2, b2), 8, (215, 0, 0), cv2.FILLED)
        cv2.circle(img, (c_x, c_y), 6, (215, 0, 0), cv2.FILLED)

        cv2.line(img, (a1, b1), (a2, b2), (215, 0, 0), 3)

        # lunghezza segmento
        lenght = math.hypot(a2 - a1, b2 - b1) / 10  # lenght è in dm, ==> facciamo /10
        # print(lenght)

        # now change the value basing on the lenght
        # i know hand range is 10-30
        vol = np.interp(lenght, [3, 30.5], [minimVolume, maximVolume])  # converto valori min e max della lenght in volume
        #print(vol)
        volumeBar = np.interp(lenght, [3, 30.5], [400, 150])  # 400 e 150 settati giu nel rectangle
        volumePercentage = np.interp(lenght, [3, 30.5], [0, 100])  # 400 e 150 settati giu nel rectangle

        volume.SetMasterVolumeLevel(vol, None)

        cv2.putText(img, f' {(int(volumePercentage))}%', (130, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (215, 0, 0), 3)
        cv2.rectangle(img, (170, 150), (205, 400), (215, 0, 0), 3)
        cv2.rectangle(img, (170, int(volumeBar)), (205, 400), (215, 0, 0), cv2.FILLED)
        cv2.putText(img, f' {lenght} cm', (620, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (215, 0, 0), 3)


        # cambio colore sotto un certo range
        if lenght < 8:
            cv2.circle(img, (a1, b1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (a2, b2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (c_x, c_y), 6, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (a1, b1), (a2, b2), (0, 255, 0), 3)
            cv2.rectangle(img, (170, int(volumeBar)), (205, 400), (0, 255, 0), cv2.FILLED)



    # anulare-pollice
        c1, d1 = landmarkList[4][1], landmarkList[4][2]
        c2, d2 = landmarkList[16][1], landmarkList[16][2]
        c__x, c__y = (c1 + c2) // 2, (d1 + d2) // 2  # coordinate per centro

        cv2.circle(img, (c1, d1), 8, (0, 0, 215), cv2.FILLED)
        cv2.circle(img, (c2, d2), 8, (0, 0, 215), cv2.FILLED)
        cv2.circle(img, (c__x, c__y), 6, (0, 0, 215), cv2.FILLED)

        cv2.line(img, (c1, d1), (c2, d2), (0, 0, 215), 3)

        # lunghezza segmento
        lenght = math.hypot(c2 - c1, d2 - d1) / 10  # lenght è in dm, ==> facciamo /10
        # print(lenght)

        # now change the value basing on the lenght
        # i know hand range is 10-30
        vol = np.interp(lenght, [3, 30.5], [minimVolume, maximVolume])  # converto valori min e max della lenght in volume
        # print(vol)
        volumeBar = np.interp(lenght, [3, 30.5], [400, 150])  # 400 e 150 settati giu nel rectangle
        volumePercentage = np.interp(lenght, [3, 30.5], [0, 100])  # 400 e 150 settati giu nel rectangle

        volume.SetMasterVolumeLevel(vol, None)

        cv2.putText(img, f' {(int(volumePercentage))}%', (270, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 215), 3)
        cv2.rectangle(img, (320, 150), (355, 400), (0, 0, 215), 3)
        cv2.rectangle(img, (320, int(volumeBar)), (355, 400), (0, 0, 215), cv2.FILLED)
        cv2.putText(img, f' {lenght} cm', (620, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 215), 3)

        # cambio colore sotto un certo range
        if lenght < 8:
            cv2.circle(img, (c1, d1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (c2, d2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (c__x, c__y), 6, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (c1, d1), (c2, d2), (0, 255, 0), 3)
            cv2.rectangle(img, (320, int(volumeBar)), (355, 400), (0, 255, 0), cv2.FILLED)


    # mignolo-pollice
        r1, s1 = landmarkList[4][1], landmarkList[4][2]
        r2, s2 = landmarkList[20][1], landmarkList[20][2]
        c___x, c___y = (r1 + r2) // 2, (s1 + s2) // 2  # coordinate per centro

        cv2.circle(img, (r1, s1), 8, (255, 205, 255), cv2.FILLED)
        cv2.circle(img, (r2, s2), 8, (255, 205, 255), cv2.FILLED)
        cv2.circle(img, (c___x, c___y), 6, (255, 205, 255), cv2.FILLED)

        cv2.line(img, (r1, s1), (r2, s2), (255, 205, 255), 3)

        # lunghezza segmento
        lenght = math.hypot(r2 - r1, s2 - s1) / 10  # lenght è in dm, ==> facciamo /10
        # print(lenght)

        # now change the value basing on the lenght
        # i know hand range is 10-30
        vol = np.interp(lenght, [3, 30.5], [minimVolume, maximVolume])  # converto valori min e max della lenght in volume
        # print(vol)
        volumeBar = np.interp(lenght, [3, 30.5], [400, 150])  # 400 e 150 settati giu nel rectangle
        volumePercentage = np.interp(lenght, [3, 30.5], [0, 100])  # 400 e 150 settati giu nel rectangle

        volume.SetMasterVolumeLevel(vol, None)

        cv2.putText(img, f' {(int(volumePercentage))}%', (410, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 205, 255), 3)
        cv2.rectangle(img, (450, 150), (485, 400), (255, 205, 255), 3)
        cv2.rectangle(img, (450, int(volumeBar)), (485, 400), (255, 205, 255), cv2.FILLED)
        cv2.putText(img, f' {lenght} cm', (620, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 205, 255), 3)

        # cambio colore sotto un certo range
        if lenght < 8:
            cv2.circle(img, (r1, s1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (r2, s2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (c___x, c___y), 6, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (r1, s1), (r2, s2), (0, 255, 0), 3)
            cv2.rectangle(img, (450, int(volumeBar)), (485, 400), (0, 255, 0), cv2.FILLED)

    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime

    cv2.putText(img, f'FPS: {(int(fps))}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (60, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)