from band_app.config.mysqlconnection import connectToMySQL
from flask import flash
from band_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re # el módulo regex
# crea un objeto de expresión regular que usaremos más adelante
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Usuarios:
    db_name="schema_banda"

    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls): #*!metodo para obtener todos los datos
        query = "SELECT * FROM usuarios;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        registro_usuarios =[]
        for x in results:
            registro_usuarios.append(cls(x))
        return registro_usuarios
    
    @classmethod
    def get_usuario(cls, data): #*!obtenemos un usuario mediante su id
        query = "SELECT * FROM usuarios WHERE id= %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data )
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data): #*!recibir por correo electronico
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        # no se encontró un usuario coincidente
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls,data): #*!guardar informacion en la bd
        query = "INSERT INTO usuarios (nombre, apellido, email, password) VALUES (%(nombre)s,%(apellido)s,%(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_form(registro): #*!validamos la informacion que ingresa el usuario en el formulario
        # los métodos estáticos no tienen self o cls pasados a los parámetros
        correo = {
            'email':registro['email']
        }
        is_valid = True # asumimos que esto es true
        if len(registro['nombre']) < 2:
            flash("Nombre debe contener al menos 2 caracteres.")
            is_valid = False
        if len(registro['apellido']) < 2:
            flash("Apellido debe contener al menos 2 caracteres.")
            is_valid = False
        if not EMAIL_REGEX.match(correo['email']): 
            flash("Direccion de correo electronico no valida!")
            is_valid = False
        elif Usuarios.get_by_email(correo):
            flash("Direccion de correo ya existente!")
            is_valid = False
        if len(registro['password']) < 8:
            flash("Contraseña insegura: debe tener al menos 8 caracteres")
            is_valid = False
        if registro['password'] != registro['password_confirm']:
            flash('Passwords no coinciden')
            is_valid = False
        return is_valid