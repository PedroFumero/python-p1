from pizza import PizzaPersonal, PizzaMediana, PizzaFamiliar

class ProcesadorOrdenes:
    
    def __init__(self):
        self.factura_final = None
        
    def contarOrdenes(self, pedidos):
        """
        Cuenta la cantidad de órdenes indicadas en el archivo .pz, incluyendo si pertenecen a un mismo cliente.
        """
        num_orden = 0
        for pedido in pedidos.values():
            for orden in pedido['pedido']:
                num_orden += 1      
        return num_orden
    
    def procesarPedidos(self, pedidos):
        """
        Instancia las pizzas según su tipo y retorna un diccionario con todos los pedidos ordenados, incluyendo el precio.
        """
        num_orden = 0
        cantidad_ordenes = self.contarOrdenes(pedidos)
        
        self.factura_final = {i: {} for i in range(1, cantidad_ordenes + 1)}
        
        for pedido in pedidos.values():
            # print(pedido)
            for orden in pedido['pedido']:
                num_orden += 1
                if orden[0].lower() == 'personal':
                    pizza = PizzaPersonal(orden[1:])
                    # print(f'Pizza personal, ingredientes {pizza.ingredientes}, precio = {pizza.precio}')
                    # self.factura_final[orden+1]['nombre'] = datos_pedido[0]
                elif orden[0].lower() == 'mediana':
                    pizza = PizzaMediana(orden[1:])
                    # print(f'Pizza mediana, ingredientes {pizza.ingredientes}, precio = {pizza.precio}')
                elif orden[0].lower() == 'familiar':
                    pizza = PizzaFamiliar(orden[1:])
                    # print(f'Pizza familiar, ingredientes {pizza.ingredientes}, precio = {pizza.precio}')
                self.factura_final[num_orden]['nombre'] = pedido['nombre']
                self.factura_final[num_orden]['fecha'] = pedido['fecha']
                self.factura_final[num_orden]['tamanio'] = orden[0]
                self.factura_final[num_orden]['ingredientes'] = pizza.ingredientes
                self.factura_final[num_orden]['precio'] = pizza.precio
        return self.factura_final
