#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import time


'''
la base de datos iamhere debe existir
con las siguientes tablas, linknodes (red armada conexion de ases tiene columna de id, columna numero as1, columna numero as2) , paisnodes (numero de as y columna con pais y columna con nic, indexar por numero de as)
'''

def conectardb():
    db_host = 'mysql'
    usuario = 'tix'
    clave = 'tix'
    base_de_datos = 'iptoas'
    conndb = mdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)
    cursor = conndb.cursor()
    return cursor, conndb

### creacion tablas base tmp
def reddbtmp(nombrered):
    '''
    nombrered: path y nombre del archivo que contiene la red a cargar
    crea y carga la tabla de enlaces de la red
    '''

    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS linknodestmp;')
    cursor.execute('CREATE TABLE linknodestmp (link_id int AUTO_INCREMENT, nodeA INT, nodeB BIGINT, frec INT, PRIMARY KEY (link_Id) );')

    datared = open(nombrered, 'r')

    for linea in datared:
        nodos = linea.split('\t')
        if not '.' in nodos[0] and not '.' in nodos[1]:
            node1 = int(nodos[0].strip())
            node2 = int(nodos[1].strip())
            frec = int(nodos[2].strip())
            cursor.execute( 'INSERT INTO iptoas.linknodestmp (nodeA, nodeB, frec) VALUES (%s,%s,%s);', (node1, node2, frec) )

    conndb.commit()

    datared.close()    
    cursor.close()
    conndb.close()


def paisdbtmp(archivopais):
    '''
    archivodb: lista con los archivo con los paises de los nodos
    crea y carga la tabla de paises de los nodos
    '''
    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS paisnodestmp;')
    cursor.execute('CREATE TABLE paisnodestmp (nodep INT, pais CHAR(2), nic TEXT, PRIMARY KEY (nodep) );')

    for archivo in archivopais:
        datapais = open(archivo, 'r')
        for indice in datapais:
            linea = indice.split('|')
            if len(linea)>=4 and linea[2] == 'asn' and linea[1]!='*':
                nodo = linea[3].strip()
                pais = linea[1].strip()
                nic = archivo.split('/')[-1]
#
                cursor.execute( 'INSERT INTO iptoas.paisnodestmp (nodep, pais, nic) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE pais=%s, nic=%s;', (nodo,pais,nic, pais, nic) )
    conndb.commit()
    datapais.close()

    cursor.close()
    conndb.close()

def nombreasdbtmp(archivoasn):
    '''
    archivoasn: archivo con los nombres de los ases
    crea y carga la tabla con los nombres de los nodos
    '''
    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS namenodestmp;')
    cursor.execute('CREATE TABLE namenodestmp (noden INT, name TEXT, PRIMARY KEY (noden) );')

    dataname = open(archivoasn, 'r')

    for linea in dataname:
        datos = linea.split('\t')
        if len(datos) == 2:
            nodo = datos[0].strip()
            name = unicode(datos[1].strip(),'latin-1')
            cursor.execute( 'INSERT INTO iptoas.namenodestmp (noden, name) VALUES (%s,%s) ON DUPLICATE KEY UPDATE name=name;', (nodo,name) )
    conndb.commit()

    dataname.close()    
    cursor.close()
    conndb.close()


### CREACION DE TABLAS
def reddb():
    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS linknodes;')
    cursor.execute('CREATE TABLE linknodes LIKE linknodestmp;')
    cursor.execute('INSERT INTO linknodes SELECT * FROM linknodestmp;')

    conndb.commit()
    cursor.close()
    conndb.close()

def paisdb():
    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS paisnodes;')
    cursor.execute('CREATE TABLE paisnodes LIKE paisnodestmp;')
    cursor.execute('INSERT INTO paisnodes SELECT * FROM paisnodestmp;')

    conndb.commit()
    cursor.close()
    conndb.close()

def nombreasdb():
    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS namenodes;')
    cursor.execute('CREATE TABLE namenodes LIKE namenodestmp;')
    cursor.execute('INSERT INTO namenodes SELECT * FROM namenodestmp;')

    conndb.commit()
    cursor.close()
    conndb.close()

def nicdb(archivonic, nic):
    '''
    archivnic: lista con los archivo de los diferentes nic (afrinic, apnic, arin, lacnic, ripe) que contiene
    los paises asignados por ip. Se crea y carga la tabla de paises ip y cantidad de host por nic
    '''
    cursor, conndb = conectardb()
#    afrinic|ZA|ipv4|198.54.148.0|256|19930505|assigned

    if nic in ['afrinic', 'apnic', 'arin', 'lacnic', 'ripe']:
        cursor.execute('DROP TABLE IF EXISTS ' + nic + ';')
        cursor.execute('CREATE TABLE ' + nic + ' (' + nic + '_id int AUTO_INCREMENT, pais_' + nic + ' CHAR(2), ip_' + nic + ' TEXT, host_' + nic + ' INT, fecha_' + nic + ' INT, cond_' + nic + ' TEXT, PRIMARY KEY (' + nic + '_id) );')
    else:
        print 'nic no conocido use afrinic, apnic, arin, lacnic, ripe'
        exit(1)

    datanic = open(archivonic, 'r')
    for indice in datanic:
        linea = indice.split('|')
        if linea[0].startswith(nic) and len(linea)==7 and linea[2] == 'ipv4':
            pais = linea[1].strip()
            ip = linea[3].strip()
            hosts = linea[4].strip()
            fecha = linea[5].strip()
            cond = linea[6].strip()
            cursor.execute( 'INSERT INTO iptoas.' + nic + ' (pais_' + nic + ', ip_' + nic + ', host_' + nic + ', fecha_' + nic + ', cond_' + nic + ') VALUES (%s,%s,%s,%s,%s);', (pais, ip, hosts, fecha, cond) )
    conndb.commit()
    datanic.close()
    cursor.close()
    conndb.close()

def routerviewdb(archivorouter):
    '''
    archivorouter: archivo caida routerviews contiene ip mascara y numero de as
    '''
    cursor, conndb = conectardb()

    cursor.execute('DROP TABLE IF EXISTS routerviews;')
    cursor.execute('CREATE TABLE routerviews (router_id int AUTO_INCREMENT, noderouter BIGINT, ip_router TEXT, mask INT, PRIMARY KEY (router_id) );')

    datarouter = open(archivorouter, 'r')

    for linea in datarouter:
        datos = linea.split('\t')
        if len(datos) == 3:
            ip = datos[0].strip()
            mask = datos[1].strip()
            nodo = datos [2].strip()
            cursor.execute( 'INSERT INTO iptoas.routerviews (noderouter, ip_router, mask) VALUES (%s,%s,%s);', (nodo, ip, mask) )
    conndb.commit()
    datarouter.close()    
    cursor.close()
    conndb.close()

#######################################################################################################
### BUSQUEDA DE INFO
def findnodosname():
    '''
    busca los nombres de los nodos de la red completa si no tiene nombre pone un string vacio
    '''
    cursor, conndb = conectardb()
    sql = 'SELECT nodeA, IFNULL(name,"") AS name FROM (SELECT nodeA FROM linknodestmp UNION SELECT nodeB FROM linknodestmp) AS nodealias LEFT JOIN namenodestmp ON noden=nodeA ORDER BY nodeA;'

    cursor.execute(sql)
    resultado=cursor.fetchall()
    cursor.close()
    conndb.close ()
    lstnodosname=[]
    for nodo in resultado:
        node = nodo[0]
        nombre = nodo[1]
        #pais = nodo[2]
        #nic = nodo[3]
        lstnodosname.append(str(node) + '\t' + nombre)
    return lstnodosname

def findnodospais():
    '''
    busca los paises de los nodos de la red completa
    '''
    cursor, conndb = conectardb()
    sql = 'SELECT nodeA, IFNULL(pais,"") FROM (SELECT nodeA FROM linknodestmp UNION SELECT nodeB FROM linknodestmp) AS nodealias LEFT JOIN paisnodestmp ON nodep=nodeA GROUP BY nodeA;'

    cursor.execute(sql)
    resultado=cursor.fetchall()
    cursor.close()
    conndb.close ()
    lstnodospais=[]
    for nodo in resultado:
        node = nodo[0]
        pais = nodo[1]
        lstnodospais.append(str(node) + '\t' + pais)
    return lstnodospais
