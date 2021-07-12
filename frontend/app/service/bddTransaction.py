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

    def fetch(self, command, fetchOne=False):
        if fetchOne:
            try:
                with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(command)
                    log.debug('status: {}'.format(cur.statusmessage))
                    bddRet = dict(cur.fetchone())
                    answerBdd = {}
                    for k, v in bddRet.items():
                        if bddRet[k] is None:
                            answerBdd[k] = 0
                        else:
                            answerBdd[k] = v
                    return answerBdd

            except psycopg2.errors.SyntaxError as Err:
                log.warning('Erreur de syntax: {}'.format(Err))
                return 0
            except psycopg2.errors.UndefinedColumn as Err:
                log.warning('Erreur de colonne: {}'.format(Err))
                return 0
            except psycopg2.errors.UndefinedTable as Err:
                log.warning('Erreur de table: {}'.format(Err))
                return 0
            except Exception as Err:
                return 0
        else:
            try:
                bddRet = pd.read_sql_query(command, self.conn)
                bddRet = bddRet.to_dict('r')
                return bddRet[0]
            except IndexError:
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