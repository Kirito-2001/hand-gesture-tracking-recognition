import cv2
import time
import os

import hand_tracking_module as htm

#################
widthCamera, highCamera = 1100, 880
##############

cap = cv2.VideoCapture(0)
cap.set(3, widthCamera)
cap.set(4, highCamera)

# store image
folderPath = "images"
myList = os.listdir(folderPath)
#print(myList)

#salvo immagine in lista
ListOfImages = []
for imagePath in myList:
    image = cv2.imread(f'{folderPath}/{imagePath}')
    ListOfImages.append(image)


previousTime = 0

detector = htm.handDetector()

idPuntiDita = [4, 8, 12, 16, 20, 5, 9, 13, 17]
while True:
    success, img = cap.read()

    img = detector.findHands(img)
    landmarkList = detector.findPosition(img, draw=False) # no palllini grandi

    if len(landmarkList)!=0:
            fingers = []

            # check sul pollice
            if landmarkList[idPuntiDita[0]][1] < landmarkList[idPuntiDita[0] - 2][1]:  # caso dito alzato
                fingers.append(1)
            else:
                fingers.append(0)
            # check sulle altre dita
            for id in range(1, 5):
                if landmarkList[idPuntiDita[id]][2] < landmarkList[idPuntiDita[id]-1][2]: # caso dito alzato
                    fingers.append(1)
                    #print("indice aperto")
                else:
                    fingers.append(0)

            #print(fingers)

            #change images
            #totalFingers = fingers.count(1)
            #print(totalFingers)

            #h, w, c =ListOfImages[totalFingers].shape
            #print(h, w, c)
            #img[0:h, 0:w] = ListOfImages[totalFingers]

            cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)

            # caso 5
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1 :
                cv2.putText(img, str(5), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[5].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[5]

            if (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1) and (landmarkList[idPuntiDita[1]][2] < landmarkList[idPuntiDita[5]][2] and landmarkList[idPuntiDita[2]][2] < landmarkList[idPuntiDita[6]][2] and landmarkList[idPuntiDita[3]][2] < landmarkList[idPuntiDita[7]][2] and landmarkList[idPuntiDita[4]][2] < landmarkList[idPuntiDita[8]][2]) :
                cv2.putText(img, str(4), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[4].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[4]

            if (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0) or (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0):
                cv2.putText(img, str(3), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[3].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[3]

            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 :
                cv2.putText(img, str(2), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[2].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[2]

            if (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0) and (landmarkList[idPuntiDita[1]][2] < landmarkList[idPuntiDita[5]][2]) :
                cv2.putText(img, str(1), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[1].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[1]

            if ((fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0) or (fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1) or (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1)) and ((landmarkList[idPuntiDita[1]][2] > landmarkList[3][2] and landmarkList[idPuntiDita[2]][2] > landmarkList[13][2] and landmarkList[idPuntiDita[3]][2] > landmarkList[15][2] and landmarkList[idPuntiDita[4]][2] > landmarkList[19][2])):
                cv2.putText(img, str(0), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[0].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[0]

            if (fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1) or (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1) :
                cv2.rectangle(img, (20, 255), (330, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'rock', (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 6)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[6].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[6]

            if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                cv2.rectangle(img, (20, 255), (330, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'peace', (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 6)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[7].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[7]

            if ((fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1) or(fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1)) and (landmarkList[idPuntiDita[1]][2] < landmarkList[idPuntiDita[5]][2] or landmarkList[idPuntiDita[1]][2] >= landmarkList[idPuntiDita[5]][2]):
                cv2.rectangle(img, (20, 255), (330, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'okey', (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 6)
                # stampo immagine corrispondente
                h, w, c = ListOfImages[8].shape
                # print(h, w, c)
                img[0:h, 0:w] = ListOfImages[8]



    # give us the current time
    currentTIme = time.time()
    fps = 1 / (currentTIme - previousTime)  # framepersecond (fps)
    previousTime = currentTIme

    cv2.putText(img, f'FPS: {(int(fps))}', (400,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)


    cv2.imshow("Img", img)
    cv2.waitKey(1)