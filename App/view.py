"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as dij


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Crear el catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Encontrar puntos de interconexión aérea")
    print("4- Encontrar clústeres de tráfico aéreo")
    print("5- Encontrar la ruta más corta entre ciudades")
    print("6- Utilizar las millas de viajero")
    print("7- Cuantificar el efecto de un aeropuerto cerrado")
    print("0- Salir")


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Creando el catalogo...")
        catalog = controller.initCatalog()

    elif int(inputs[0]) == 2:
        print('Cargando la información en el catálogo...')
        controller.loadData(catalog)
        rutas = catalog['rutas']
        print('=== Airports-Routes DiGraph === \n'+str(lt.size(catalog['aeropuertos']))+' loaded airports. \n'+str(gr.numEdges(rutas))+' loaded routes.')
        print('Nodes: '+str(gr.numVertices(rutas))+' & Edges: '+str(gr.numEdges(rutas)))
        print('First & Last Airport loaded in the DiGraph.')
        datos = controller.datosCarga(catalog)
        print(tabulate(datos, headers=['Name', 'City','Country','Latitude','Longitude'], tablefmt='fancy_grid'))
        conexiones = catalog['conexiones']
        print('=== Airports-Routes Graph === \n'+str(lt.size(catalog['aeropuertos']))+' loaded airports. \n'+str(gr.numEdges(conexiones))+' loaded routes.')
        print('Nodes: '+str(gr.numVertices(conexiones))+' & Edges: '+str(gr.numEdges(conexiones)))
        print('First & Last Airport loaded in the Graph.')
        print(tabulate(datos, headers=['Name', 'City','Country','Latitude','Longitude'], tablefmt='fancy_grid'))
        Ciudades = catalog['Ciudades']
        print('Number of cities: '+ str(lt.size(Ciudades))+ '\n First & Last city loaded in the data structure:')
        datos = controller.datosCargaCiudades(catalog)
        print(tabulate(datos, headers=['City', 'Contry','Population','Latitude','Longitude'], tablefmt='fancy_grid'))
    elif int(inputs[0])==3:
        respuesta = controller.darConectados(catalog)
        datos = respuesta[0]
        numero = respuesta[1]
        print('Connected airports inside network: '+str(numero))
        print('Top 5 most connected airports')
        print(tabulate(datos, headers=['IATA','Name','City', 'Contry','Connections'], tablefmt='fancy_grid'))
        
    elif int(inputs[0]) == 4:
        componentes = scc.KosarajuSCC(catalog['rutas'])
        print('Number of SCC in Airport-Route network: '+str(componentes['components']))
        a1 = input('Airport-1 IATA Code: ')
        if gr.containsVertex(catalog['rutas'], a1):
            a2 = input('Airport-2 IATA Code: ')
            if gr.containsVertex(catalog['rutas'], a2):
                if scc.stronglyConnected(componentes, a1, a2) == True:
                    print('Los aeropuertos SI pertenecen al mismo componente.')
                else:
                    print('Los aeropuertos NO pertenecen al mismo componente.')
            else:
                print('El aeropuerto con IATA '+a2+' no se encuentra en la base de datos.')
        else:
           print('El aeropuerto con IATA '+a1+' no se encuentra en la base de datos.') 
    elif int(inputs[0]) == 5:
        salida = input('Departure City: ')
        if mp.contains(catalog['ciudades'], salida):
            salida = mp.get(catalog['ciudades'], salida)
            lista = me.getValue(salida)
            lista = lista.copy()
            if lt.size(lista) == 1:
                salida = lt.firstElement(lista)
            else:
                print('Se encontró más de una ciudad con este nombre: ')
                datos = controller.ciudadesHomonimas(lista)
                print(tabulate(datos, headers=['Position','City', 'Contry','Admin_name','Population','Latitude','Longitude'], tablefmt='fancy_grid'))
                pos = input('Seleccione la posición de la ciudad: ')
                if 0<int(pos)<=lt.size(lista):
                    salida = lt.getElement(lista, int(pos))   
            llegada = input('Arrival City: ')
            if mp.contains(catalog['ciudades'], llegada) and llegada != salida:
                llegada = mp.get(catalog['ciudades'], llegada)
                lista = me.getValue(llegada)
                lista = lista.copy()
                if lt.size(lista) == 1:
                    llegada = lt.firstElement(lista)
                else:
                    print('Se encontró más de una ciudad con este nombre: ')
                    datos = controller.ciudadesHomonimas(lista)
                    print(tabulate(datos, headers=['Position','City', 'Contry','Admin_name','Population','Latitude','Longitude'], tablefmt='fancy_grid'))
                    pos = input('Seleccione la posición de la ciudad: ')
                    if(0<int(pos) <= lt.size(lista)):
                        llegada = lt.getElement(lista, int(pos)) 
                print('The departure airport in '+salida['city']+ ' is:')
                hola = controller.aeropuertoCercano(catalog, salida)
                salida = hola['Aeropuerto']
                distancia = hola['Distancia']
                print(tabulate(controller.infoAeropuerto(salida), headers=['IATA','Name','City', 'Contry'], tablefmt='fancy_grid'))
                print('The arrival airport in '+llegada['city']+ ' is:')
                hola = controller.aeropuertoCercano(catalog, llegada)
                llegada = hola['Aeropuerto']
                distancia = distancia + hola['Distancia']
                print(tabulate(controller.infoAeropuerto(llegada), headers=['IATA','Name','City', 'Country'], tablefmt='fancy_grid'))
                caminos = dij.Dijkstra(catalog['rutas'],salida['IATA'])
                camino = dij.pathTo(caminos, llegada['IATA'])
                if camino != None:
                    distancia = round(distancia + dij.distTo(caminos, llegada['IATA']),2)    
                    print('+++ Dijkstra\'s trip details +++')
                    print('Total Distance: '+str(distancia)+' (km)')
                    datos = controller.infoCamino(camino)
                    print(tabulate(datos, headers=['Departure','Destination', 'Distance'], tablefmt='fancy_grid'))
                else:
                    print('No existe una ruta posible entre las dos ciudades')

            elif llegada == salida:
                print('Ha ingresado la misma ciudad.')
            else:
                print('La ciudad no se encuentra en la base de datos')
            
        else:
            print('La ciudad '+salida+ ' no se encuentra en la base de datos')
    elif int(inputs[0]) == 6:
        
        salida = input('Departure IATA code: ')
        if mp.contains(catalog['Aeropuertos'], salida):
            millas = float(input('Available Travel Miles: '))
            respuesta = controller.darMST(catalog,salida)
            print('Number of possible airports: '+ str(respuesta[0]))
            print('Traveling distance sum between airports: '+ str(respuesta[1]))
            print('Passenger available traveling miles: '+str(round(float(millas)*1.6,2))+' (km)')
            print('+++ Longest Possible route with airport '+salida+' +++')
            print('Longest possible path distance: '+str(respuesta[2]))
            print('Longest possible path details: ')
            print(tabulate(respuesta[3], headers=['Departure','Destination','Distance'], tablefmt='fancy_grid'))
            millas = (respuesta[3]*2/1.6)-millas
            if millas > 0:
                print('The passenger needs '+str(millas)+' miles to complete the trip')
            else:
                print('The passenger will be with '+str(-1*millas)+' miles after completing the trip')

        else:
            print('Este aeropuerto no se encuentra en la base de datos.')
    elif(int(inputs[0])==7):
        cerrado = input('Closing the airport with IATA code: ')
        lista = controller.eliminarAeropuerto(catalog, cerrado)
        print('There are '+ str(lt.size(lista))+' Airports affectedby the removal of '+cerrado)
        print('The 5 first and last 3 airports affected are: ')
        datos = controller.datosFinal(lista)
        print(tabulate(datos, headers=['IATA','Name','City', 'Contry'], tablefmt='fancy_grid'))
    else:
        sys.exit(0)
sys.exit(0)
