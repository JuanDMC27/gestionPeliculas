from bson import ObjectId
from flask import Blueprint, request, render_template, session, redirect, url_for, jsonify
from models.pelicula import Pelicula
from models.genero import Genero
import yagmail
import os


ruta_pelicula = Blueprint('ruta_pelicula', __name__)

@ruta_pelicula.route('/', endpoint='inicio')
def vistaPeliculas():
    if 'user' not in session:
        return redirect(url_for('ruta_usuario.mostrar_login'))  # redirige si no ha iniciado sesión
    return render_template("contenido.html")
@ruta_pelicula.route('/pelicula/enviar-correo', methods=['POST'])
def enviar_correo():
    datos = request.get_json()
    correo = datos['correo']
    id_pelicula = datos['pelicula_id']

    try:
        p = Pelicula.objects(id=ObjectId(id_pelicula)).first()

        if not p:
            return {'estado': False, 'mensaje': 'Película no encontrada'}

        yag = yagmail.SMTP(user=os.getenv("EMAIL_USER"), password=os.getenv("EMAIL_PASS"))

        contenido = f"""
        <h2>¡Te invitamos a ver una gran película!</h2>
        <p>Hola,</p>
        <p>Queremos recomendarte la película <strong>{p.titulo}</strong>.</p>
        <ul>
            <li><strong>Protagonista:</strong> {p.protagonista}</li>
            <li><strong>Duración:</strong> {p.duracion} minutos</li>
            <li><strong>Resumen:</strong> {p.resumen}</li>
        </ul>
        <p>¡No te la pierdas! 🍿🎬</p>
        """

        yag.send(
            to=correo,
            subject=f"Invitación: Mira '{p.titulo}'",
            contents=contenido
        )

        return {'estado': True, 'mensaje': 'Correo enviado correctamente'}
    except Exception as e:
        return {'estado': False, 'mensaje': f'Error al enviar: {str(e)}'}





@ruta_pelicula.route('/peliculas', endpoint='peliculas')
def vistaPeliculasListado():
    return render_template("peliculas.html")


@ruta_pelicula.route('/pelicula/', methods=['POST'])
def addPelicula():
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        genero = Genero.objects(nombre=datos['genero']).first()
        if genero is not None:
            pelicula = Pelicula(
                codigo=datos['codigo'],
                titulo=datos['titulo'],
                protagonista=datos['protagonista'],
                duracion=datos['duracion'],
                resumen=datos['resumen'],
                foto=datos.get('foto', '')
            )
            pelicula.genero = genero
            pelicula.save()
            estado = True
            mensaje = 'Película agregada correctamente'
        else:
            mensaje = 'No se puede agregar: el género no existe.'
    except Exception as error:
        mensaje = str(error)

    return {'estado': estado, 'mensaje': mensaje}


@ruta_pelicula.route("/pelicula/", methods=['GET'])
def listaPeliculas():
    if "user" in session:
        try:
            mensaje = None
            peliculas = Pelicula.objects()
            lista = []

            for p in peliculas:
                try:
                    genero_nombre = p.genero.nombre if p.genero else "Sin género"
                except Exception:
                    genero_nombre = "Sin género"

                lista.append({
                    'id': str(p.id),
                    'codigo': p.codigo,
                    'titulo': p.titulo,
                    'protagonista': p.protagonista,
                    'duracion': p.duracion,
                    'resumen': p.resumen,
                    'foto': p.foto,
                    'genero': {'nombre': genero_nombre}
                })
        except Exception as error:
            mensaje = str(error)
            lista = []

        return {'peliculas': lista, 'mensaje': mensaje}
    else:
        return {'mensaje': 'Credenciales no válidas', 'peliculas': []}


@ruta_pelicula.route("/pelicula/recientes", methods=["GET"])
def peliculasRecientes():
    try:
        peliculas = Pelicula.objects().order_by('-id').limit(10)
        lista = [{
            'id': str(p.id),
            'foto': p.foto,
            'titulo': p.titulo,
        } for p in peliculas]
        return {'peliculas': lista}
    except Exception as e:
        return {'mensaje': str(e), 'peliculas': []}


@ruta_pelicula.route('/pelicula/', methods=['PUT'])
def updatePelicula():
    try:
        mensaje = None
        estado = False
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
            pelicula.genero = genero
            pelicula.save()
            estado = True
            mensaje = 'Película actualizada...'
        else:
            mensaje = 'No existe película con el ID para actualizar'
    except Exception as error:
        mensaje = str(error)

    return {'estado': estado, 'mensaje': mensaje}


@ruta_pelicula.route('/pelicula/', methods=['DELETE'])
def deletePelicula():
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        pelicula = Pelicula.objects(id=ObjectId(datos['id'])).first()
        if pelicula is not None:
            pelicula.delete()
            estado = True
            mensaje = 'Película eliminada...'
        else:
            mensaje = 'No existe película con el ID para eliminar'
    except Exception as error:
        mensaje = str(error)

    return {'estado': estado, 'mensaje': mensaje}
