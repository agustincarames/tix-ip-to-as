#!/usr/bin/python

import codecs

###############################################################################
# genera un diccionario a partir de los archivos asn
###############################################################################
def concatenar_asn(archivos, arch_sal):
    '''
    archivos asn a concatenar lista ordenada del mas nuevo al mas viejo
    '''
    diccnombre = {}
    for arch in archivos:
        with codecs.open(arch, 'r', encoding='iso-8859-15') as fileasn:
            lineas = fileasn.readlines()
        for linea in lineas:
            nodo = linea.split('\t')[0]
            nombre = linea.split('\t')[1]
            if nodo not in diccnombre:
                diccnombre[nodo] = nombre
    
    arch_salida = open(arch_sal, 'w')
    for clave in diccnombre:
        info = clave + '\t' + diccnombre[clave]
        arch_salida.write(info)
    arch_salida.close()
    return True


def concatenar_routerviews(archivos, arch_sal):
    '''
    archivos routerview a concatenar lista ordenada del mas nuevo al mas viejo
    '''
    diccrouterviews = {}
    for arch in archivos:
        with codecs.open(arch, 'r', encoding='iso-8859-15') as filerouter:
            lineas = filerouter.readlines()
        for linea in lineas:
            parts = linea.split('\t')
            ip = parts[0]
            mascara = parts[1]
            nodoas = parts[2]
            if not ('_' in nodoas or ',' in nodoas or '.' in nodoas):
                key = ip + '\t' + mascara
                if key not in diccrouterviews:
                    diccrouterviews[key] = linea
    
    arch_salida = open(arch_sal, 'w')
    for v in diccrouterviews.values():
        arch_salida.write(v)
    arch_salida.close()
    return True
