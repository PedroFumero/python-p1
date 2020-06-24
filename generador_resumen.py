import sys
import pizza
class ResumenDelDia:
    '''Clase que modela el resumen de un dia especifico
        Atributos 
            fecha: fecha del resumen
            total: total en UMs de ese dia
            ventasXpizza: diccionario de tamanos de pizza cuyo valor es un 
                diccionario compuesto por la cantidad vendida y la ganancia
            ventasXingrediente: diccionario de igredientes cuyo valor es un 
                diccionario compuesto por la cantidad vendida y la ganancia
    '''
    def __init__(self,fecha,total,ventasXpizza,ventasXingrediente):
        self.fecha = fecha
        self.total = total
        self.ventasXpizza = ventasXpizza
        self.ventasXingrediente = ventasXingrediente 
    
    def mostrarResumen(self):
        """
            Muestra por consola el resumen de ventas para el dia 
            correspondiente.
            Usa los atributos de la propia clase.
            Para imprimir cada fila se ingresan los datos en una variable "row"
            la cual es una tupla y son mapeados para su impresion en el print
        """
        print('Fecha: ' + self.fecha + '\nTotal: ' + str(self.total) + ' UMs')
        print ('\nVentas por pizza (sin incluir adicionales):\n')
        print ('{0:<15} {1:>15} {2:>15}'.format(*('Tamaño','Unidades','MontoUMs')))
        for key, value in self.ventasXpizza.items():
            row = (key.title(),value['cantidad'],value['ganancia'])
            print ('{0:<15} {1:>15} {2:>15}'.format(*row))
        print ('\nVentas por Ingrediente:\n')
        print ('{0:<15} {1:>15} {2:>15}'.format(*('Ingredientes','Unidades','MontoUMs')))
        for key,value in self.ventasXingrediente.items():
            row = (key.title(),value['cantidad'],value['ganancia'])
            print ('{0:<15} {1:>15} {2:>15}'.format(*row ))
        print('\n\n')

class GeneradorResumen():
    """
        Clase encargada de la generacion del resumen
        Atributos 
            pedidos: diccionario que contiene los pedidos
    """
    def __init__(self,pedidos):
        """
            Constructor de la clase ResumenDelDia
        """
        self.pedidos = pedidos

    def guardarResumen(self,listaResumen):
        """
            Al pasarle una lista previamente generada de resumenes diarios
            guarda en un archivo todo el resumen
        """
        orig_stdout = sys.stdout
        f = open('misc/resumen.txt', 'w')

        sys.stdout = f
        for resumen in listaResumen:
            resumen.mostrarResumen()
        sys.stdout = orig_stdout
        f.close()

    def mostrarPedidos(self):
        """
            Funcion que permite postrar los pedidos que fueron cargados
            en la clase
        """
        pedidos = self.pedidos  
        if pedidos is None:
            print('No hay pedidos por mostrar!') 
        else:
            for pedido in pedidos:
                print (pedido)
                for campo in pedidos[pedido]:
                    print (campo,':',pedidos[pedido][campo])  
                    
    def obtenerPrecios(self, tamanio, componente):
        return pizza.PizzaBase().obtenerPrecios(tamanio,componente)             

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

    def generarListaResumen(self,save):
        """
            Funcion que genera el resumen total partiendo de la lista de pedidos agrupada
            Se retorna una lista resumen con Objetos de la clase ResumenDelDia.   
            Atributos
                save: bool que controla si se desea o no guardar en archivo     
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
        if save :
            self.guardarResumen(listaResumen)
        return listaResumen