class Resumen:
    """
        Clase encargada de manejar la generacion del resumen
    """
    def __init__(self,factura):
        self.factura = factura

    def mostrarResumen(self):
        print(self.factura)