from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = MongoEngine()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.getenv("SECRET_KEY", "clave_default_segura")
    app.config['UPLOAD_FOLDER'] = './static/images/'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'gestionPeliculas',
        'host': os.getenv("URI")
    }

    db.init_app(app)

    # Registro de Blueprints
    from app.routes.genero import ruta_genero
    from app.routes.pelicula import ruta_pelicula
    from app.routes.usuario import ruta_usuario

    app.register_blueprint(ruta_genero)
    app.register_blueprint(ruta_pelicula)
    app.register_blueprint(ruta_usuario)

    return app
