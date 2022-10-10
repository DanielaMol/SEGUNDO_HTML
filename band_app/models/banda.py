from band_app.config.mysqlconnection import connectToMySQL
from flask import flash
from band_app.models.usuario import Usuarios

class Bandas:
    db_name="schema_banda"

    def __init__( self , data ):
        self.id = data['id']
        self.nombre_banda = data['nombre_banda']
        self.genero_musical = data['genero_musical']
        self.ciudad_origen = data['ciudad_origen']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.usuario = []

    @classmethod
    def get_all(cls): #*!metodo para obtener todos los datos de la tabla de bd
        query = "SELECT * FROM bandas;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        registro_bandas =[]
        for x in results:
            registro_bandas.append(cls(x))
        return registro_bandas
    
    @classmethod
    def get_banda(cls, data): #*!obtenemos una banda mediante su id
        query = "SELECT * FROM bandas WHERE id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data )
        return cls(result[0])

    @classmethod
    def guardar_banda(cls,data): #*!guardar informacion en la table bandas de la bd
        query = "INSERT INTO bandas (nombre_banda, genero_musical, ciudad_origen, created_at, updated_at, usuario_id) VALUES (%(nombre_banda)s,%(genero_musical)s,%(ciudad_origen)s, NOW(), NOW(), %(usuario_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def banda_usuario(cls):
        query = "SELECT * FROM bandas JOIN usuarios ON bandas.usuario_id = usuarios.id;"
        result = connectToMySQL(cls.db_name).query_db(query)
        todas_las_bandas = []
        for banda in result:
            objeto_banda = cls(banda)
            objeto_banda.usuario.append(Usuarios(banda))
            todas_las_bandas.append(objeto_banda)
        return todas_las_bandas
    
    @classmethod
    def eliminar(cls,data): #*!metodo para eliminar informacion de la bd
        query  = "DELETE FROM bandas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def actualizar(cls,data):
        query = "UPDATE bandas SET nombre_banda=%(nombre_banda)s, genero_musical=%(genero_musical)s, ciudad_origen=%(ciudad_origen)s WHERE id=%(banda_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_banda(registro_banda): #*!validamos la informacion que ingresa el usuario en el formulario
        # otros métodos Burger más allá
        # los métodos estáticos no tienen self o cls pasados a los parámetros
        # necesitamos tomar un parámetro para representar
        is_valid = True # asumimos que esto es true
        if len(registro_banda['nombre_banda']) < 2:
            flash("Nombre de la banda contener al menos 2 caracteres.")
            is_valid = False
        if len(registro_banda['genero_musical']) < 2:
            flash("Genero musical inválido! debe contener al menos 2 caracteres.")
            is_valid = False
        if len(registro_banda['ciudad_origen']) < 4:
            flash("Ciudad de origen inválida! debe contener al menos 4 caracteres")
            is_valid = False
        return is_valid