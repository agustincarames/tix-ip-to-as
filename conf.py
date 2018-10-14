#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

basePath = os.path.abspath(os.path.dirname(__file__)) + '/files'
routeviews_required = 30

logDownloadPath = basePath + '/log'
logConcatPath = basePath + '/log'

asnDownloadPath = basePath + '/descargas/asn/'
rvDownloadPath = basePath + '/descargas/routerviews/'

tmpDownloadPath = basePath + '/tmp/descargas/'
 
tmpCompPath = basePath + '/tmp/comp/'
tmpConcatAsnPath = basePath + '/tmp/concat/asn/'
tmpConcatRvPath = basePath + '/tmp/concat/routerviews/'

def permanent_dirs():
    return [
        asnDownloadPath,
        rvDownloadPath
    ]

def temporary_dirs():
    return [
        tmpDownloadPath,
        tmpCompPath,
        tmpConcatAsnPath,
        tmpConcatRvPath
    ]

def make_dirs():
    for d in permanent_dirs() + temporary_dirs():
        if not os.path.exists(d):
            os.makedirs(d)
            
def rm_temp_dirs():
    for d in temporary_dirs():
        shutil.rmtree(d, ignore_errors=True)
