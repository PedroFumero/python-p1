pedidos = []
# Se lee el archivo
lector = open('misc/pedidos1.pz', encoding="utf-8")
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

lista_pedidos = {i: {} for i in range(1, len(pedidos) + 1)}

for i, pedido in enumerate(pedidos):
    for j, dato in enumerate(pedido):
        if j == 0:
            datos_pedido = dato.split(';')
            lista_pedidos[i+1]['nombre'] = datos_pedido[0]
            lista_pedidos[i+1]['fecha'] = datos_pedido[1]
            lista_pedidos[i+1]['pedido'] = []
        if j > 0:
            individual = dato.split(';')
            lista_pedidos[i+1]['pedido'].append(individual)

print(lista_pedidos)   