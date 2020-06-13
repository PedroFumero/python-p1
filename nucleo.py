from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes

ruta_archivo = Manejador().getRutaArchivo()
pedidos = Manejador().cargarArchivo(ruta_archivo)
# print(pedidos)


total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
print(total_ordenes)