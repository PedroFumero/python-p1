from cargador_archivo import Manejador
from pizza import PizzaPersonal, PizzaMediana, PizzaFamiliar

pedidos = Manejador().cargarArchivo()
# print(pedidos)

for pedido in pedidos.values():
    # print(pedido)
    for orden in pedido['pedido']:
        # print(orden)
        if orden[0].lower() == 'personal':
            pizza = PizzaPersonal(orden[1:])
            print(f'Pizza personal, ingredientes {pizza.ingredientes}, precio = {pizza.precio}')
        elif orden[0].lower() == 'mediana':
            pizza = PizzaMediana(orden[1:])
            print(f'Pizza mediana, ingredientes {pizza.ingredientes}, precio = {pizza.precio}')
        elif orden[0].lower() == 'familiar':
            pizza = PizzaFamiliar(orden[1:])
            print(f'Pizza familiar, ingredientes {pizza.ingredientes}, precio = {pizza.precio}')
        