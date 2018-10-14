#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
import shutil
import gzip

import create_db
import concatenar_files
import conf

def descomGZ(archivoIN, archivoOUT=''):
    if not os.path.exists(archivoIN):
        return False
    if not archivoIN.endswith('.gz'):
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

def selectforlastdays(carpeta, days):
    '''
    la fecha debe estar en formato, year, month, day y de forma completa 20130501
    carpeta: carpeta donde se encuantran los archivos
    days(int): cantidad de dias de los archivos con los que me quedo una semana = 7
    separador: para hacer el split con que caracter separar
    ubucacionfecha: en que posicion se encuentra la fecha se puede usar indice negativo
    '''
    listaArchivos=sorted(os.listdir(carpeta), reverse = True)[:days]
    hoy = datetime.date.today()
    intervalo = hoy - datetime.timedelta(days=days)
    listaFILES = []
    for archivo in listaArchivos:
        datofecha = archivo.split('-')[1].replace('.gz', '')
        fechatime = datetime.datetime.strptime(datofecha, "%Y%m%d").date()
        if fechatime > intervalo:
            listaFILES.append(archivo)
    return listaFILES

def create_clean_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)

def extract(listaArchivos, compPath):
    create_clean_dir(compPath)
    
    result = []
    for archGZ in listaArchivos:
        shutil.copy2(archGZ, compPath)
        
        filename = archGZ.split('/')[-1]
        descomGZ(compPath + filename)
        os.remove(compPath + filename)
        result.append(compPath + filename[:-3])
    return result

def concateno(name, inPath, compPath, outPath, days, concatFn):
    listaFiles = selectforlastdays(inPath, days)
    listaArchivos = [inPath + s for s in listaFiles]
    tmplistaArchivos = extract(listaArchivos, compPath)
    if concatFn(tmplistaArchivos, outPath):
        print('Concatenado ' + name)
        shutil.rmtree(compPath, ignore_errors=True)
        return True
    else:
        print('Error concatenar ' + name)
        shutil.rmtree(compPath, ignore_errors=True)
        return False

def concateno_as(inPath, compPath, outPath):
    return concateno(name = 'ASN',
                     inPath = inPath,
                     compPath = compPath,
                     outPath = outPath,
                     days = 1,
                     concatFn = concatenar_files.concatenar_asn)

def concateno_routeviews(inPath, compPath, outPath):
    return concateno(name = 'Routerviews',
                     inPath = inPath,
                     compPath = compPath,
                     outPath = outPath,
                     days = conf.routeviews_required,
                     concatFn = concatenar_files.concatenar_routerviews)

def build_files():
    concateno_as(inPath = conf.asnDownloadPath,
                 compPath = conf.tmpCompPath,
                 outPath = conf.tmpConcatAsnPath + 'asn')
    concateno_routeviews(inPath = conf.rvDownloadPath,
                         compPath = conf.tmpCompPath,
                         outPath = conf.tmpConcatRvPath + 'rv')
    
    #create_db.nombre_as(conf.tmpConcatAsnPath + 'asn')
    #create_db.routerview(conf.tmpConcatRvPath + 'rv')
    
    #create_db.rotate_tables()
