from app import app, recaptcha
from utils.email import enviar_correo
from flask import render_template, request, session, redirect
from models.usuario import Usuario
from dotenv import load_dotenv
import random
import string
import os
import yagmail
import threading


load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

@app.route("/")
def inicio():
    return render_template("frmIniciarSesion.html")

def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None):
    try:
        email.send(to=destinatario, subject=asunto, contents=mensaje)
    except Exception as error:
        print(str(error))

@app.route("/iniciarSesion2/",  methods=['POST'])
def iniciarSesion2():   
    mensaje = ""       
    if request.method=='POST':
        try:          
            username=request.form['txtUser']
            password=request.form['txtPassword'] 
            usuario = Usuario.objects(usuario=username,password=password).first()
            if usuario:
                session['user']=username
                session['user_name']=f"{usuario.nombres} {usuario.apellidos}"
                email = yagmail.SMTP("yesidortiz225@gmail.com",os.environ.get("PASSWORD-ENVIAR-CORREO"), 
                                     encoding="utf-8")
                asunto = "Ingreso al Sistema"
                mensaje = f"Cordial saludo {usuario.nombres} {usuario.apellidos}. \
                           Bienvenido a nuestro aplicativo"
                thread = threading.Thread(target=enviarCorreo,
                                          args=(email, usuario.correo, asunto, mensaje))
                thread.start()
                return redirect("/home/")
            else:
                mensaje="Credenciales no válidas"
        except Exception as error:
            mensaje=str(error)
    
        return render_template("frmIniciarSesion.html", mensaje=mensaje)




@app.route("/iniciarSesion/",  methods=['POST'])
def iniciarSesion():   
    mensaje = ""
    try:    
        if request.method=='POST':               
            if recaptcha.verify():           
                username=request.form['txtUser']
                password=request.form['txtPassword'] 
                usuario = Usuario.objects(usuario=username,password=password).first()
                if usuario:
                    session['user']=username
                    session['name_user']=f"{usuario.nombres} {usuario.apellidos}"
                    email = yagmail.SMTP("yesidortiz225@gmail.com",os.environ.get("PASSWORD-ENVIAR-CORREO"), 
                                     encoding="utf-8")
                    asunto = "Ingreso al Sistema"
                    mensaje = f"Cordial saludo <b>{usuario.nombres} {usuario.apellidos}.</b> \
                            Bienvenido a nuestro aplicativo Gestión peliculas. \
                            Enviamos Manual de usuario del aplicativo en formato pdf.<br><br>\
                            Cordialmente,<br><br><br> \
                            <b>Administración<br>Aplicativo Gestión Películas.</b>"
                    thread = threading.Thread(target=enviarCorreo,
                                            args=(email, [usuario.correo,"yesidortiz225@gmail.com"], asunto, [mensaje,"Manuales.pdf"]))
                    thread.start()
                    return redirect("/home/")
                else:
                    mensaje="Credenciales no válidas"
            else:
                mensaje = "Debe validar primero el recaptcha"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
    
    return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/usuario/", methods=['POST'])
def addUsuario():
    try:
        mensaje=None
        estado=False
        datos= request.get_json(force=True)
        usuario = Usuario(**datos)
        usuario.save()
        estado=True
        mensaje="Usuario agregado correctamente"       
        
    except Exception as error:
        mensaje=str(error) 
        
    return {"estado":estado, "mensaje":mensaje}


@app.route("/home/")
def home():
    if("user" in session):
        return render_template("contenido.html")
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/salir/")
def exit():
    session.clear()
    mensaje="Ha cerrado la sesión de forma"
    return render_template("frmIniciarSesion.html",mensaje=mensaje)
@app.route("/usuario/",methods=["GET"])
def listarUsuario():
    try:
        mensaje=None
        usuarios=Usuario.objects()
    except Exception as error:
        mensaje=str(error)
    return {"mensaje": mensaje,"usuarios": usuarios}



def generar_contraseña(n=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(n))

@app.route("/olvide", methods=["GET","POST"])
def recuperar():
    mensaje = ""
    try:
        if request.method == 'POST':
            usuario = request.form['txtusuario']
            correo_form = request.form['txtcorreo']

            # Verifica que el usuario exista
            user = Usuario.objects(usuario=usuario, correo=correo_form).first()
            if user:
                nueva_pass = generar_contraseña()
                user.password = nueva_pass  
                user.save()

                correo_envio = os.environ.get("EMAIL_USER")
                clave_envio = os.environ.get("EMAIL_PASS")
                email = yagmail.SMTP(user=correo_envio, password=clave_envio)
                asunto = "Recuperación de contraseña"
                mensaje = f"Hola {user.nombres}, tu nueva contraseña es: {nueva_pass}"

                email.send(to=user.correo, subject=asunto, contents=mensaje)
                return render_template("frmIniciarSesion.html", mensaje="Nueva contraseña enviada al correo")
            else:
                mensaje = "Usuario o correo incorrecto"
    except Exception as e:
        mensaje = str(e)

    return render_template("frmRecuperarContraseña.html", mensaje=mensaje)
    