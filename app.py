from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os
from google_recaptcha_flask import ReCaptcha

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.secret_key = "1234567890aeiou"

uri="mongodb+srv://yesidortiz225:jLkLTfKRRCwIIkGs@cluster0.n4ffy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

app.config['MONGODB_SETTINGS'] = {
    'db': 'GestionPeliculas',
    'host': uri,
   
}

#configurar recaptcha
app.config['GOOGLE_RECAPTCHA_ENABLED'] =True
app.config['GOOGLE_RECAPTCHA_SITE_KEY'] = os.environ.get("RECAPTCHA_SITE_KEY")  # Sustituye por tu clave pública
app.config['GOOGLE_RECAPTCHA_SECRET_KEY'] = os.environ.get("RECAPTCHA_SECRET_KEY") # Sustituye por tu clave secreta

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

#crear objeto detipo Recaptcha
recaptcha = ReCaptcha(app)

#Crear objeto de tipo MonoEngine
db = MongoEngine(app)


from routes.usuario import *
from routes.genero import *
from routes.pelicula import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


