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
        print('El grafo dirigido de rutas tiene '+str(gr.numVertices(rutas))+' aeropuertos diferentes, y '+str(gr.numVertices(rutas))+' rutas aéreas. El primer aeropuerto registrado fue: ')
        primero = lt.firstElement(gr.vertices(rutas))
        primero = mp.get(catalog['aeropuertos'], primero)
        primero = me.getValue(primero)
        conexiones = catalog['conexiones']
        print("Nombre: "+primero['Name']+ "\nCiudad: "+ primero['City']+ "\nPais: "+ primero['Country']+ "\nLatitud: "+ primero['Latitude']+ "\nLongitud: "+ primero['Longitude'])
        print('El grafo no dirigido de conexiones tiene '+str(gr.numVertices(conexiones))+' aeropuertos diferentes, y '+str(gr.numVertices(conexiones))+' rutas aéreas. El primer aeropuerto registrado fue: ')
        ciudades = catalog['ciudades']
        primero = lt.firstElement(gr.vertices(conexiones))
        primero = mp.get(catalog['aeropuertos'], primero)
        primero = me.getValue(primero)
        print("Nombre: "+primero['Name']+ "\nCiudad: "+ primero['City']+ "\nPais: "+ primero['Country']+ "\nLatitud: "+ primero['Latitude']+ "\nLongitud: "+ primero['Longitude'])
        print('Se han cargado '+ str(lt.size(ciudades))+ ' ciudades. La última ciudad cargada fue: ')
        ultima = lt.lastElement(ciudades)
        print("Nombre: "+ultima['city']+ "\nPoblación: "+ ultima['population']+"\nLatitud: "+ ultima['lat']+ "\nLongitud: "+ ultima['lng'])

    else:
        sys.exit(0)
sys.exit(0)
