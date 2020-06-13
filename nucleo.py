from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import Resumen

ruta_archivo = Manejador().getRutaArchivo()
pedidos = Manejador().cargarArchivo(ruta_archivo)
# print(pedidos)


total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
Resumen(total_ordenes).mostrarPedidos()