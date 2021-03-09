#!/usr/bin/env python3
# coding: utf-8

# $Id$
# SPDX-License-Identifier: BSD-2-Clause

# Copyright 2021 Loïs Taulelle
# Copyright 2021 Damien LE BORGNE

"""
perform some queries on database

-- # https://www.epochconverter.com/
-- epoch (2010-01-01) 1262304000
-- epoch (2010-12-31) 1293753600
-- epoch (2011-12-31) 1325289600
-- epoch (2012-12-31) 1356912000
-- epoch (2013-12-31) 1388448000
-- epoch (2014-12-31) 1419984000
-- epoch (2015-12-31) 1451520000
-- epoch (2016-12-31) 1483142400
-- epoch (2017-12-31) 1514678400
-- epoch (2018-12-31) 1546214400
-- epoch (2019-12-31) 1577750400
-- epoch (2020-12-31) 1609372800
-- epoch (2021-12-31) 1640908800

"""

# import argparse
import logging
import psycopg2
import datetime
# from pprint import pprint

import config

log = logging.getLogger()
stream_handler = logging.StreamHandler()
log.addHandler(stream_handler)
# log.setLevel('DEBUG')

YEARS = [(1262304000, 1293753600),
         (1293753600, 1325289600),
         (1325289600, 1356912000),
         (1356912000, 1388448000),
         (1388448000, 1419984000),
         (1419984000, 1451520000),
         (1451520000, 1483142400),
         (1483142400, 1514678400)
         ]
"""
         (1514678400, 1546214400),
         (1546214400, 1577750400),
         (1577750400, 1609372800),
         (1609372800, 1640908800)
         ]
"""


def execute_sql(connexion, commande, payload, commit=False):
    """ execute commande, always return id
    SQL inserts MUST returning ids, else fetchone() will fail """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(commande, payload)
            if commit:
                connexion.commit()
            log.debug('status: {}'.format(cursor.statusmessage))
            # return cursor.fetchone()
            return cursor.fetchall()

    except psycopg2.errors.StringDataRightTruncation as e:
        # if job_name or project is too long, ignore job, there's a problem.
        log.warning('insertion error: {}'.format(e))
        pass
    except psycopg2.errors.NotNullViolation as e:
        # if any of 'NOT NULL' field is null, ignore job, there's a problem.
        log.warning('notnull error: {}'.format(e))
        pass
    except psycopg2.errors.ProgrammingError as e:
        # if cursor.execute() did not produce any result
        log.warning('fetch error: {}'.format(e))
        pass


def prepare_select(conn, payload):
    """ """
    log.debug('payload: {}'.format(payload))

    # start, end = payload
    # sql_str = ''.join(['SELECT ', id_name, ' FROM ', table, ' WHERE ', name, ' LIKE (%s);'])
    sql_str = """ SELECT groupes.group_name, sum(job_.cpu) AS sum_cpu, count(job_.id_job_) AS nb_job
                  FROM job_, groupes
                  WHERE job_.id_groupe = groupes.id_groupe
                  AND start_time >= (%s)
                  AND start_time <= (%s)
                  GROUP BY groupes.group_name
                  ORDER BY sum_cpu DESC; """

    result = execute_sql(conn, sql_str, payload)
    log.debug('select: {}'.format(result))
    return result


if __name__ == '__main__':
    """ """
    # prepare la config locale pgsql
    param_conn_db = config.parserIni(filename='infodb.ini', section='postgresql')
    log.debug(param_conn_db)

    try:
        with psycopg2.connect(**param_conn_db) as conn:
            log.debug(conn)
            for year in YEARS:
                start, end = year
                # print(datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d'))
                # print(datetime.datetime.fromtimestamp(end).strftime('%Y-%m-%d'))
                print('année: {}'.format(datetime.datetime.fromtimestamp(end).strftime('%Y')))
                resultat = prepare_select(conn, year)
                # pprint(resultat)
                for groupe, secondes, nb in resultat:
                    print('{};{};{:.0f}'.format(groupe, nb, secondes / 3600))

    except psycopg2.Error as e:
        log.debug(e.diag.message_primary)
