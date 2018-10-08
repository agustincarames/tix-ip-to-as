#!/usr/bin/python
# -*- coding: utf-8 -*-
#FunIamhere
from sgmllib import SGMLParser
import os
import sys
import urllib2
from ftplib import FTP
import hashlib
import gzip
import bz2
import re
from datetime import timedelta, date, datetime
from unicodedata import normalize

#parser para obtener los archivos de descarga disponibles en una pagina web saca los href
class Parser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []

    def start_a(self, attrs):
        href = [v for k, v in attrs if k=='href']
        if href:
            self.urls.extend(href)


####eliminar elementos repetidos de una lista y/o devuelve ordenados alfabeticamente

    ### Ordena Alfabeticamente
def ordena_1(lista):
    '''
    ordena_1(lista)
    lista: una lista de elementos 
    retorna una lista de elementos no repetidos ordenados alfabeticamente 
    '''
    lstOrdFilt = sorted(list(set(lista)))
    return lstOrdFilt

#check MD5
def check_md5(archivo):
    check='False'
    if  os.path.isfile(archivo) and os.path.isfile(archivo+'.md5'):
        md5=hashlib.md5()
        fileAux=open(archivo, 'rb')
      
        for line in fileAux:
            md5.update(line)
            f=open(archivo+'.md5', 'rb')
            m=re.findall(r'\w{32}',f.readline())
   
            if m and md5.hexdigest() == m[0]:
                check='True'
            #    print 'check md5... ok\n'
            #else:
            #    print 'check md5... bad\n' 
            f.close()
        fileAux.close()
    #else:
        #print 'check md5... bad\n' 
    if check:
         print 'check md5 ... ok\n'
    else:
        print 'check md5 ... ok\n'
    return check

### comprimir archivo en gz
def comGZ(archivoIN, archivoOUT=''):
    if not os.path.exists(archivoIN):
        print 'archivo no existe'
        return False
    f_in = open(archivoIN, 'rb')
    if archivoOUT == '':
        archivoOUT = archivoIN + '.gz'
    elif not archivoOUT.endswith('.gz'):
        archivoOUT = archivoOUT + '.gz'
    f_out = gzip.open(archivoOUT, 'wb')     
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()


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

### descomprimir archivos .bz2 
def descomBZ2(archivoIN, archivoOUT=''):
    #print 'descomprimiendo archivo...\n'
    if not os.path.exists(archivoIN):
        print 'archivo no existe'
        return False
    if not archivoIN.endswith('.bz2'):
        print 'archivo no es .bz2'
        return False
    if archivoOUT == '':
        archivoOUT = archivoIN[:-4]
    if archivoOUT.endswith('.bz2'):
        archivoOUT = archivoOUT[:-4]
    inF = bz2.BZ2File(archivoIN, 'rb')
    s=inF.read()
    inF.close()
    outF = open(archivoOUT, 'wb');
    outF.write(s)
    outF.close()
    return True


### descarga de archivos
def descarga(server,carpeta=[],archivo=[], destino=os.getcwd(), proto='ftp', proxy=''):
    print 'descargando archivo: ' + archivo + ' ...\n'

    if proto == 'http':
        try:
            webFile = urllib2.urlopen(server + archivo)
            localFile = open(destino + archivo, 'wb' )
            localFile.write(webFile.read())
            webFile.close()
            localFile.close()    
            return True
        except:
            print 'error en la descarga' 
            try: 
                os.remove( destino + archivo )
                return False
            except:
                return False
 
    if not proxy =='':
        if proto == 'ftp':
            try:
                ftpFile = urllib2.urlopen('ftp://' + server + carpeta + archivo )
                localFile = open( destino + archivo, 'wb' )
                localFile.write(ftpFile.read())
                ftpFile.close()
                localFile.close()
                return True
            except:
                print 'no se pudo realizar la descarga' 
                try: 
                    os.remove( destino + archivo )
                    return False
                except:
                    return False

    else:
        if proto == 'ftp':
            try:
                ftp = FTP(server)
                ftp.login()
                ftp.cwd(carpeta)
                ftp.retrbinary('RETR ' + archivo, open(destino + archivo,'wb').write)
                ftp.quit()
                return True
            except:
                print 'no se pudo realizar la descarga'
                try: 
                    os.remove( destino + archivo )
                    return False
                except:
                    return False
 
     
### genera una lista de archivos para descargar de los diferentes lugares
def lista_archivo_server(server,carpeta=[],proto='ftp', proxy=''):
    '''
    server: es la direccion url del servidor 
    carpeta: es la carpeta del servidor 
    proto: protocolo ftp o http
    retorna una lista con los nombres de los archivos disponibles para descargar
    si no encuentra nada retorna una lista vacia
    '''

    dirs=[]

    if proto == 'http':
        #print 'Obteniendo lista de archivos del servidor http: ' + server + '...\n'
        try:
            URLv = urllib2.urlopen(server)
            DownloadURL = Parser()
            DownloadURL.feed(URLv.read())
            DownloadURL.close()
            URLv.close()
            dirs = DownloadURL.urls[5:]
        except:
            print 'no se pudo listar los archivos'

    if not proxy == '':
        try:

            if proto == 'ftp':
                #print 'Obteniendo lista de archivos del servidor: ' + server + '...\n'
                URLf = urllib2.urlopen('ftp://'+server+carpeta)
                DownloadURL = Parser()
                DownloadURL.feed(URLf.read())
                dirsaux = DownloadURL.urls
                URLf.close()
                DownloadURL.close()
                for i in dirsaux:
                    aux2=i.split(';')[0]
                    dirs.append(aux2) 
                dirs=ordena_1(dirs)

        except:
            print 'server caido no se pudo listar los archivos'

    else:
        try:
            if proto == 'ftp':
                ftp = FTP(server)
                ftp.login()
                ftp.cwd(carpeta)
                dirs = ftp.nlst()
                ftp.quit()
        except:
            print 'server caido o no se pudo listar los archivos'
 
    return dirs

########################################################
# parametros globales usados en los diferentes scripts #
########################################################

def parametrosGlobales():
    dirTrabajo = os.path.abspath(os.path.dirname(__file__)) + '/'
    try:
        dicVariables={}
        archivoVariables = open(dirTrabajo + "variables.conf", "r")
        lista_conf = archivoVariables.readlines()
        for linea in lista_conf:
            linea = linea.strip()
            if not (linea.startswith('#') or linea.startswith('\n') or linea == ''):
                if ( ('=' in linea) and (linea.startswith('proxy') or linea.startswith('dias')) ) or ( ('=' in linea) and (linea.endswith('/')) ):
                  #  print linea.split('=')
                    parametro = linea.split('=')
                    dicVariables[parametro[0].strip()] = parametro[1].strip()
                else:
                    print 'los directorios deben terminar con slash (/) o variable dias o proxy no estan definidos\n las variables que deven existir son: cgi_datos_dir, redesdir, mapasdir,\n lanetvidir, lanetvilogdir, logdir, descargasdir,dias, proxy'
                    exit(1)
                    
        return dicVariables

    except:
        print 'error en variables.conf'
