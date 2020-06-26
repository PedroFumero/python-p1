import sys
import os
import csv

from cargador_archivo import Manejador
from procesador_ordenes import ProcesadorOrdenes
from generador_resumen import ResumenDelDia,GeneradorResumen
from database_controller import DatabaseController

# Inicializacion de la Base de Datos
db = DatabaseController('misc/pizzeria_database.db')


# Menú de opciones
opt = '0'
while opt != '7':
    existe_db = db.tiene_datos()
    existe_csv = os.path.exists('misc/pizzeria.csv')
    print()
    print('-'*25)
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
    elif opt == '4' and existe_db:
        # Mostrar la base de datos
        db.print_datase()
        continue
    elif opt == '5' and existe_db:
        # Limpiar base de datos
        db.limpiar_database()
        continue
    elif opt == '6' and existe_csv:
        # Cargar desde un archivo .csv
        ruta_archivo = "misc/pizzeria.csv"
        with open(ruta_archivo, encoding='utf-8', newline='') as csvfile:
            pizzeria_reader = csv.reader(csvfile, delimiter=';')
            registros = list(pizzeria_reader)
            # Elminamos la primera fila de headers
            registros = registros[1:]
        pedidos = db.procesarRegistros(registros)
    elif opt == '7':
        sys.exit()


    # Valida posibles errores en la lectura del archivo
    if not Manejador().validar(pedidos):
        # sys.exit()
        
        # Procesar pedidos de los clientes
        total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
        # Crear un generador con las ordenes procesadas
        generador = GeneradorResumen(total_ordenes)
        # Generar lista resumen   True = guardar archivo
        resumenXfecha = generador.generarListaResumen(True)

        # Mostrar cuanto cobrar a cada cliente
        dicCobro = generador.generarDiccionarioCobro()
        for fecha in dicCobro:
            print (fecha + '\n')
            for k,v in dicCobro[fecha].items():
                print(' ' + k,str(v) +' UMs')
            print('\n')
        # Mostrar resumen
        # for dia in resumenXfecha:
        #     dia.mostrarResumen()

        # Cargar datos a BD si no vienen de la BD
        if opt != '3' and len(pedidos):
            print("¿Desea cargar estos datos en la base de datos?")
            print("Considere que cargar varias veces el mismo archivo puede generar datos duplicados")
            opt_db = input('[si/no]: ')
            if opt_db.lower() in ['y', 'yes', 's', 'si', 'sí']:
                db.cargar_registros(pedidos)

        # Guardar datos de BD a un archivo .csv
        existe_db = db.tiene_datos()
        if opt != '6' and existe_db and len(pedidos):
            print("¿Desea guardar los datos de la base de datos en un archivo .csv? (misc/pizzeria.csv)")
            opt_db = input('[si/no]: ')
            if opt_db.lower() in ['y', 'yes', 's', 'si', 'sí']:
                with open('misc/pizzeria.csv', mode='w', encoding='utf-8', newline='') as csvfile:
                    pizzeria_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    registros = db.obtenerPedidos()
                    registros.insert(0, "usuario,fecha,precio_total,numero_pedido,pizza,ingrediente".split(','))
                    pizzeria_writer.writerows(registros)

        #print(pedidos)
        #db.print_datase()
