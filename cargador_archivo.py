import os

class Manejador:
    """
    Incluye toda la lógica para la carga del archivo .pz
    """
    def __init__(self):
        self.lista_pedidos = None
    

    def cargarArchivo(self, ruta_archivo):
        """
        Encargado de realizar el procesamiento de carga. Retorna un diccionario con los pedidos.
        """
        # TODO faltan las validaciones, actualmente no cuenta con ninguna
        pedidos = []
        # Se lee el archivo
        lector = open(ruta_archivo, encoding="utf-8")
        lectura = lector.readlines()
        # Se elimina \n (salto de linea de cada índice de la lista)
        lectura = [i.rstrip('\n') for i in lectura]

        for i in lectura:
            if(i.lower() == 'comienzo_pedido'):
                pedido = []
                continue
            elif(i.lower()) == 'fin_pedido':
                pedidos.append(pedido)
            else:
                pedido.append(i)

        self.lista_pedidos = {i: {} for i in range(1, len(pedidos) + 1)}

        for i, pedido in enumerate(pedidos):
            for j, dato in enumerate(pedido):
                if j == 0:
                    datos_pedido = dato.split(';')
                    self.lista_pedidos[i+1]['nombre'] = datos_pedido[0]
                    self.lista_pedidos[i+1]['fecha'] = datos_pedido[1]
                    self.lista_pedidos[i+1]['pedido'] = []
                if j > 0:
                    individual = dato.split(';')
                    self.lista_pedidos[i+1]['pedido'].append(individual)
        return self.lista_pedidos

    @staticmethod
    def getRutaArchivo():
        """
        Pregunta y valida la ruta del archivo con el que se trabajaran los pedidos
        Retrorna el nombre de un archivo valido
        """
        while True:
            print("Por favor, introduzca el el nombre del archivo. Ej: misc/pedidos1.pz")
            ruta_archivo = input()
            if os.path.exists(ruta_archivo):
                return ruta_archivo
            else:
                print(ruta_archivo, "no fue localizado")
    
    @staticmethod
    def menu(opt):
        while(opt not in ['1', '2']):
            print(f'1 - Introduzca el nombre de un archivo para cargar.')
            print(f'2 - Cargar todos los archivos .pz en el directorio /misc/')
            opt = input('Opción: ')
        return opt
            
    @staticmethod
    def leerTodos():
        directorio = f'{os.getcwd()}/misc/'
        contenido = os.listdir(directorio)
        pedidos = []
        for archivo in contenido:
            if os.path.isfile(os.path.join(directorio, archivo)) and archivo.endswith('.pz'):
                pedidos.append(archivo)
        return pedidos
    
    @staticmethod
    def validarVacio(lista_pedidos):
        for pedido in lista_pedidos.values():
            for llave, valor in pedido.items():
                if not valor:
                    print(f'Existe un error en el archivo. :: {llave} :: esta vacío. Realice las correcciones y vuelva a ejecutar el programa.')
                    return True
        return False