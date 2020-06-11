class PizzaBase:
    def detalle(self, precio):
        # print('Tipo de pizza: ')
        if(isinstance(self, PizzaPersonal)):
            print(f'Pizza personal, el precio es: {precio}')
        elif(isinstance(self, PizzaMediana)):
            print(f'Pizza mediana, el precio es: {precio}')
        elif(isinstance(self, PizzaFamiliar)):
            print(f'Pizza familiar, el precio es: {precio}')
            
    
        

class PizzaPersonal(PizzaBase):
    
    def __init__(self, hola):
        self.precio = 10
        self.ingredientes = []
        print(hola)
        
    def detalle(self):
        super().detalle(self.precio)
        
class PizzaMediana(PizzaBase):
    
    def __init__(self):
        self.precio = 15
        self.ingredientes = []
        
    def detalle(self):
        super().detalle(self.precio)

class PizzaFamiliar(PizzaBase):
    
    def __init__(self):
        self.precio = 20
        self.ingredientes = []
    
    def detalle(self):
        super().detalle(self.precio)

# pizza1 = PizzaPersonal()
# pizza1.detalle()

# pizza2 = PizzaMediana()
# pizza2.detalle()

# pizza3 = PizzaFamiliar()
# pizza3.detalle()