import json
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
        print('Fecha: ' + self.fecha + '\nTotal: ' + str(self.total) + ' UMs')
        print ('\nVentas por pizza (sin incluir adicionales):\n')
        print ('{0:<15} {1:>15} {2:>15}'.format(*('Tamaño','Unidades','MontoUMs')))
        for key, value in self.ventasXpizza.items():
            row = (key,value['cantidad'],value['ganancia'])
            print ('{0:<15} {1:>15} {2:>15}'.format(*row))
        print ('\nVentas por Ingrediente:\n')
        print ('{0:<15} {1:>15} {2:>15}'.format(*('Ingredientes','Unidades','MontoUMs')))
        for key,value in self.ventasXingrediente.items():
            row = (key,value['cantidad'],value['ganancia'])
            print ('{0:<15} {1:>15} {2:>15}'.format(*row ))
        print('\n\n')

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
                    
    def obtenerPrecios(self, tamanio, componente):
            with open('misc/precios.json', encoding='utf-8') as json_file:
                precios = json.load(json_file)
                return precios[tamanio][componente]            


    def generarListaResumen(self):
        """
            Funcion que genera el resumen total partiendo de la lista de pedidos agrupada
        """
        pedidos = self.agruparFecha()
        listaResumen =[]
        for fecha in pedidos.keys():
            totalRes = 0
            fechaRes = fecha
            ventasXpizza = {}
            ventasXingrediente = {}
            for pedido in pedidos[fecha].keys():
                totalRes += pedidos[fecha][int(pedido)]['precio']
                tamanio = pedidos[fecha][int(pedido)]['tamanio']
                if tamanio in ventasXpizza.keys():
                    ventasXpizza[tamanio]['cantidad'] += 1
                    ventasXpizza[tamanio]['ganancia'] += self.obtenerPrecios(tamanio, 'base')
                else:
                    ventasXpizza[tamanio] = {}
                    ventasXpizza[tamanio]['cantidad'] = 1
                    ventasXpizza[tamanio]['ganancia'] = self.obtenerPrecios(tamanio, 'base')
                for ingrediente in pedidos[fecha][int(pedido)]['ingredientes']:
                    if ingrediente in ventasXingrediente.keys():
                        ventasXingrediente[ingrediente]['cantidad'] += 1
                        ventasXingrediente[ingrediente]['ganancia'] += self.obtenerPrecios(tamanio, ingrediente)
                    else:
                        ventasXingrediente[ingrediente] = {}
                        ventasXingrediente[ingrediente]['cantidad'] = 1
                        ventasXingrediente[ingrediente]['ganancia'] = self.obtenerPrecios(tamanio, ingrediente)
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
