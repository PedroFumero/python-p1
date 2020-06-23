import sys

from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import ResumenDelDia,GeneradorResumen
from database_controller import DatabaseController

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

# TODO Cambiar nombre de método a validar() solamente, porque se estan validando varias cosas
if Manejador().validarVacio(pedidos):
    sys.exit()
    

db = DatabaseController('pizzeria_database.db')
db.cargar_registros(pedidos)
# db.print_datase()

total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
#generadorResumen(total_ordenes).mostrarPedidos()
resumenXfecha = GeneradorResumen(total_ordenes).generarListaResumen()

for dia in resumenXfecha:
    dia.mostrarResumen()