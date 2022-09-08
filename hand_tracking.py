import cv2
import mediapipe as mp
import time  # to check frame rate

cap = cv2.VideoCapture(0) # catturare video del mio (0) computer

mpHand = mp.solutions.hands
hands = mpHand.Hands()

# metodo di mideapipe per disegnare linea mano
mpDraw = mp.solutions.drawing_utils

previousTime = 0
currentTIme = 0

while True:
    success, img = cap.read()

    # mandare la nostra RGB image all'hands
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convertiamo BGR in RGB perche hands utilizza RGBS
    results = hands.process(imgRGB) #processo il frame
    # print(results.multi_hand_landmarks)
    #   |-->result di suo è statico, non fa nulla, quindi mettiamo la gestione della ricezione della mano

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landMark in enumerate(hand_landmarks.landmark):
                # print(id,landMark)
                height, width, chanels = img.shape
                # landmark non è in pixel, ma è decimale,allora lo trasformo in int e poi lo setto come pixel
                cx, cy = int(landMark.x*width), int(landMark.y*height)
                # print(id,cx,cy)

                if id == 0: # -->ogni id è un punto della mano,==>creo modulo riutilizzabile per gestire hand tracking
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            # metodo di mideapipe per disegnare linea mano e connettere i punti
            mpDraw.draw_landmarks(img, hand_landmarks, mpHand.HAND_CONNECTIONS)

    # give us the current time
    currentTIme = time.time()
    fps = 1/(currentTIme-previousTime) #framepersecond (fps)
    previousTime = currentTIme

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)

    # display the image
    cv2.imshow("Image", img)
    cv2.waitKey(1)


