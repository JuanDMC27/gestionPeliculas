from bson import ObjectId
from flask import Blueprint, request, render_template, session, redirect, url_for
from app.models.genero import Genero


ruta_genero = Blueprint('ruta_genero', __name__)


@ruta_genero.route('/generos')
def vistaGeneros():
    if 'user' not in session:
        return redirect(url_for('ruta_usuario.mostrar_login')) 
    return render_template("generos.html")



@ruta_genero.route("/genero/", methods=['GET'])
def listarGeneros():
    try:
        mensaje = None
        generos = Genero.objects()
        lista = [{'_id': str(g.id), 'nombre': g.nombre} for g in generos]
    except Exception as error:
        mensaje = str(error)
        lista = []

    return {'mensaje': mensaje, 'generos': lista}


@ruta_genero.route('/genero/', methods=['POST'])
def addGenero():
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        nombre = datos['nombre'].strip()
        genero_existente = Genero.objects(nombre=nombre).first()

        if genero_existente:
            mensaje = 'El género ya existe'
        else:
            nuevo_genero = Genero(nombre=nombre)
            nuevo_genero.save()
            estado = True
            mensaje = 'Género agregado correctamente'

    except Exception as error:
        mensaje = str(error)

    return {'estado': estado, 'mensaje': mensaje}


@ruta_genero.route('/genero/', methods=['PUT'])
def updateGenero():
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        genero = Genero.objects(id=ObjectId(datos['id'])).first()
        if genero:
            genero.nombre = datos['nombre']
            genero.save()
            estado = True
            mensaje = 'Género actualizado con éxito'
        else:
            mensaje = 'No se encontró el género'
    except Exception as error:
        mensaje = str(error)

    return {'estado': estado, 'mensaje': mensaje}


@ruta_genero.route('/genero/', methods=['DELETE'])
def deleteGenero():
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        genero = Genero.objects(id=ObjectId(datos['id'])).first()
        if genero:
            genero.delete()
            estado = True
            mensaje = 'Género eliminado'
        else:
            mensaje = 'No existe este género'
    except Exception as error:
        mensaje = str(error)

    return {'estado': estado, 'mensaje': mensaje}
