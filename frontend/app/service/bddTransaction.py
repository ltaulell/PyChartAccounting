#!/usr/bin/env python3
# coding: utf-8
# Ce programme a été écrit par Damien LE BORGNE le 28/01/2021
# Gestion Lecture base de données

import psycopg2
from psycopg2.sql import SQL, Identifier
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from psycopg2.extras import RealDictCursor
import pandas as pd
import logging

from app.utils import parserIni


log = logging.getLogger(__name__)

class BddTransaction(object):
    
    def __init__(self, fichierConfig: str):
        
        self.paramsDb = None

        try:
            self.paramsDb = parserIni(filename=fichierConfig, section='postgresql')
        except(Exception) as Err:
            log.warning(Err)
            raise(Err)
        
        self.conn = self.__establishCon()

    def __establishCon(self):
        """
            Etablier la connexion avec la base de données
        """
        try:
            conn = psycopg2.connect(**self.paramsDb) #Connexion à la base de données
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            log.info('Connect with {0}'.format(self.paramsDb))
            return conn
            
        except (Exception, psycopg2.OperationalError) as Err:
            log.warning(Err)
            raise(Err)
    
    def disconnectCon(self):
        """
            Fermer la liaison avec la base de données
        """
        self.conn.close()

    def version(self):
        cur = self.conn.cursor() #Ouvrir le cursor
        cur.execute('SELECT version()') #Executer une commande
        db_version = cur.fetchone() #Recuperer la réponse
        cur.close() #Fermer le cursor
        return db_version #Retourner la réponse

    def fetch(self, command):
        try:
            bddRet = pd.read_sql_query(command, self.conn)
            bddRet = bddRet.to_dict('records')
            if(len(bddRet) < 2):
                return bddRet[0]
            return bddRet

        except psycopg2.errors.SyntaxError as e:
            log.warning('Erreur de syntax: {}'.format(e))
            return 0
        except psycopg2.errors.UndefinedColumn as e:
            log.warning('Erreur de colonne: {}'.format(e))
            return 0
        except psycopg2.errors.UndefinedTable as e:
            log.warning('Erreur de table: {}'.format(e))
            return 0
        except Exception as e:
            return 0

            


    def fetchAll(self, command):
        try:
            dat = pd.read_sql_query(command, self.conn)
        except:
            dat = None
        return dat

    def listUser(self):
        sql = """SELECT login FROM users;""" 
        dat = pd.read_sql_query(sql, self.conn)
        return dat

    def listQueues(self):
        sql = """SELECT queue_name FROM queues;""" 
        dat = pd.read_sql_query(sql, self.conn)
        return dat

    def listClusters(self):
        sql = """SELECT cluster_name FROM clusters;""" 
        dat = pd.read_sql_query(sql, self.conn)
        return dat

    def listGroupes(self):
        sql = """SELECT group_name FROM groupes;""" 
        dat = pd.read_sql_query(sql, self.conn)
        return dat

    def findGroupByUser(self, nom):
        if nom != None:
            sql = """select group_name from users, groupes, users_in_groupes
                        where users.id_user = users_in_groupes.id_user
                        and groupes.id_groupe = users_in_groupes.id_groupe
                        and users.login = '%s'
                    """
            dat = pd.read_sql_query(sql%(nom), self.conn)
            return dat
        else:
            pass

"""
sql.SQL and sql.Identifier are needed to avoid SQL injection attacks.
cur.execute(sql.SQL('CREATE DATABASE {};').format(
    sql.Identifier(self.db_name)))
"""