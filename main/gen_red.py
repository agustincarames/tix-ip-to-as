#!/usr/bin/python

import datetime
from FunIamhere import complementa_dic


###############################################################################
# genera un diccionario a partir de los archivos de caida (teams)
###############################################################################
def inicia_dic(archivo):
    '''
    archivos caida de los teams 
    '''
    diccLink = {}
    monitorKeys = {}
    arch = open(archivo, 'r')
    lineas = arch.readlines()
    arch.close()
    for linea in lineas:
        if linea.startswith('M'):
            monitorKeys[linea.split()[3]] = linea.split()[1]
        elif linea.startswith('D') and not ('_' in linea or ',' in linea or '.' in linea):
            valor = linea.split()[3:]
            monitores = []
            for v in valor:
                monitores.append(monitorKeys[v])
            diccLink[linea.split()[1] + '\t' + linea.split()[2]] = monitores
        elif linea.startswith('I') and not ('_' in linea or ',' in linea or '.' in linea):
            elemento = linea.split()[1] + '\t' + linea.split()[2]
            if elemento not in diccLink:
                valor = linea.split()[4:]
                monitores = []
                for v in valor:
                    monitores.append(monitorKeys[v])
                diccLink[elemento] = monitores
            else:
                valor = linea.split()[4:]
                monitores_nuevos = []
                for v in valor:
                    monitores_nuevos.append(monitorKeys[v])
                monitores_cargados = diccLink[elemento]
                valor_concatenado = list(set(monitores_nuevos) | set(monitores_cargados))
                diccLink[elemento] = valor_concatenado

    return diccLink



###############################################################################
# genera la red con el valor de frecuencia de descubrimiento del enlace
###############################################################################
def red_frec(diccionario, red_frec_out='red_frec.txt', red_solo_out='red.txt'):
    '''
    entrada diccionario con enlaces y monitores que lo descubrieron, y los archivos de salida
    '''
    arch_frec = open(red_frec_out, 'w')
    arch_solo = open(red_solo_out, 'w')

    for clave in diccionario:
        dato = clave + '\t' + str(len(diccionario[clave])) + '\n'
        arch_frec.write(dato)
        arch_solo.write(clave + '\n')
    arch_frec.close()
    arch_solo.close()
    return True

def genred(teams,outfile):
    '''
    teams: lista de teams (path + nombre) del archivo de caida que se utilizaran para generar las redes
    outfile: path y nombre del archivo de salida (frec_, red_, y la fecha y hora se agregan al nombre elegido)
    retorna true si anda 
    '''
    fechahora = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    diccFinal = {}
    for archivo in teams:
        dicc = inicia_dic(archivo)
        diccFinal = complementa_dic(diccFinal, dicc)
    return red_frec(diccFinal, outfile + '-_frec', outfile ), fechahora
