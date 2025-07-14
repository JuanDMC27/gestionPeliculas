from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario import Usuario
import requests

ruta_usuario = Blueprint('ruta_usuario', __name__)

@ruta_usuario.route('/frmInicioSesion', methods=['GET'])
def mostrar_frmInicioSesion():
    return render_template("frmInicioSesion.html")

@ruta_usuario.route('/login', methods=['GET'])
def mostrar_login():
    return render_template("frmInicioSesion.html")

@ruta_usuario.route('/iniciarsesion/', methods=['POST'])
def iniciar_sesion():
    usuario = request.form.get('txtuser')
    contraseña = request.form.get('txtPassword')
    token = request.form.get('g-recaptcha-response')

    if not token:
        mensaje = "Verifica el reCAPTCHA antes de continuar."
        return render_template("frmInicioSesion.html", mensaje=mensaje)

    
    secret = '6Lc4KYIrAAAAAGna7C3rGm-SYfTr72GF8f-COu_1'
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': secret, 'response': token}
    ).json()

    if not response.get('success'):
        mensaje = "Falló la validación de reCAPTCHA"
        return render_template("frmInicioSesion.html", mensaje=mensaje)

    user = Usuario.objects(usuario=usuario, password=contraseña).first()
    if user:
        session['user'] = usuario
        return redirect(url_for('ruta_pelicula.inicio'))
    else:
        mensaje = "Credenciales incorrectas"
        return render_template("frmInicioSesion.html", mensaje=mensaje)


@ruta_usuario.route("/registrar", methods=["GET", "POST"])
def registrar():
    mensaje = ""
    if request.method == "POST":
        try:
            nuevo_usuario = Usuario(
                usuario=request.form["txtUser"],
                password=request.form["txtPassword"],
                nombres=request.form["txtNombres"],
                apellidos=request.form["txtApellidos"],
                correo=request.form["txtCorreo"]
            )
            nuevo_usuario.save()
            mensaje = "Usuario registrado exitosamente"
        except Exception as e:
            mensaje = f"Error: {str(e)}"
    return render_template("frmRegistro.html", mensaje=mensaje)


@ruta_usuario.route("/logout")
def logout():
    session.clear()
    mensaje = "Sesión cerrada exitosamente"
    return redirect(url_for('ruta_usuario.mostrar_frmInicioSesion'))
