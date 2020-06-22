from database_model import PizzeriaDatabase

class DatabaseController:
    def __init__(self, database_name):
        self.db = PizzeriaDatabase(database_name)

        db = self.db
        db.create_project_tables_if_not_exists()
        with db.conn:
            # Insertar ingredientes pizzas
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
            
            pizzas = db.select_pizzas()
            if(len(pizzas) == 0):
                for i in range(len(tamanios)):
                    db.insert_pizza(tamanios[i], precios_pizzas[i])

            ingredientes = db.select_ingredientes()
            if(len(ingredientes) == 0):
                for ingrediente, precios in precios_ingredientes.items():
                    for i in range(len(tamanios)):
                        db.insert_ingrediente(ingrediente, tamanios[i], precios[i])          

            db.conn.commit()

    def cargar_registros(self, registros):
        db = self.db
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

        with db.conn:

            db.select("DELETE FROM detalle")

            for registro in registros.values():
                id_usuario = db.insert_usuario(nombre=registro['nombre'])
                id_pedido = db.insert_pedido(fk_usuario=id_usuario, fecha=registro['fecha'])
                for pedido in registro['pedido']:
                    id_pizza = tamanios.index(pedido[0]) + 1
                    if len(pedido) == 1:
                        db.insert_detalle(
                            fk_pedido=id_pedido, 
                            fk_pizza=id_pizza, 
                            fk_ingrediente=None
                        )
                    elif len(pedido) > 1:
                        for i in range(1, len(pedido)):
                            ingrediente = list(precios_ingredientes.keys()).index(pedido[i])
                            id_ingrediente = ingrediente * len(tamanios) + id_pizza
                            db.insert_detalle(
                                fk_pedido=id_pedido, 
                                fk_pizza=id_pizza, 
                                fk_ingrediente=id_ingrediente
                            )
            
            db.conn.commit()
    
    def print_datase(self):
        db = self.db
        with db.conn:
            sql = """
            SELECT u.id, u.nombre, pe.id, pe.fecha, pi.id, pi.tamanio, i.id, i.nombre 
            FROM detalle AS d
                LEFT OUTER JOIN ingrediente AS i ON d.fk_ingrediente = i.id
                JOIN pizza AS pi ON d.fk_pizza = pi.id
                JOIN pedido AS pe ON d.fk_pedido = pe.id
                JOIN usuario AS u ON pe.fk_usuario = u.id
            """
            print("(u.id, u.nombre, pe.id, pe.fecha, pi.id, pi.tamanio, i.id, i.nombre)")
            rows = db.select(sql)
            for r in rows:
                print(r)