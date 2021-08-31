#!/usr/bin/env python3
# coding: utf-8
# Ce programme a été écrit par Damien LE BORGNE le 28/01/2021
# Fonctions utiles au fonctionnement

from configparser import ConfigParser
import os

def parserIni(filename, section):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    parserData = ConfigParser()
    #Avec le parser, lire le fichier
    parserData.read(dir_path + filename)
    paramsDb = {}
    if parserData.has_section(section):
        params = parserData.items(section)
        for param in params:
            paramsDb[param[0]] = param[1]
    else:
        raise Exception('File or Section [{0}] not found, Path: {1}'.format(section, filename))
        #créer un declencheur
    return paramsDb

def splitDict(args):
    if not args:
        return ({'value': 0})
    l = list()
    for t in args:
        l.append({t:args[t]})

    return tuple(l)
