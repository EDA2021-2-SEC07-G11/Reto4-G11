"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'conexiones': None, 'rutas':None, 'ciudades': None, 'aeropuertos': None}
    catalog['conexiones'] = gr.newGraph(datastructure='ADJ_LIST', directed=False,size=14000,comparefunction=compareAirports)
    catalog['rutas'] = gr.newGraph(datastructure='ADJ_LIST', directed=True,size=14000,comparefunction=compareAirports)
    catalog['aeropuertos'] = mp.newMap(maptype='CHAINING', loadfactor= 4.0)
    catalog['ciudades'] = lt.newList(datastructure='ARRAY_LIST',cmpfunction=compareCities)
    return catalog

# Funciones para agregar informacion al catalogo
def agregarRuta(catalog, ruta):
    rutas = catalog['rutas']
    salida = ruta['Departure']
    llegada = ruta['Destination']
    distancia = ruta['distance_km']
    if(gr.containsVertex(rutas, salida)):
        if gr.containsVertex(rutas, llegada):
            if gr.getEdge(rutas, salida, llegada) == None :
                gr.addEdge(rutas, salida, llegada, distancia)
                if gr.getEdge(rutas, llegada, salida) != None:
                    agregarConexion(catalog, salida, llegada, distancia)
        else:
            gr.insertVertex(rutas, llegada)
            gr.addEdge(rutas, salida, llegada, distancia)
    else:
        gr.insertVertex(rutas, salida)
        if gr.containsVertex(rutas, llegada):
            gr.addEdge(rutas, salida, llegada, distancia)
        else:
            gr.insertVertex(rutas, llegada)
            gr.addEdge(rutas, salida, llegada, distancia)

def agregarConexion(catalog, salida, llegada, distancia):
    conexiones = catalog['conexiones']
    if(gr.containsVertex(conexiones, salida)):
        if gr.containsVertex(conexiones, llegada):
            if gr.getEdge(conexiones, salida, llegada) == None :
                gr.addEdge(conexiones, salida, llegada, distancia)
        else:
            gr.insertVertex(conexiones, llegada)
            gr.addEdge(conexiones, salida, llegada, distancia)
    else:
        gr.insertVertex(conexiones, salida)
        if gr.containsVertex(conexiones, llegada):
            gr.addEdge(conexiones, salida, llegada, distancia)
        else:
            gr.insertVertex(conexiones, llegada)
            gr.addEdge(conexiones, salida, llegada, distancia)

def agregarAeropuerto(catalog, aeropuerto):
    aeropuertos = catalog['aeropuertos']
    nombre = aeropuerto['IATA']
    mp.put(aeropuertos,nombre, aeropuerto)

def agregarCiudad(catalog, ciudad):
    ciudades = catalog['ciudades']
    nombre = ciudad['city']
    lt.addLast(ciudades, ciudad)


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def compareAirports(a1, a2):
    a2 = a2['key']
    if a1 > a2:
        return 1
    elif a2 > a1:
        return -1
    else:
        return 0

def compareCities(c1, c2):
    if c1 > c2:
        return 1
    elif c2 > c1:
        return -1
    else:
        return 0

# Funciones de ordenamiento
