from database_model import PizzeriaDatabase
from sqlite3 import Error

class DatabaseController:
    """ Controlador que interactua con el Modelo principal de la BD """
    
    def __init__(self, database_name):
        """ 
        Inicializacion de la base de datos 
        Se crean las tablas si no existen y se insertan los precios de las pizzas
        e ingredientes con las que trabaja el sistema
        """
        self.db = PizzeriaDatabase(database_name)
        db = self.db
        db.create_project_tables_if_not_exists()

        with db.conn:
            try:
                # Datos del negocio
                tamanios = ['personal', 'mediana', 'familiar']
                precios_pizzas = [10,15,20]
                precios_ingredientes = {
                    'jamón': [1.5, 1.75, 2],
                    'champiñones': [1.75, 2.05, 2.5],
                    'pimentón': [1.5, 1.75, 2],
                    'doble queso': [0.8, 1.3, 1.7],
                    'aceitunas': [1.8, 2.15, 2.6],
                    'pepperoni': [1.25, 1.7, 1.9],
                    'salchichón': [1.6, 1.85, 2.1]
                }
                
                # Insertar pizzas
                pizzas = db.select_pizzas()
                if(len(pizzas) == 0):
                    for i in range(len(tamanios)):
                        db.insert_pizza(tamanios[i], precios_pizzas[i])

                # Insertar ingredientes
                ingredientes = db.select_ingredientes()
                if(len(ingredientes) == 0):
                    for ingrediente, precios in precios_ingredientes.items():
                        for i in range(len(tamanios)):
                            db.insert_ingrediente(ingrediente, tamanios[i], precios[i])          

            except Error as e:
                db.conn.rollback()
                print("SQLite Excepiton Error:", e)
                print("Error al inicializar la base datos")
            else:                    
                db.conn.commit()

    def cargar_registros(self, registros):
        """ 
        Cargar todos los registros proporcionados a la base de datos 
        El formato de los registros se obtiene desde otras clases como el Manejador
        """
        db = self.db

        with db.conn:
            try: 
                for registro in registros.values():

                    # Insetar usuario y pedido sin precio total
                    id_usuario = db.insert_usuario(nombre=registro['nombre'])
                    id_pedido = db.insert_pedido(fk_usuario=id_usuario, fecha=registro['fecha'])
                    precio_total = 0

                    for pedido in registro['pedido']:
                        tamanio = pedido[0]
                        pizza = db.select_pizzas_where(tamanio=tamanio)[0]
                        id_pizza = pizza[0]
                        precio_total += pizza[2]

                        # Insertar un pizza sin ingredinetes adicionales
                        if len(pedido) == 1:
                            db.insert_detalle(
                                fk_pedido=id_pedido, 
                                fk_pizza=id_pizza, 
                                fk_ingrediente=None
                            )
                            
                        # Insertar una pizza con ingredinetes adicionales
                        elif len(pedido) > 1:
                            for i in range(1, len(pedido)):
                                ingrediente = db.select_ingredientes_where(
                                    tamanio=tamanio, 
                                    nombre=pedido[i]
                                )[0]
                                id_ingrediente = ingrediente[0]
                                precio_total += ingrediente[3]

                                db.insert_detalle(
                                    fk_pedido=id_pedido, 
                                    fk_pizza=id_pizza, 
                                    fk_ingrediente=id_ingrediente
                                )
                    
                    # Actualizar el precio total del pedido
                    db.update_precio_pedido(id_pedido, precio_total)
            
            except Error as e:
                db.conn.rollback()
                print("SQLite Excepiton Error:", e)
                print("Error al cargar registros en la base de datos")
            else:                    
                db.conn.commit()

    def print_datase(self):
        """ Imprimir en pantalla la base de datos (para debbugin) """
        db = self.db
        with db.conn:
            print("(u.id, u.nombre, pe.id, pe.fecha, pe.precio_total, pi.id, pi.tamanio, i.id, i.nombre)")
            rows = db.select_all_database()
            for row in rows:
                for value in row:
                    if value:
                        print('|{0:<18}|'.format(value), end="")
                    else:
                        print('|', ' '*16, '|', end="")
                print()

            print(db.test())