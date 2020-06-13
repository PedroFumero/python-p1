class Resumen:
    """
        Clase encargada de manejar la generacion del resumen
    """
    def __init__(self,pedidos):
        self.pedidos = pedidos

    def mostrarPedidos(self):
        for pedido in self.pedidos.keys():
            print(self.pedidos[pedido])