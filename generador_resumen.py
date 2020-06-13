class ResumenDelDia:
    """
        Clase que modela el resumen
    """
    def __init__(self,fecha,total,ventasXpizza,ventasXingrediente):
        self.fecha = fecha
        self.total = total
        self.ventasXpizza = ventasXpizza
        self.ventasXingrediente = ventasXingrediente 
    
    def mostrarResumen(self):
        print('Fecha: ' + self.fecha + '\nTotal: ' + str(self.total))
        print ('\nVentas por pizza (sin incluir adicionales):\n')
        for item in self.ventasXpizza.items():
            print ('{0:<15} {1:>8}'.format(*item))
        print ('\nVentas por Ingrediente:\n')
        for item in self.ventasXingrediente.items():
            print ('{0:<15} {1:>8}'.format(*item))

class GeneradorResumen():
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

    def generarListaResumen(self):
        """
            Funcion que genera el resumen total partiendo de la lista de pedidos agrupada
        """
        pedidos = self.agruparFecha()
        listaResumen =[]
        for fecha in pedidos.keys():
            totalRes = 0
            ventasXpizza = {}
            ventasXingrediente = {}
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
                        ventasXingrediente[ingrediente] += 1
                    else:
                        ventasXingrediente[ingrediente] = 1
            listaResumen.append(ResumenDelDia(fechaRes,totalRes,ventasXpizza,ventasXingrediente))

        return listaResumen

    def agruparFecha(self):
        """
            Funcion que agrupa por fecha los pedidos
        """
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
