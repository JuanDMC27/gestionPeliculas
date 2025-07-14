from flask import request, render_template
from models.genero import Genero
from app import app, db

@app.route('/')
def vistaInicio():
    return render_template("frmInicioSesion.html")

