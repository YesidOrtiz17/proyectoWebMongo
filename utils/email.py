import yagmail
import os

def enviar_correo(destinatario, asunto, mensaje):
    try:
        email = yagmail.SMTP("yesidortiz225@gmail.com", os.environ.get("PASSWORD-ENVIAR-CORREO"))
        email.send(to=destinatario, subject=asunto, contents=mensaje)
    except Exception as e:
        print("Error al enviar correo:", e)
