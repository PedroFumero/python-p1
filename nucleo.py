from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import ResumenDelDia,GeneradorResumen

ruta_archivo = Manejador().getRutaArchivo()
pedidos = Manejador().cargarArchivo(ruta_archivo)
# print(pedidos)


total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
#generadorResumen(total_ordenes).mostrarPedidos()
resumenXfecha = GeneradorResumen(total_ordenes).generarListaResumen()

for dia in resumenXfecha:
    print('\n')
    dia.mostrarResumen()