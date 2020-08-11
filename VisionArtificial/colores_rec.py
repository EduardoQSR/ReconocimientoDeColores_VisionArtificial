from tkinter import *
import cv2
import numpy as np
import pyttsx3


window = Tk()  # Creamos un objeto de la clase Tk con el nombre de window
window.title("Reconocimiento de colores")  # Asignamos titulo a la interfaz
window.geometry('450x300')  # Definición de las dimensiones de la interfaz

engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Aquí puedes seleccionar la velocidad de la voz
engine.setProperty('voice', 'spanish')  # lenguaje de la voz a ejecutar


def habla(texto):
    engine.say(texto)
    engine.runAndWait()


def dibujar(mask, color, colors, frame, font):
    contornos, __ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  #  se encerrarán las áreas de color / le entregamos como primer argumento la imagen binaria, en nuestro caso mask , el segundo argumento indica que se tomarán en cuenta únicamente los contornos externos y finalmente con cv2.CHAIN_APPROX_SIMPLE , se indica que se guarden solo algunos puntos del contorno total.
    for c in contornos: #  Se recorre cada uno de los contornos encontrados con un for, ahora se analiza cada contorno (c).
        area = cv2.contourArea(c)  # determinamos el área en pixeles del contorno.
        if area > 3000: # deja pasar a los contornos que superen dicho valor, por lo tanto los más pequeños serán descartados
            M = cv2.moments(c)  #   Se encuentran los momentos del contorno
            if (M["m00"] == 0): M["m00"] = 1 #  se realiza una división para determinar las coordenadas
            x = int(M["m10"] / M["m00"])  #  encontrar los puntos centrales del contorno en x
            y = int(M['m01'] / M['m00']) #  encontrar los puntos centrales del contorno en y
            nuevoContorno = cv2.convexHull(c)
            cv2.circle(frame, (x, y), 7, (0, 255, 0), -1) # Aquí vamos a dibujar un círculo con cv2.circle, este va a ser dibujado en frame, en las coordenadas x e y encontradas, con un radio de 7 pixeles, de color verde que en BGR sería (0,255,0), finalmente con -1 especificamos que sea un círculo y no una circunferencia.
            cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 0.75, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)  #  Se dibujan los contornos
            habla(colors)


def Salir():
    window.destroy()


def Iniciar():
    cap = cv2.VideoCapture(0)

    azulBajo = np.array([100, 100, 20], np.uint8)
    azulAlto = np.array([125, 255, 255], np.uint8)

    verdeBajo = np.array([46, 100, 20], np.uint8)
    verdeAlto = np.array([75, 255, 255], np.uint8)

    redBajo1 = np.array([0, 100, 20], np.uint8)
    redAlto1 = np.array([5, 255, 255], np.uint8)

    redBajo2 = np.array([175, 100, 20], np.uint8)
    redAlto2 = np.array([179, 255, 255], np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, frame = cap.read() # Como este procedimiento se lo va a realizar a través de un video streaming, la imagen o fotograma que vamos a usar es frame, en la línea 11.
        if ret == True:
            frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # transformamos la imagen de BGR a HSV
            maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto) # obtenemos una imagen binaria
            maskVerde = cv2.inRange(frameHSV, verdeBajo, verdeAlto)
            maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
            maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
            maskRed = cv2.add(maskRed1, maskRed2)
            dibujar(maskAzul, (255, 0, 0), "color azul", frame, font)
            dibujar(maskVerde, (0, 128, 0), "color verde", frame, font)
            dibujar(maskRed, (0, 0, 255), "color rojo", frame, font)
            cv2.imshow('frame', frame)  #  visualizamos el frame
            if cv2.waitKey(1) & 0xFF == ord('e'):
                break
    cap.release()
    cv2.destroyAllWindows()
    #  cv2.destroyWindow()


btn_Reconocer_Color = Button(window, text="Iniciar", command=Iniciar)  # Botón para agregar texto
btn_Reconocer_Color.grid(column=0, row=0)


btn_Reconocer_Color = Button(window, text="Salir", command=Salir)  # Botón para agregar texto
btn_Reconocer_Color.grid(column=0, row=1)


window.mainloop()
