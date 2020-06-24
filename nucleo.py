import sys

from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import ResumenDelDia,GeneradorResumen
from database_controller import DatabaseController

# Inicializacion de la Base de Datos
db = DatabaseController('pizzeria_database.db')
existe_db = db.tiene_datos()
print(existe_db)

# Menú de opciones
opt = Manejador().menu(0, existe_db)
if opt == '1':
    # Cargar pedidos desde un archivo
    ruta_archivo = Manejador().getRutaArchivo()
    pedidos = Manejador().cargarArchivo(ruta_archivo)
elif opt == '2':
    # Cargar todos los pedidos en la carpeta /misc
    pedidos = ProcesadorOrdenes().procesarTodos()
    # print(pedidos)
elif opt == '3' and existe_db:
    # Cargar desde la base de datos
    pedidos = db.obtenerPedidos()


# TODO Cambiar nombre de método a validar() solamente, porque se estan validando varias cosas
if Manejador().validarVacio(pedidos):
    sys.exit()
    
total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
#generadorResumen(total_ordenes).mostrarPedidos()
resumenXfecha = GeneradorResumen(total_ordenes).generarListaResumen()

for dia in resumenXfecha:
    dia.mostrarResumen()

# Cargar datos a BD si no vienen de la BD
if opt != '3':
    print("¿Desa cargar estos datos en la base de datos?")
    print("Considere que cargar varias veces el mismo archivo puede generar datos duplicados")
    opt_db = input('[si/no]: ')
    if opt_db.lower() in ['y', 'yes', 's', 'si', 'sí']:
        db.cargar_registros(pedidos)

#print(pedidos)
#db.print_datase()
