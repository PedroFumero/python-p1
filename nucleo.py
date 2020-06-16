from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import Resumen

# Menú de opciones
opt = Manejador().menu(0)
if opt == '1':
    # Cargar pedidos desde un archivo
    ruta_archivo = Manejador().getRutaArchivo()
    pedidos = Manejador().cargarArchivo(ruta_archivo)
elif opt == '2':
    # Cargar todos los pedidos en la carpeta /misc
    pedidos = ProcesadorOrdenes().procesarTodos()
    # print(pedidos)



# ruta_archivo = Manejador().getRutaArchivo()
# pedidos = Manejador().cargarArchivo(ruta_archivo)
# print(pedidos)


total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
Resumen(total_ordenes).mostrarPedidos()