from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from routes.genero import ruta_genero
from routes.pelicula import ruta_pelicula
from routes.usuario import ruta_usuario
from flask_cors import CORS 


load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = "misuperclave123456!@#$"
app.register_blueprint(ruta_genero)
app.register_blueprint(ruta_pelicula)
app.register_blueprint(ruta_usuario)

app.config['UPLOAD_FOLDER'] = './static/images/'
app.config['MONGODB_SETTINGS'] = [
    {
        'db': 'gestionPeliculas',
        'host': os.environ.get("URI"),
        # 'port': 27017,
    }
]

db = MongoEngine(app)

if __name__ == '__main__':
    from routes.genero import *
    from routes.pelicula import * 
    from routes.usuario import *
    
    app.run(port='5400', host='0.0.0.0', debug=True)