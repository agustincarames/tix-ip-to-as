#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import time

'''
la base de datos iptoas debe existir
'''

#TODO: Recibir estos valores por configuracion
def _conectar():
    db_host = 'localhost'
    usuario = 'tix'
    clave = 'tix'
    base_de_datos = 'tix'
    conndb = mdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)
    cursor = conndb.cursor()
    return cursor, conndb

### creacion tablas base tmp
def nombre_as(archivoasn):
    '''
    archivoasn: archivo con los nombres de los ases
    crea y carga la tabla con los nombres de los nodos
    '''
    cursor, conndb = _conectar()

    with open(archivoasn, 'r') as dataname:
        cursor.execute('DROP TABLE IF EXISTS namenodestmp;')
        cursor.execute('CREATE TABLE namenodestmp (noden INT, name TEXT, PRIMARY KEY (noden) );')
        for linea in dataname:
            datos = linea.split('\t')
            if len(datos) == 2:
                nodo = datos[0].strip()
                name = unicode(datos[1].strip(), 'latin-1')
                cursor.execute('INSERT INTO iptoas.namenodestmp (noden, name) VALUES (%s,%s) ON DUPLICATE KEY UPDATE name=name;', (nodo,name))
        conndb.commit()

    cursor.close()
    conndb.close()

def routerview(archivorouter):
    '''
    archivorouter: archivo caida routerviews contiene ip mascara y numero de as
    '''
    cursor, conndb = _conectar()

    with open(archivorouter, 'r') as datarouter:
        cursor.execute('DROP TABLE IF EXISTS routerviews_tmp;')
        cursor.execute('CREATE TABLE routerviews_tmp (router_id int AUTO_INCREMENT, noderouter BIGINT, ip_router TEXT, mask INT, PRIMARY KEY (router_id) );')
        for linea in datarouter:
            datos = linea.split('\t')
            if len(datos) == 3:
                ip = datos[0].strip()
                mask = datos[1].strip()
                nodo = datos [2].strip()
                cursor.execute('INSERT INTO iptoas.routerviews_tmp (noderouter, ip_router, mask) VALUES (%s,%s,%s);', (nodo, ip, mask))
        conndb.commit()
    
    cursor.close()
    conndb.close()

def rotate_tables():
    cursor, conndb = _conectar()

    cursor.execute('DROP TABLE IF EXISTS namenodes;')
    cursor.execute('CREATE TABLE namenodes LIKE namenodestmp;')
    cursor.execute('INSERT INTO namenodes SELECT * FROM namenodestmp;')
    cursor.execute('DROP TABLE IF EXISTS namenodestmp;')
    
    cursor.execute('DROP TABLE IF EXISTS routerviews;')
    cursor.execute('CREATE TABLE routerviews LIKE routerviews_tmp;')
    cursor.execute('INSERT INTO routerviews SELECT * FROM routerviews_tmp;')
    cursor.execute('DROP TABLE IF EXISTS routerviews_tmp;')
    conndb.commit()
    
    cursor.close()
    conndb.close()
