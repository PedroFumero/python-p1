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
while opt != '8':
    existe_db = db.tiene_datos()
    existe_csv = os.path.exists('misc/pizzeria.csv')
    print()
    print('-'*25, 'Menu inicial', '-'*25)
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
    elif opt == '6' and existe_db:
        # Respaldar DB en un .csv
        registros = db.obtenerPedidos()
        registros.insert(0, "usuario,fecha,precio_total,numero_pedido,pizza,ingrediente".split(','))
        ruta_archivo = "misc/pizzeria.csv"
        with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as csvfile:
            pizzeria_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            pizzeria_writer.writerows(registros)
        continue
    elif opt == '7' and existe_csv:
        # Cargar desde un archivo .csv
        ruta_archivo = "misc/pizzeria.csv"
        with open(ruta_archivo, encoding='utf-8', newline='') as csvfile:
            pizzeria_reader = csv.reader(csvfile, delimiter=';')
            registros = list(pizzeria_reader)
            registros = registros[1:] # Elminamos la primera fila de headers
        pedidos = db.procesarRegistros(registros)
    elif opt == '8':
        sys.exit()


    # Valida posibles errores en la lectura del archivo
    if not Manejador().validar(pedidos):
        
        # Procesar pedidos de los clientes
        total_ordenes = ProcesadorOrdenes().procesarPedidos(pedidos)
        # Crear un generador con las ordenes procesadas
        generador = GeneradorResumen(total_ordenes)
        # Generar lista resumen   True = guardar archivo
        resumenXfecha = generador.generarListaResumen(True)

        print()
        print('-'*25, 'Menu final', '-'*25)
        opt_2 = '0'
        while opt_2 not in ['1','2','3','4','5']:
            print("1 - Mostrar en pantalla monto a cobrar a cada cliente")
            print("2 - Mostrar en pantalla resumen por dia")
            print("3 - Cargar datos en base de datos")
            print("4 - Continuar")
            print("5 - Salir")
            opt_2 = input('Opción: ')
            
        if opt_2 == '1':
            # Mostrar cuanto cobrar a cada cliente
            dicCobro = generador.generarDiccionarioCobro()
            for fecha in dicCobro:
                print (fecha + '\n')
                for k,v in dicCobro[fecha].items():
                    print(' ' + k,str(v) +' UMs')
                print('\n')

        elif opt_2 == '2':
            # Mostrar resumen
            for dia in resumenXfecha:
                dia.mostrarResumen()

        elif opt_2 == '3':
            # Cargar datos a BD si no vienen de la BD
            print("¿ Seguro que desea cargar estos datos en la base de datos?")
            print("Considere que cargar varias veces el mismo archivo puede generar datos duplicados")
            opt_db = input('[si/no]: ')
            if opt_db.lower() in ['y', 'yes', 's', 'si', 'sí']:
                db.cargar_registros(pedidos)

        elif opt_2 == '5':
            sys.exit()            
