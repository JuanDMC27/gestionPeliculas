from bson import ObjectId
from flask import request
from models.pelicula import Pelicula
from app import app, db
from models.genero import Genero

@app.route('/pelicula/', methods=['POST'])
def addPelicula():
    try:
        mensaje = None
        estado = False
        if(request.method == 'POST'):
            datos= request.get_json(force=True)
            genero = Genero.objects(nombre=datos['genero']).first()
            print(genero)
            if genero is not None:
                pelicula = Pelicula(**datos)
                pelicula.save()
                estado = True
                mensaje = 'Pelicula agregada correctamente'
            else:
                mensaje = 'No se puede agregar el genero no existe'
        else:
            mensaje = 'No permitido'
        
    except Exception as error:
        mensaje=str(error)
        
    return {'estado': estado, 'mensaje': mensaje}

@app.route("/pelicula/", methods=['GET'])
def listaPeliculas():
    try:
        mensaje= None
        peliculas = Pelicula.objects()
        
        
    except Exception as error:
        mensaje = str(error)
    
    return {'peliculas': peliculas, 'mensaje': mensaje}

@app.route('/pelicula/', methods=['PUT'])
def updatePelicula():
    try:
        mensaje = None
        estado= False
        if request.method == 'PUT':
            datos = request.get_json(force=True)
            pelicula = Pelicula.objects(id=ObjectId(datos['id'])).first()
            if pelicula is not None:
                pelicula.codigo = datos['codigo']
                pelicula.titulo = datos['titulo']
                pelicula.protagonista = datos['protagonista']
                pelicula.duracion = datos['duracion']
                pelicula.resumen = datos['resumen']
                pelicula.foto = datos['foto']
                genero = Genero.objects(nombre=datos['genero']).first()
                pelicula.save()
                estado= True
                mensaje = 'Pelicula actualizada...'
            else:
                mensaje = 'No existe pelicula con el id para actualizar'
        
    except Exception as error:
        mensaje = str(error)
    
    return {'estado': estado, 'mensaje': mensaje}

@app.route('/pelicula/', methods=['DELETE'])
def deletePelicula():
    try:
        mensaje = None
        estado= False
        if request.method == 'DELETE':
            datos = request.get_json(force=True)
            pelicula = Pelicula.objects(id=ObjectId(datos['id'])).first()
            if pelicula is not None:
                pelicula.delete()
                estado= True
                mensaje = 'Pelicula eliminada...'
            else:
                mensaje = 'No existe pelicula con el id para eliminar'
        
    except Exception as error:
        mensaje = str(error)
    
    return {'estado': estado, 'mensaje': mensaje}