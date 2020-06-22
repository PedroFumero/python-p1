class Resumen:
    """
        Clase encargada de manejar la generacion del resumen
    """
    def __init__(self,pedidos):
        self.pedidos = pedidos

    def mostrarPedidos(self):
        pedidos = self.pedidos   
        for pedido in pedidos:
            print (pedido)
            for campo in pedidos[pedido]:
                print (campo,':',pedidos[pedido][campo])
              
    def fechas(self):
        listado_fechas = []
        for pedido in self.pedidos.values():
            listado_fechas.append(pedido['fecha'])
        listado_fechas = sorted(list(set(listado_fechas)))
        return listado_fechas
            
    def ordenarPedidos(self):
        lista_resumen = { key: [] for key in self.fechas() }
        for pedido in self.pedidos.values():
            lista_resumen[pedido['fecha']].append(pedido)
        return lista_resumen
    
    def calcularPrecioIngrediente(self, pedido, cant_ingredientes, precios_ingredientes):
        precios_lista = None
        if pedido['tamanio'] == 'personal':
            precios_lista = {
            'jamón': 1.5,
            'champiñones': 1.75,
            'pimentón': 1.5,
            'doble queso': 0.8,
            'aceitunas': 1.8,
            'pepperoni': 1.25,
            'salchichón': 1.6
        }
        elif pedido['tamanio'] == 'mediana':
            precios_lista = {
                'jamón': 1.75,
                'champiñones': 2.05,
                'pimentón': 1.75,
                'doble queso': 1.3,
                'aceitunas': 2.15,
                'pepperoni': 1.7,
                'salchichón': 1.85
            }
        elif pedido['tamanio'] == 'familiar':
            precios_lista = {
            'jamón': 2,
            'champiñones': 2.5,
            'pimentón': 2,
            'doble queso': 1.7,
            'aceitunas': 2.6,
            'pepperoni': 1.9,
            'salchichón': 2.1
        }
            
        for ingrediente in pedido['ingredientes']:
            precios_ingredientes[ingrediente] += precios_lista[ingrediente]
            cant_ingredientes[ingrediente] += 1
        
    
    def armarResumen(self):
        lista_pedidos = self.ordenarPedidos()
    
        for fecha, pedidos in lista_pedidos.items():
            cant_pizzas = {'personal': 0,'mediana': 0,'familiar': 0}
            precios_pizzas = {'personal': 0,'mediana': 0,'familiar': 0}
            cant_ingredientes = {'jamón': 0,'champiñones': 0,'pimentón': 0,'doble queso': 0,'aceitunas': 0,'pepperoni': 0,'salchichón': 0}
            precios_ingredientes = {'jamón': 0,'champiñones': 0,'pimentón': 0,'doble queso': 0,'aceitunas': 0,'pepperoni': 0,'salchichón': 0}
            print(fecha)
            for pedido in pedidos:
                # print(pedido)
                cant_pizzas[pedido['tamanio']] += 1
                precios_pizzas[pedido['tamanio']] += pedido['precio']
                self.calcularPrecioIngrediente(pedido, cant_ingredientes, precios_ingredientes)
            print(f'Total: {sum(precios_pizzas.values())}')
            print(f'Cantidades: {cant_pizzas}')
            print(f'Precios: {precios_pizzas}')
            print('-'*20)
            print('Ingredientes:')
            print(f'Cantidades: {cant_ingredientes}')
            print(f'Precios: {precios_ingredientes}')
            print()
            
