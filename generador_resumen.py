class Resumen:
    """
        Clase que modela el resumen
    """
    def __init__(self,fecha,total,ventasXpizza,ventasXingrediente):
       self.fecha = fecha,
       self.total = total,
       ventasXpizza = ventasXpizza,
       ventasXingrediente = ventasXingrediente

    # def generarResumen(self):
    #     pedidos = self.pedidos   
    #     resumen = Re
    #     for pedido in pedidos.values():
    #         for nombre,fecha,tamanio,ingredientes,precio in pedido.items(): 

class generadorResumen():
    """
        Clase que genera el resumen
    """
    def __init__(self,pedidos):
        self.pedidos = pedidos

    def mostrarPedidos(self):
        pedidos = self.pedidos  
        if pedidos is None:
            print('No hay pedidos por mostrar!') 
        else:
            for pedido in pedidos:
                print (pedido)
                for campo in pedidos[pedido]:
                    print (campo,':',pedidos[pedido][campo])            