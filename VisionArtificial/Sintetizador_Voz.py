import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 130)  # Aquí puedes seleccionar la velocidad de la voz
engine.setProperty('voice', 'spanish')  # lenguaje de la voz a ejecutar


def habla(texto):
    engine.say(texto)
    engine.runAndWait()


while 1:
    frase_decir = input("--> ")
    if frase_decir == "exit":
        exit(0)
    habla(frase_decir)
