import sqlite3
from sqlite3 import Error

class Database:
    """
    Modelo base para interactuar con una base de datos en SQLite
    Consta de metodos para crear tablas y CRUD de datos 
    """
    def __init__(self, database):
        self.conn = self.__create_connection(database)

    def __create_connection(self, database):
        """ Crear la conexion con la base de datos """
        conn = None
        try:
            conn = sqlite3.connect(database)
            return conn
        except Error as e:
            print("Error de conexión con BD:", e)
        
        return conn

    def _create_table(self, create_table_sql):
        """ Metodo para crear tablas """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print("Error en la creación de tabla: ", create_table_sql)
            raise Error(e)

    def _insert(self, sql, *values):
        """ Metodo para insertar datos y devolver el id del ultimo insertado """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            return cur.lastrowid
        except Error as e:
            print("Error al insertar:", sql, values)
            raise Error(e)

    def _update(self, sql, *values):
        """ Metodo para actualizar datos """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
        except Error as e:
            print("Error al actualizar:", sql, values)
            raise Error(e)

    def _select(self, sql, *values):
        """ Metodo para retornar un arreglo de filas """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            rows = cur.fetchall()
            return rows
        except Error as e:
            print("Error al seleccionar:", sql, values)
            raise Error(e)

    def _delete(self, sql, *values):
        """ Metodo para eliminar datos """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
        except Error as e:
            print("Error al eliminar:", sql, values)
            raise Error(e)

class PizzeriaDatabase(Database):
    """ Modelo especifico para la Base de Datos de la Pizzeria """
    def __init__(self, database):
        super().__init__(database)

    def create_project_tables_if_not_exists(self):
        """ Creacion de las tablas de la base de datos si no existen """

        sql_tables = list()
        sql_project_table = """ CREATE TABLE IF NOT EXISTS usuario (
                                    id INTEGER PRIMARY KEY,
                                    nombre TEXT NOT NULL); """
        sql_tables.append(sql_project_table)
        
        sql_project_table = """ CREATE TABLE IF NOT EXISTS pedido (
                                    id INTEGER PRIMARY KEY,
                                    fecha TEXT NOT NULL,
                                    precio_total REAL,
                                    fk_usuario INTEGER NOT NULL,
                                    FOREIGN KEY (fk_usuario)
                                        REFERENCES usuario (id)); """
        sql_tables.append(sql_project_table)

        sql_project_table = """ CREATE TABLE IF NOT EXISTS pizza (
                                    id INTEGER PRIMARY KEY,
                                    tamanio TEXT NOT NULL,
                                    precio_base REAL); """
        sql_tables.append(sql_project_table)

        sql_project_table = """ CREATE TABLE IF NOT EXISTS ingrediente (
                                    id INTEGER PRIMARY KEY,
                                    nombre TEXT NOT NULL,
                                    tamanio TEXT NOT NULL,
                                    precio REAL); """
        sql_tables.append(sql_project_table)

        sql_project_table = """ CREATE TABLE IF NOT EXISTS detalle (
                                    numero_pedido INTEGER NOT NULL,
                                    fk_pedido INTEGER NOT NULL,
                                    fk_pizza INTEGER NOT NULL,
                                    fk_ingrediente INTEGER,
                                    FOREIGN KEY (fk_pedido)
                                        REFERENCES pedido (id),
                                    FOREIGN KEY (fk_pizza)
                                        REFERENCES pizza (id),
                                    FOREIGN KEY (fk_ingrediente)
                                        REFERENCES ingrediente (id)); """
        sql_tables.append(sql_project_table)

        # Crear las tablas
        for sql in sql_tables:
            self._create_table(sql)

    def insert_usuario(self, nombre):
        """ Insertar un usuario dado su nombre """
        sql = """ INSERT INTO usuario(nombre) VALUES(?) """
        return self._insert(sql, nombre)

    def insert_pedido(self, fk_usuario, fecha, precio_total = None):
        """ Insertar un pedido dato el usuario, fecha y precio total """
        sql = """ INSERT INTO pedido(fecha, precio_total, fk_usuario) VALUES(?, ?, ?) """
        return self._insert(sql, fecha, precio_total, fk_usuario)

    def insert_pizza(self, tamanio, precio_base):
        """ Insertar una pizza dado su tamanio y precio base """
        sql = """ INSERT INTO pizza(tamanio, precio_base) VALUES(?, ?) """
        return self._insert(sql, tamanio, precio_base)

    def insert_ingrediente(self, nombre, tamanio, precio):
        """ Insertar ingrediente dado su nombre, tamanio y precio """
        sql = """ INSERT INTO ingrediente(nombre, tamanio, precio) VALUES(?, ?, ?) """
        return self._insert(sql, nombre, tamanio, precio)

    def insert_detalle(self, numero_pedido, fk_pedido, fk_pizza, fk_ingrediente = None):
        """ Insertar detaller de la ralacion entre pedido, pizza e ingrediente """
        sql = """ INSERT INTO detalle(numero_pedido, fk_pedido, fk_pizza, fk_ingrediente) VALUES(?, ?, ?, ?) """
        return self._insert(sql, numero_pedido, fk_pedido, fk_pizza, fk_ingrediente)

    def update_precio_pedido(self, id_pedido, precio_total):
        """ 
        Actualizar el precio del pedido 
        Se calcula despues de insertar todos los ingredientes a la pizza en el detalle
        """
        sql = """ UPDATE pedido SET precio_total = ? WHERE id = ? """
        self._update(sql, precio_total, id_pedido)

    def select_pizzas(self):
        """ Seleccionar todas las pizzas """
        sql = "SELECT * FROM pizza"
        return self._select(sql)

    def select_ingredientes(self):
        """ Seleccionar todos los ingredientes """
        sql = "SELECT * FROM ingrediente"
        return self._select(sql)

    def select_pizzas_where(self, tamanio):
        """ Seleccionar varias pizzas dado un tamaño """
        sql = "SELECT * FROM pizza WHERE tamanio = ?"
        return self._select(sql, tamanio)

    def select_ingredientes_where(self, tamanio, nombre):
        """ Seleccionar varios ingrediente dado su tamaño y nombre """
        sql = "SELECT * FROM ingrediente WHERE tamanio = ? AND nombre = ?"
        return self._select(sql, tamanio, nombre)

    def select_1_detalle(self):
        """ Petición sencilla para validar si hay datos en la BD """
        sql = """ SELECT * FROM detalle LIMIT 1"""
        return self._select(sql)
    
    def select_all_data(self):
        """ Seleccionar todos los datos importantes de la base de datos con JOIN de tablas """
        sql = """
            SELECT u.nombre, pe.fecha, pe.precio_total, d.numero_pedido, pi.tamanio, i.nombre 
            FROM detalle AS d
                LEFT OUTER JOIN ingrediente AS i ON d.fk_ingrediente = i.id
                JOIN pizza AS pi ON d.fk_pizza = pi.id
                JOIN pedido AS pe ON d.fk_pedido = pe.id
                JOIN usuario AS u ON pe.fk_usuario = u.id
            """
        return self._select(sql)
    
    def select_all_database(self):
        """ Seleccionar todos los datos de la base de datos, se usa para debbugin """
        sql = """
            SELECT u.id, u.nombre, pe.id, pe.fecha, pe.precio_total, d.numero_pedido, pi.id, pi.tamanio, i.id, i.nombre 
            FROM detalle AS d
                LEFT OUTER JOIN ingrediente AS i ON d.fk_ingrediente = i.id
                JOIN pizza AS pi ON d.fk_pizza = pi.id
                JOIN pedido AS pe ON d.fk_pedido = pe.id
                JOIN usuario AS u ON pe.fk_usuario = u.id
            """
        return self._select(sql)
