from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import Resumen
from database_controller import DatabaseController

ruta_archivo = Manejador().getRutaArchivo()
pedidos = Manejador().cargarArchivo(ruta_archivo)

db = DatabaseController('pizzeria_database.db')
db.cargar_registros(pedidos)
db.print_datase()


total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
Resumen(total_ordenes).mostrarPedidos()