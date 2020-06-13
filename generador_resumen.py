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