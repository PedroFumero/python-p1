import json
class PizzaBase:
    """
    Pizza base, con métodos comúnes
    """
    def obtenerPrecios(self, tamanio, componente):
        """
            Funcion que obtiene de un archivo .json ubicado en 'misc/'
            La estructura del json es convertida a un diccionario a traves
            de la libreria json importada al inicio
        """
        if componente is None:
            with open('misc/precios.json', encoding='utf-8') as json_file:
                precios = json.load(json_file)
                return precios[tamanio] 
        else:
            with open('misc/precios.json', encoding='utf-8') as json_file:
                precios = json.load(json_file)
                return precios[tamanio][componente]        

    def calcularPrecio(self, precio, precios, ingredientes):
        """
        Retorna el precio final de cada pizza incluyendo la suma de sus ingredientes.
        """
        
        # print(precios, ingredientes)
        for ingrediente in ingredientes:
            if ingrediente in precios.keys():
                precio += precios[ingrediente]
        # print(f'Pizza personal, con ingredientes adicionales: {ingredientes} = {precio}')
        return precio

class PizzaPersonal(PizzaBase):
    """
    Pizza tamaño personal de valor 10um (Base)
    """
    
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes
        self.precios_lista = self.obtenerPrecios('personal',None)
        self.base = self.obtenerPrecios('personal','base')
        # print(self.ingredientes)
        self.precio = self.calcularPrecio(self.base, self.precios_lista, self.ingredientes)
        # print(self.precio)
        
class PizzaMediana(PizzaBase):
    """
    Pizza tamaño mediana de valor 15um (Base)
    """
    
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes
        self.precios_lista = self.obtenerPrecios('mediana',None)
        self.base = self.obtenerPrecios('mediana','base')
        # print(self.ingredientes)
        self.precio = self.calcularPrecio(self.base, self.precios_lista, self.ingredientes)
        # print(self.precio)

class PizzaFamiliar(PizzaBase):
    """
    Pizza tamaño familiar de valor 20um (Base)
    """
    
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes
        self.precios_lista = self.obtenerPrecios('familiar',None)
        self.base = self.obtenerPrecios('familiar','base')
        # print(self.ingredientes)
        self.precio = self.calcularPrecio(self.base, self.precios_lista, self.ingredientes)
        # print(self.precio)
        
    # * Así se pude utilizar un método de la súper clase en python
    # super().detalle(self.precio)

    # TODO algunos ingredientes no son tomados correctamente, debido a que en el archivo algunos tienen acento y otros no: jamón -> jamon, salchichón -> salchichon, otros tienen errores, por ejemplo pepperoni -> peppperoni
