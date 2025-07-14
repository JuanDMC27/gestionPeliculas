from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = MongoEngine()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = "misuperclave123456!@#$"
    CORS(app)

    app.config['UPLOAD_FOLDER'] = './static/images/'
    app.config['MONGODB_SETTINGS'] = [{
        'db': 'gestionPeliculas',
        'host': os.environ.get("URI"),
    }]

    db.init_app(app)

    # Importar y registrar Blueprints
    from app.routes.genero import ruta_genero
    from app.routes.pelicula import ruta_pelicula
    from app.routes.usuario import ruta_usuario

    app.register_blueprint(ruta_genero)
    app.register_blueprint(ruta_pelicula)
    app.register_blueprint(ruta_usuario)

    return app
