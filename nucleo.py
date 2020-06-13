from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes

pedidos = Manejador().cargarArchivo()
# print(pedidos)


total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
print(total_ordenes)