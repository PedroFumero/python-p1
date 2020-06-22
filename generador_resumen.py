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
    
    def armarResumen(self):
        lista_pedidos = self.ordenarPedidos()
    
        for fecha, pedidos in lista_pedidos.items():
            precios_pizzas = {'personal': 0,'mediana': 0,'familiar': 0}
            cant_pizzas = {'personal': 0,'mediana': 0,'familiar': 0}
            print(fecha)
            for pedido in pedidos:
                # print(pedido)
                cant_pizzas[pedido['tamanio']] += 1
                precios_pizzas[pedido['tamanio']] += pedido['precio']
            print(f'Total: {sum(precios_pizzas.values())}')
            print(f'Cantidades: {cant_pizzas}')
            print(f'Precios: {precios_pizzas}')
            print()
            
