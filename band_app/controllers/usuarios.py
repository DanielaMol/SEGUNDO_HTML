from band_app import app
from flask_bcrypt import Bcrypt
from flask import request,flash,render_template,redirect,session
from band_app.controllers import bandas
from band_app.models.usuario import Usuarios
from band_app.models.banda import Bandas


bcrypt = Bcrypt(app)

@app.route('/') #*!Ruta raiz
def raiz():
    return render_template("registro_login.html")

@app.route('/add_usuario', methods=['POST']) #*!Ruta para añadir un usuario
def register():
    # validar el formulario aquí...
    if not Usuarios.validate_form(request.form):
        return render_template("registro_login.html", action='register')
    # if request.form['password'] != request.form['password_confirm']:
    #     flash('Passwords no coinciden')
    #     return redirect('/')

    # crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    #poner pw_hash en el diccionario de datos
    data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # llama al @classmethod de guardado en Usuario
    user_id = Usuarios.save(data)
    # almacenar id de usuario en la sesión
    session['user_id'] = user_id
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/login', methods=['POST']) #*!ruta para hacer login
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = { "email" : request.form["email"] }
    user_in_db = Usuarios.get_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
        flash("Invalid Email/Password")
        return render_template("registro_login.html", action='login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # si obtenemos False después de verificar la contraseña
        flash("Invalid Email/Password")
        return render_template("registro_login.html", action='login')
    # si las contraseñas coinciden, configuramos el user_id en sesión
    session['user_id'] = user_in_db.id
    # ¡¡¡Nunca renderices en una post!!!
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/clearsession') #*!ruta para limpiar sesion, usuario hacer logout
def clear():
    session.clear()
    return redirect('/')

@app.route('/dashboard/<int:id>')
def presentar_info(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    obtener_usuario = Usuarios.get_usuario(data)
    usuarios_con_bandas = Bandas.banda_usuario()
    print(usuarios_con_bandas)
    return render_template('dashboard.html', obtener_usuario=obtener_usuario, usuarios_con_bandas=usuarios_con_bandas)

@app.route('/misbandas')
def mi_bandas():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id':session['user_id']
    }
    obtener_usuario = Usuarios.get_usuario(data)
    banda_usuario = Bandas.banda_usuario()
    return render_template('mis_bandas.html', obtener_usuario=obtener_usuario, banda_usuario=banda_usuario)

@app.route('/banda')
def mostrar_banda():
    if 'user_id' not in session:
        return redirect("/")
    return render_template('registro_banda.html')

@app.route('/add_banda', methods=['POST']) #*!Ruta para añadir una banda
def registrar_banda():
    banda_id = Bandas.guardar_banda(request.form)
    return redirect(f'/dashboard/{banda_id}')

@app.route('/destroy')
def eliminar():
    data = {
        'id':id
    }
    Bandas.eliminar(data)
    return redirect(f'/dashboard/{session["user_id"]}')

@app.route('/editar/<int:banda_id>')
def editar_banda(banda_id):
    if 'user_id' not in session:
        return redirect("/")

    data = {
        'id':banda_id
    }
    #usuario_ingreso = Usuarios.get_usuario(data)
    obtener_usuario = Usuarios.get_usuario(data)
    bandas_con_usuarios = Bandas.banda_usuario()
    return render_template('editar_banda.html', bandas_con_usuarios=bandas_con_usuarios, obtener_usuario=obtener_usuario)

@app.route('/editar/<int:banda_id>', methods=['POST'])
def editar(banda_id):
    if 'user_id' not in session:
        return redirect("/")
    #usuario_ingreso = Usuarios.get_usuario(data)
    Bandas.actualizar(request.form)
    return redirect('/bandas')