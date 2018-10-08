#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import gzip
from datetime import timedelta, date, datetime

### descomprimir archivos .gz 
def descomGZ(archivoIN, archivoOUT=''):
    #print 'descomprimiendo archivo...\n'
    if not os.path.exists(archivoIN):
        print 'archivo no existe'
        return False
    if not archivoIN.endswith('.gz'):
        print 'archivo no es .gz'
        return False 
    if archivoOUT == '':
        archivoOUT = archivoIN[:-3]
    if archivoOUT.endswith('.gz'):
        archivoOUT = archivoOUT[:-3]
    inF = gzip.GzipFile(archivoIN, 'rb');
    s=inF.read()
    inF.close()
    outF = open(archivoOUT, 'wb');
    outF.write(s)
    outF.close()
    return True

##########################################        
# unir un string con una lista de string #
##########################################
def str_mas_lista_str(cadena,lstcadena):
    salida=[]
    for element in lstcadena:
        salida.append(cadena+element)
    return salida

#######################################################
# selector de archivos fechados de los ultimos x dias #
#######################################################
def selectforlastdays(carpeta, days, separador, ubicacionfecha):
    '''
    la fecha debe estar en formato, year, month, day y de forma completa 20130501
    carpeta: carpeta donde se encuantran los archivos
    days(int): cantidad de dias de los archivos con los que me quedo una semana = 7
    separador: para hacer el split con que caracter separar
    ubucacionfecha: en que posicion se encuentra la fecha se puede usar indice negativo
    '''
    listaArchivos=sorted(os.listdir(carpeta), reverse = True)[:days]
    #print listaArchivos
    hoy = date.today()
    intervalo = hoy - timedelta(days=days)
    listaFILES = []
    for archivo in listaArchivos:
        datofecha = archivo.split(separador)[ubicacionfecha]
        fecha = datofecha[:4] + '-' + datofecha[4:6] + '-' + datofecha[6:8]
        fechatime = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fechatime > intervalo:
            listaFILES.append(archivo)
    return listaFILES
