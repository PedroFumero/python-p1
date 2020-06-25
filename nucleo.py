import sys
import os
import csv

from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import ResumenDelDia,GeneradorResumen
from database_controller import DatabaseController

# Inicializacion de la Base de Datos
db = DatabaseController('misc/pizzeria_database.db')
existe_db = db.tiene_datos()
existe_csv = os.path.exists('misc/pizzeria.csv')

# Menú de opciones
opt = Manejador().menu(0, existe_db, existe_csv)
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
    registros = db.obtenerPedidos()
    pedidos = db.procesarRegistros(registros)
elif opt == '4' and existe_csv:
    # Cargar desde un archivo .csv
    ruta_archivo = "misc/pizzeria.csv"
    with open(ruta_archivo, encoding='utf-8') as csvfile:
        pizzeria_reader = csv.reader(csvfile, delimiter=',')
        registros = list(pizzeria_reader)
        # Elminamos la primera fila de headers
        registros = registros[1:]
    pedidos = db.procesarRegistros(registros)


# Valida posibles errores en la lectura del archivo
if Manejador().validar(pedidos):
    sys.exit()
    
total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
#generadorResumen(total_ordenes).mostrarPedidos()
resumenXfecha = GeneradorResumen(total_ordenes).generarListaResumen(True)
for dia in resumenXfecha:
    dia.mostrarResumen()

# Cargar datos a BD si no vienen de la BD
if opt != '3':
    print("¿Desa cargar estos datos en la base de datos?")
    print("Considere que cargar varias veces el mismo archivo puede generar datos duplicados")
    opt_db = input('[si/no]: ')
    if opt_db.lower() in ['y', 'yes', 's', 'si', 'sí']:
        db.cargar_registros(pedidos)

# Guardar datos de BD a un arcvhivo .csv
existe_db = db.tiene_datos()
if opt != '4' and existe_db:
    print("¿Desa guardar los datos de la base de datos en un archivo .csv? (misc/pizzeria.csv)")
    opt_db = input('[si/no]: ')
    if opt_db.lower() in ['y', 'yes', 's', 'si', 'sí']:
        with open('misc/pizzeria.csv', mode='w', encoding='utf-8') as csvfile:
            pizzeria_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            registros = db.obtenerPedidos()
            registros.insert(0, "usuario,fecha,precio_total,numero_pedido,pizza,ingrediente".split(','))
            pizzeria_writer.writerows(registros)

#print(pedidos)
#db.print_datase()
