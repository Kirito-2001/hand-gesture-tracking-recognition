import cv2
import mediapipe as mp
import time


# ref: https://stackoverflow.com/questions/69780732/getting-errors-with-opencv-and-mediapipe-for-making-hand-tracking-module-in-pyth

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity = 1,  detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.complexity = complexity
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.complexity, self.detectionConfidence, self.trackConfidence)

        # metodo di mideapipe per disegnare linea mano
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # mandare la nostra RGB image all'hands
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #convertiamo BGR in RGB perche hands utilizza RGBS
        self.results = self.hands.process(imgRGB) #processo il frame
        # print(results.multi_hand_landmarks) #result di suo è statico, non fa nulla, quindi mettiamo la gestione della ricezione della mano

        if self.results.multi_hand_landmarks:
            for hand_marks in self.results.multi_hand_landmarks:
                if draw:
                    #metodo di mideapipe per disegnare linea mano e connettere i punti
                    self.mpDraw.draw_landmarks(img,hand_marks, self.mpHand.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNumber=0, draw=True):
        landMarkList =[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id, landMark in enumerate(myHand.landmark):
                # print(id,landMark)
                height, width, chanels = img.shape # mi da in pixel le dimensioni dell'immagine
                # landmark non è in pixel, ma è decimale,allora lo trasformo in intero e poi lo setto come pixel
                cx, cy = int(landMark.x * width), int(landMark.y * height)
                # print(id,cx,cy)
                landMarkList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        return landMarkList


def main():
    previousTime = 0
    currentTIme = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        landMarkList = detector.findPosition(img)
        #if len(landMarkList) != 0:
        #    print(landMarkList[4])
        # give us the current time
        currentTIme = time.time()
        fps = 1 / (currentTIme - previousTime)  # framepersecond (fps)
        previousTime = currentTIme

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
           # display the image
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":  # se sto runnando questo script fai la funzione main()
    main()
