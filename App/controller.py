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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    archivoAeropuertos = cf.data_dir + 'Skylines/airports-utf8-small.csv'
    input_file = csv.DictReader(open(archivoAeropuertos, encoding='utf-8'))
    for aeropuerto in input_file:
        model.agregarAeropuerto(catalog, aeropuerto)
    archivoRutas = cf.data_dir + 'Skylines/routes-utf8-small.csv'
    input_file = csv.DictReader(open(archivoRutas, encoding='utf-8'))
    for ruta in input_file:
        model.agregarRuta(catalog, ruta)
    archivoCiudades = cf.data_dir + 'Skylines/worldcities-utf8.csv'
    input_file = csv.DictReader(open(archivoCiudades, encoding='utf-8'))
    for ciudad in input_file:
        model.agregarCiudad(catalog, ciudad)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def datosCarga(catalog):
    return model.datosCargaAeropuertos(catalog)

def datosCargaCiudades(catalog):
    return model.datosCargaCiudades(catalog)

def ciudadesHomonimas(lista):
    return model.darCiudadesHomonimas(lista)

def aeropuertoCercano(catalog, ciudad):
    return model.aeropuertoCercano(catalog, ciudad)

def infoAeropuerto(aeropuerto):
    return model.datosAeropueto2(aeropuerto)

def infoCamino(pila):
    return model.datosCamino(pila)

def darConectados(catalog):
    return model.darConectados(catalog)

def darMST(catalog,aeropuerto):
    return model.darMST(catalog,aeropuerto)

def eliminarAeropuerto(catalog, eliminado):
    return model.darVerticesAfectados(catalog, eliminado)

def datosFinal(lista):
    return model.darInfoUltimo(lista)