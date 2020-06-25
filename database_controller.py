from database_model import PizzeriaDatabase
from sqlite3 import Error
import json

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
                pizzas = db.select_pizzas()
                ingredientes = db.select_ingredientes()
                if len(pizzas) == 0 or len(ingredientes) == 0:
                    # Datos del negocio
                    with open('misc/precios.json', encoding='utf-8') as json_file:
                        precios = json.load(json_file)
                    for tamanio, precio in precios.items():
                        for nombre, valor in precio.items():
                            # Insertar pizzas
                            if nombre == 'base':
                                db.insert_pizza(tamanio, valor)
                            # Insertar ingredientes
                            else:
                                db.insert_ingrediente(nombre, tamanio, valor)
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

                    numero_pedido = 0 # Util si una persona hace varios pedidos
                    for pedido in registro['pedido']:
                        tamanio = pedido[0]
                        pizza = db.select_pizzas_where(tamanio=tamanio)[0]
                        id_pizza = pizza[0]
                        precio_total += pizza[2]

                        # Insertar un pizza sin ingredinetes adicionales
                        if len(pedido) == 1:
                            db.insert_detalle(
                                numero_pedido=numero_pedido,
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
                                    numero_pedido=numero_pedido,
                                    fk_pedido=id_pedido, 
                                    fk_pizza=id_pizza, 
                                    fk_ingrediente=id_ingrediente
                                )
                        numero_pedido += 1
                    
                    # Actualizar el precio total del pedido
                    db.update_precio_pedido(id_pedido, precio_total)
            
            except Error as e:
                db.conn.rollback()
                print("SQLite Excepiton Error:", e)
                print("Error al cargar registros en la base de datos")
            else:                    
                db.conn.commit()

    def obtenerPedidos(self):
        """ 
            Obtiene los pedidos desde la BD
            Hace un JOIN de las tablas de la base de datos y retorna los valores importantes
                return: list rows
        """
        db = self.db
        rows = None
        with db.conn:
            try:
                rows = db.select_all_data()
            except Error as e:
                db.conn.rollback()
                print("SQLite Excepiton Error:", e)
                print("Error al extraer los registros de la base de datos")
        return rows

    @staticmethod
    def procesarRegistros(rows):
        """
            Transforma los registros provenientes de BD o .csv al formato del resto del programa
                return: dict dict_pedidos
        """
        if rows is not None and len(rows) > 0:
            pedidos = list()
            for row in rows:
                nombre = row[0]
                fecha = row[1]
                # precio_total = row[2]
                numero_pedido = int(row[3]) # Util cuando un usuario tiene varios pedidos
                tamanio = row[4]
                ingrediente = row[5] if row[5] != '' else None
                
                # Primer registro
                if len(pedidos) == 0:
                    detalle = [tamanio, ingrediente] if ingrediente else [tamanio]
                    pedido = {
                        'nombre': nombre,
                        'fecha': fecha,
                        'pedido': [detalle]
                    }
                    pedidos.append(pedido)

                # Si son datos pertenecientes a la persona anterior
                elif pedidos[-1]['nombre'] == nombre and pedidos[-1]['fecha'] == fecha:
                    # Si son datatos del mismo pedido
                    if numero_pedido == len(pedidos[-1]['pedido']) - 1:
                        pedidos[-1]['pedido'][numero_pedido].append(ingrediente)
                    # Si es un nuevo pedido de la misma persona
                    else:
                        detalle = [tamanio, ingrediente] if ingrediente else [tamanio]
                        pedidos[-1]['pedido'].append(detalle)

                # Si son datos de una persona distinta a la anterior
                else:
                    detalle = [tamanio, ingrediente] if ingrediente else [tamanio]
                    pedido = {
                        'nombre': nombre,
                        'fecha': fecha,
                        'pedido': [detalle]
                    }
                    pedidos.append(pedido)
                
            # Retorna los pedidos en el formato requerido
            dict_pedidos = {i:pedidos[i-1] for i in range(1, len(pedidos) + 1)}
            return dict_pedidos

    def tiene_datos(self):
        """ Verficiar si hay datos en la base de datos """
        db = self.db
        with db.conn:
            try:
                row = db.select_1_detalle()
                return len(row) >= 1
            except Error as e:
                return False

    def print_datase(self):
        """ Imprimir en pantalla la base de datos (para debbugin) """
        db = self.db
        with db.conn:
            columnas = '|{0:15}||{1:20}||{2:15}||{3:15}||{4:15}||{5:15}||{6:15}||{7:15}||{8:15}||{9:15}|'
            print(columnas.format('u.id', 'u.nombre', 'pe.id', 'pe.fecha', 'pe.precio_total', 'd.numero_pedido', 'pi.id', 'pi.tamanio', 'i.id', 'i.nombre'))
            rows = db.select_all_database()
            i = 0
            for row in rows:
                for i in range(len(row)):
                    if row[i] is not None and i == 1:
                        print('|{0:<20}|'.format(row[i]), end="")
                    elif row[i] is not None:
                        print('|{0:<15}|'.format(row[i]), end="")
                    elif i == 1:
                        print('|', ' '*18, '|', end="")
                    else:
                        print('|', ' '*13, '|', end="")
                print()
