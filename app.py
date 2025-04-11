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


app.config['MONGODB_SETTINGS'] = {
    'db': 'GestionPeliculas',
    'host': os.environ.get("URI"),
   
}


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


