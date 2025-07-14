# utils/email.py
import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def enviar_correo(destinatario, asunto, mensaje):
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    yag.send(to=destinatario, subject=asunto, contents=mensaje)
