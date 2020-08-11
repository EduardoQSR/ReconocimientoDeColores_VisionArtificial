import cv2
import numpy as np

import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Aquí puedes seleccionar la velocidad de la voz
engine.setProperty('voice', 'spanish')  # lenguaje de la voz a ejecutar


def habla(texto):
    engine.say(texto)
    engine.runAndWait()

var = ""


def dibujar(mask: object, color: object) -> object:
    contornos, __ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        assert isinstance(c, object)
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if (M["m00"] == 0): M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])
            nuevoContorno = cv2.convexHull(c)
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1)
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)


cap = cv2.VideoCapture(0)
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

amarilloBajo = np.array([46, 100, 20], np.uint8)
amarilloAlto = np.array([75, 255, 255], np.uint8)

redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)
redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    if ret:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)

        maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)

        maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1, maskRed2)
        dibujar(maskAzul, (255, 0, 0))
        habla("azul")
        dibujar(maskAmarillo, (0, 128, 0))
        habla("verde")
        dibujar(maskRed, (0, 0, 255))
        habla("rojo")
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

cap.release()
cv2.destroyAllWindows()
