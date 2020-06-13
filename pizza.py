class PizzaBase:
    """
    Pizza base, con métodos comúnes
    """
        
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
        self.precios_lista = {
            'jamón': 1.5,
            'champiñones': 1.75,
            'pimentón': 1.5,
            'doble queso': 0.8,
            'aceitunas': 1.8,
            'pepperoni': 1.25,
            'salchichon': 1.6
        }
        # print(self.ingredientes)
        self.precio = self.calcularPrecio(10, self.precios_lista, self.ingredientes)
        # print(self.precio)
        
class PizzaMediana(PizzaBase):
    """
    Pizza tamaño mediana de valor 15um (Base)
    """
    
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes
        self.precios_lista = {
            'jamón': 1.75,
            'champiñones': 2.05,
            'pimentón': 1.75,
            'doble queso': 1.3,
            'aceitunas': 2.15,
            'pepperoni': 1.7,
            'salchichon': 1.85
        }
        # print(self.ingredientes)
        self.precio = self.calcularPrecio(15, self.precios_lista, self.ingredientes)
        # print(self.precio)

class PizzaFamiliar(PizzaBase):
    """
    Pizza tamaño familiar de valor 20um (Base)
    """
    
    def __init__(self, ingredientes):
        self.ingredientes = ingredientes
        self.precios_lista = {
            'jamon': 2,
            'champiñones': 2.5,
            'pimentón': 2,
            'doble queso': 1.7,
            'aceitunas': 2.6,
            'pepperoni': 1.9,
            'salchichon': 2.1
        }
        # print(self.ingredientes)
        self.precio = self.calcularPrecio(20, self.precios_lista, self.ingredientes)
        # print(self.precio)
        
    # * Así se pude utilizar un método de la súper clase en python
    # super().detalle(self.precio)

    # TODO algunos ingredientes no son tomados correctamente, debido a que en el archivo algunos tienen acento y otros no: jamón -> jamon, salchichón -> salchichon, otros tienen errores, por ejemplo pepperoni -> peppperoni
