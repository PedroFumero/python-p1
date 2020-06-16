import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, database):
        self.conn = self.create_connection(database)

    def create_connection(self, database):
        """ Crear la conexion con la base de datos """
        conn = None
        try:
            conn = sqlite3.connect(database)
            return conn
        except Error as e:
            print(e)
        
        return conn

    def create_table(self, create_table_sql):
        """ Metodo para crear tablas """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_tables_if_not_exists(self):
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

        for sql in sql_tables:
            self.create_table(sql)

    def insert(self, sql, *values):
        cur = self.conn.cursor()
        cur.execute(sql, values)
        return cur.lastrowid

    def insert_usuario(self, nombre):
        sql = """ INSERT INTO usuario(nombre) VALUES(?) """
        return self.insert(sql, nombre)

    def insert_pedido(self, fk_usuario, fecha, precio_total = None):
        sql = """ INSERT INTO pedido(fecha, precio_total, fk_usuario) VALUES(?, ?, ?) """
        return self.insert(sql, fecha, precio_total, fk_usuario)

    def insert_pizza(self, tamanio, precio_base):
        sql = """ INSERT INTO pizza(tamanio, precio_base) VALUES(?, ?) """
        return self.insert(sql, tamanio, precio_base)

    def insert_ingrediente(self, nombre, tamanio, precio):
        sql = """ INSERT INTO ingrediente(nombre, tamanio, precio) VALUES(?, ?, ?) """
        return self.insert(sql, nombre, tamanio, precio)

    def insert_detalle(self, fk_pedido, fk_pizza, fk_ingrediente = None):
        sql = """ INSERT INTO detalle(fk_pedido, fk_pizza, fk_ingrediente) VALUES(?, ?, ?) """
        return self.insert(sql, fk_pedido, fk_pizza, fk_ingrediente)

    def update(self, sql, *values):
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()

    def update_precio_pedido(self, id_pedido, precio_total):
        sql = """ UPDATE pedido SET precio_total = ? WHERE id = ? """
        self.update(sql, precio_total, id_pedido)

    def my_select(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)

        rows = cur.fetchall()

        for row in rows:
            print(row)