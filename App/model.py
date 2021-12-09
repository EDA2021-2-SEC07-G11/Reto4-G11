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


from App.controller import eliminarAeropuerto
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import stack as stack
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sh
assert cf
from math import radians, cos, sin, asin, sqrt
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.ADT import queue as q
from DISClib.Algorithms.Graphs import dfo as dfo

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {'conexiones': None, 'rutas':None, 'ciudades': None, 'aeropuertos': None}
    catalog['conexiones'] = gr.newGraph(datastructure='ADJ_LIST', directed=False,size=14000,comparefunction=compareAirports)
    catalog['rutas'] = gr.newGraph(datastructure='ADJ_LIST', directed=True,size=14000,comparefunction=compareAirports)
    catalog['aeropuertos'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['Aeropuertos'] = mp.newMap(maptype='CHAINING',loadfactor=4.0)
    catalog['ciudades'] = mp.newMap(maptype='CHAINING',loadfactor=4.0)
    catalog['Ciudades'] = lt.newList(datastructure='ARRAY_LIST')
    return catalog

# Funciones para agregar informacion al catalogo
def agregarRuta(catalog, ruta):
    rutas = catalog['rutas']
    salida = ruta['Departure']
    llegada = ruta['Destination']
    distancia = float(ruta['distance_km'])

    gr.addEdge(rutas, salida, llegada, distancia)
    if gr.getEdge(rutas, llegada, salida) != None:
        agregarConexion(catalog, salida, llegada, distancia)


def agregarConexion(catalog, salida, llegada, distancia):
    conexiones = catalog['conexiones']
    
    if gr.getEdge(conexiones, salida, llegada) == None :
        gr.addEdge(conexiones, salida, llegada, distancia)

def agregarAeropuerto(catalog, aeropuerto):

    aeropuertos = catalog['aeropuertos']
    lt.addLast(aeropuertos,aeropuerto)
    mp.put(catalog['Aeropuertos'],aeropuerto['IATA'],aeropuerto)
    rutas = catalog['rutas']
    gr.insertVertex(rutas, aeropuerto['IATA'])
    conexiones = catalog['conexiones']
    gr.insertVertex(conexiones, aeropuerto['IATA'])

def agregarCiudad(catalog, ciudad):
    ciudades = catalog['ciudades']
    nombre = ciudad['city']
    if mp.contains(ciudades,nombre):
        entrada = mp.get(ciudades, nombre)
        lista = me.getValue(entrada)
        lt.addLast(lista, ciudad)
    else:
        lista = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lista,ciudad)
        mp.put(ciudades, nombre, lista)
    lt.addLast(catalog['Ciudades'],ciudad)




    


# Funciones para creacion de datos

# Funciones de consulta
def datosCargaAeropuertos(catalog):
    aeropuertos = catalog['aeropuertos']
    primero = lt.firstElement(aeropuertos)
    ultimo = lt.lastElement(aeropuertos)
    datos = []
    datos.append(datosAeropueto(primero))
    datos.append(datosAeropueto(ultimo))
    return datos

def datosAeropueto(aeropuerto):
    return aeropuerto['Name'],aeropuerto['City'],aeropuerto['Country'],aeropuerto['Latitude'],aeropuerto['Longitude']

def datosAeropueto2(aeropuerto):
    datos =[]
    datos.append([aeropuerto['IATA'],aeropuerto['Name'],aeropuerto['City'],aeropuerto['Country']])
    return datos

def datosCargaCiudades(catalog):
    ciudades = catalog['Ciudades']
    primero = lt.firstElement(ciudades)
    ultimo = lt.lastElement(ciudades)
    datos = []
    datos.append(datosCiudad(primero))
    datos.append(datosCiudad(ultimo))
    return datos

def datosCiudad(ciudad):
    return ciudad['city'],ciudad['country'],ciudad['population'],ciudad['lat'],ciudad['lng']

def datosCiudad2(ciudad,numero):
    return numero, ciudad['city'],ciudad['country'],ciudad['admin_name'],ciudad['population'],ciudad['lat'],ciudad['lng']

def darCiudadesHomonimas(lista):
    datos = []
    n= 1
    for ciudad in lt.iterator(lista):
        datos.append(datosCiudad2(ciudad,n))
        n+= 1
    return datos

def datosCamino(pila):
    datos = []
    while stack.isEmpty(pila) == False:
        elemento = stack.pop(pila)
        datos.append([elemento['vertexA'],elemento['vertexB'],elemento['weight']])
    return datos
def aeropuertoCercano(catalog, ciudad):
    aeropuertos = catalog['aeropuertos']
    lat = float(ciudad['lat'])
    lng = float(ciudad['lng'])
    salida = None
    for i in lt.iterator(aeropuertos):
        lati = float(i['Latitude'])
        longi = float(i['Longitude'])
        distancia = haversine(lng, lat, longi, lati)
        if salida == None:
            salida = {'Aeropuerto': i, 'Distancia': distancia}
        else:
            if distancia < salida['Distancia']:
                salida = {'Aeropuerto': i, 'Distancia': distancia}
    return salida

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
    
def darConectados(catalog):
    lista = lt.newList('ARRAY_LIST')
    rutas = catalog['rutas']
    vertices = gr.vertices(rutas)
    for i in lt.iterator(vertices):
        cantidad = gr.indegree(rutas, i) + gr.outdegree(rutas, i)
        if cantidad > 0:
            lt.addLast(lista, [i,cantidad])
    lista = sh.sort(lista, cmpCantidad)
    return info5Conectados(catalog, lista), lt.size(lista)
    
def info5Conectados(catalog, lista):
    datos = []
    aeropuertos = catalog['Aeropuertos']
    n = 1
    while n < 6:
        elemento = lt.getElement(lista, n)
        aeropuerto = elemento[0]
        cantidad = elemento[1]
        aeropuerto = mp.get(aeropuertos, aeropuerto)
        aeropuerto = me.getValue(aeropuerto)
        info = [aeropuerto['IATA'], aeropuerto['Name'],aeropuerto['City'], aeropuerto['Country'], cantidad]
        datos.append(info)
        n+= 1
    return datos

def darMST(catalog, aeropuerto):
    arbol = prim.PrimMST(catalog['conexiones'])
    total = round(prim.weightMST(catalog['conexiones'], arbol),2)
    vertices = lt.size(arbol['mst'])
    conectados = dfs.DepthFirstSearch(catalog['conexiones'], aeropuerto)['visited']
    info = darInfoConectados(catalog, conectados)
    return vertices, total, info[0], info[1]

def darInfoConectados(catalog,conectados):
    llaves = mp.keySet(conectados)
    datos = []
    grafo = catalog['conexiones']
    distanciaTot = 0
    for llave in lt.iterator(llaves):
        entrada = mp.get(conectados, llave)
        valor = me.getValue(entrada)
        donde = valor['edgeTo']
        if donde != None:
            distancia = gr.getEdge(grafo, donde, llave)['weight']
            distanciaTot += distancia
            datos.append([donde, llave, distancia])
    return distanciaTot, datos

def darVerticesAfectados(catalog, eliminado):
    rutas = catalog['rutas']
    lista = lt.newList('ARRAY_LIST')
    aeropuertos = gr.vertices(rutas)
    for vertice in lt.iterator(aeropuertos):
        if gr.getEdge(rutas, eliminado, vertice) != None or gr.getEdge(rutas, vertice, eliminado):
            estaya = False
            for i in lt.iterator(lista):
                if i['IATA'] == vertice:
                    estaya = True
                    break
            if estaya == False:
                entrada = mp.get(catalog['Aeropuertos'], vertice)
                aeropuerto = me.getValue(entrada)
                lt.addLast(lista, aeropuerto)
    rutas = gr.removeVertex(rutas,eliminado)
    catalog['conexiones'] = gr.removeVertex(catalog['conexiones'],eliminado)
    return lista

def darInfoUltimo(lista):
    datos = []
    n = 0
    if 0 <lt.size(lista) < 7:
        for aeropuerto in lt.iterator(lista):
            datos.append([aeropuerto['IATA'],aeropuerto['Name'],aeropuerto['City'],aeropuerto['Country']])
    else:
        while n < 3:
            aeropuerto = lt.getElement(lista, n)
            datos.append([aeropuerto['IATA'],aeropuerto['Name'],aeropuerto['City'],aeropuerto['Country']])
            n+= 1
        n = lt.size(lista) - 3
        while n < lt.size(lista):
            aeropuerto = lt.getElement(lista, n)
            datos.append([aeropuerto['IATA'],aeropuerto['Name'],aeropuerto['City'],aeropuerto['Country']])
            n+= 1
    return datos


                    

    



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

def cmpCantidad(a1, a2):
    c1 = a1[1]
    c2 = a2[1]
    if c1 > c2:
        return 1
    elif c2 < c1:
        return -1
    else:
        return 0



# Funciones de ordenamiento
