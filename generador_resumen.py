class Resumen:
    """
        Clase que modela el resumen
    """
    def __init__(self,fecha,total,ventasXpizza,ventasXingrediente):
       self.fecha = fecha,
       self.total = total,
       ventasXpizza = ventasXpizza,
       ventasXingrediente = ventasXingrediente 

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

    def generarResumen(self):
        pedidos = self.agruparFecha()
        fechaRes = None
        totalRes = 0
        ventasXpizza = {}
        ventasXingrediente = {}
        for fecha in pedidos.keys():
            fechaRes = fecha
            for pedido in pedidos[fecha].keys():
                totalRes += pedidos[fecha][int(pedido)]['precio']
                tamanio = pedidos[fecha][int(pedido)]['tamanio']
                if tamanio in ventasXpizza.keys():
                    ventasXpizza[tamanio] += 1
                else:
                    ventasXpizza[tamanio] = 1
                for ingrediente in pedidos[fecha][int(pedido)]['ingredientes']:
                    if ingrediente in ventasXingrediente.keys():
                        ventasXingrediente[tamanio] += 1
                    else:
                        ventasXingrediente[tamanio] = 1

        return Resumen(fechaRes,totalRes,ventasXpizza,ventasXingrediente)

    def agruparFecha(self):
        pedidos = self.pedidos
        resumenAgrupado = {}
        for pedido in pedidos.values():
            fecha = pedido['fecha']
            if fecha in resumenAgrupado.keys():
                pos = len(resumenAgrupado[fecha].values())+1 
                resumenAgrupado[fecha][pos] = pedido               
            else:
                resumenAgrupado[fecha] = {}
                resumenAgrupado[fecha][1] = pedido
        return resumenAgrupado
