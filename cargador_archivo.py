import os
import re

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
        pedidos = []
        # Se lee el archivo
        lector = open(ruta_archivo, encoding="utf-8")
        lectura = lector.readlines()
        # Se elimina \n (salto de linea de cada índice de la lista)
        lectura = [i.rstrip('\n') for i in lectura]
        lector.close()
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
        Pregunta y valida la ruta del archivo con el que se trabajarán los pedidos
        Retorna el nombre de un archivo válido
        """
        while True:
            print("Por favor, introduzca el nombre del archivo. Ej: misc/pedidos1.pz")
            ruta_archivo = input()
            if not ruta_archivo.endswith('.pz'):
                print('El archivo debe tener extensión .pz')
            else:
                if os.path.exists(ruta_archivo):
                    return ruta_archivo
                else:
                    print(ruta_archivo, "no fue localizado")
    
    @staticmethod
    def menu(opt, existe_db = False):
        """
        Menu de opciones del programa
        """
        while(opt not in ['1', '2', '3'] or (opt == '3' and not existe_db)):
            print(f'1 - Introduzca el nombre de un archivo para cargar.')
            print(f'2 - Cargar todos los archivos .pz en el directorio /misc/')
            if existe_db:
                print(f'3 - Cargar datos desde la base de datos (pizzeria_database.db)')
            opt = input('Opción: ')
        return opt
            
    @staticmethod
    def leerTodos():
        """
        Lee todos los archivos .pz dentro del directorio /misc/
        """
        directorio = f'{os.getcwd()}/misc/'
        contenido = os.listdir(directorio)
        pedidos = []
        for archivo in contenido:
            if os.path.isfile(os.path.join(directorio, archivo)) and archivo.endswith('.pz'):
                pedidos.append(archivo)
        return pedidos
    
    def chequearVacio(self, llave, valor):
        """
        Valida que cualquier campo en el archivo no sea vacío
        """
        if not valor: 
            print(f'Existe un error en el archivo. Un campo de {llave} esta vacío. Realice las correcciones y vuelva a ejecutar el programa.')
            return True
        return False
    
    def chequearNumeroEnNombre(self, llave, valor):
        """
        Valida que un nombre no contenga números
        """
        if llave == 'nombre':    
            tiene_numero = any(map(str.isdigit, valor))
            if tiene_numero:
                print(f'Existe un error en el archivo. Uno o más nombres contienen números. Realice las correcciones y vuelva a ejecutar el programa.')
                return True
            return False
    
    def chequearFormatoFecha(self, llave, valor):
        """
        Valida que el formado de fecha sea correcto: dia/mes/año
        """
        if llave == 'fecha':
            match = re.search('([0-9|/]+)', valor)
            if not match:
                print(f'Existe un error en el archivo. El formato de fecha debe ser dia/mes/anio. Realice las correcciones y vuelva a ejecutar el programa.')
                return True
            return False
    
    @staticmethod
    def validar(lista_pedidos):
        """
        Método que valida posibles errores en la lectura del archivo
        """
        for pedido in lista_pedidos.values():
            for llave, valor in pedido.items():
                if Manejador().chequearVacio(llave, valor):
                    return True
                elif Manejador().chequearNumeroEnNombre(llave, valor):
                    return True
        return False