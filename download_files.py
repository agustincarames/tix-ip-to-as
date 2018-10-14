#!/usr/bin/python
# -*- coding: utf-8 -*-

import lxml.html
from lxml.cssselect import CSSSelector
import os
import shutil
import urllib.request
import datetime
import re
import gzip

import conf

def compress_gz(origen, destino):
    with open(origen, 'rb') as i:
        with gzip.open(destino, 'wb') as o:
            o.writelines(i)

def descarga(origen, destino):
    with open(destino, 'wb') as localFile:
        print(origen)
        with urllib.request.urlopen(origen) as webFile:
            localFile.write(webFile.read())
            

def lista_archivos_remotos(search_regex, url):
    '''Lista archivos a los que enlaza una pagina'''
    print(url)
    with urllib.request.urlopen(url) as remote:
        dom = lxml.html.fromstring(remote.read())
        selector = CSSSelector('a')
        foundElements = selector(dom)
        urls = [e.get('href') for e in foundElements]

    for item in reversed(sorted(urls)):
        match = re.search(search_regex, item)
        if match:
            yield (url + item, match.group(1))

#def log_error(name):
#    fechahora = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
#    with open(conf.logDownloadPath, 'a+') as descarga_log:
#        descarga_log.write(fechahora + ' -- ' + name + ' DOWNLOAD FAIL\n')
            
def download_asn():
    nombre = 'asn-' + str(datetime.date.today()).replace('-', '')
    nombrecomp = nombre + '.gz'
    if os.path.isfile(conf.asnDownloadPath + nombrecomp):
        return

    descarga(origen = 'http://www.potaroo.net/bgp/iana/asn.txt',
             destino = conf.tmpDownloadPath + nombre)
    compress_gz(origen = conf.tmpDownloadPath + nombre,
                destino = conf.tmpDownloadPath + nombrecomp)
    shutil.move(conf.tmpDownloadPath + nombrecomp,
                conf.asnDownloadPath + nombrecomp)
    return conf.asnDownloadPath + nombrecomp

def download_rv():
    available = []
    errors = 0
    for (year_url, year) in lista_archivos_remotos('(\d{4})/', 'http://data.caida.org/datasets/routing/routeviews-prefix2as/'):
        for (month_url, month) in lista_archivos_remotos('(\d{2})/', year_url):
            for (file_url, date) in lista_archivos_remotos('routeviews-rv2-(\d{8}-\d{4}).pfx2as.gz', month_url):
                name = 'rv-' + date + '.gz'
                try:
                    if not os.path.isfile(conf.rvDownloadPath + name):
                        descarga(origen = file_url,
                                 destino = conf.tmpDownloadPath + name)
                        shutil.move(conf.tmpDownloadPath + name,
                                    conf.rvDownloadPath + name)
                    available.append(conf.rvDownloadPath + name)
                except Exception as e:
                    errors += 1
                    if errors >= 5:
                        raise errors

                if len(available) >= conf.routeviews_required:
                    return available
    return available
