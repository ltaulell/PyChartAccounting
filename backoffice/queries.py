#!/usr/bin/env python3
# coding: utf-8

# $Id$
# SPDX-License-Identifier: BSD-2-Clause

# Copyright 2021 Loïs Taulelle
# Copyright 2021 Damien LE BORGNE

"""
perform some queries on database

# https://towardsdatascience.com/reshape-pandas-dataframe-with-pivot-table-in-python-tutorial-and-visualization-2248c2012a31
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it/56746204#56746204

# https://www.epochconverter.com/

"""

import argparse
import logging
import datetime
import pandas as pd
from pprint import pprint
import psycopg2

import config

log = logging.getLogger()
stream_handler = logging.StreamHandler()
log.addHandler(stream_handler)

# TODO/FIXME
# make it a function, from first day of the year to first day of the next year
YEARS = [(1262304000, 1293840000),
         (1293840000, 1325376000),
         (1325376000, 1356998400),
         (1356998400, 1388534400),
         (1388534400, 1420070400),
         (1420070400, 1451606400),
         (1451606400, 1483228800),
         (1483228800, 1514764800)
         ]
"""
         (1514764800, 1546300800),
         (1546214400, 1577836800),
         (1577836800, 1609459200),
         (1609459200, 1640995200)
         ]
"""


def get_args(helper=False):
    """ read parser and return args (as args namespace),
        if helper=True, show usage() or help()
    """
    parser = argparse.ArgumentParser(description='query accounting database')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug ON')

    if helper:
        return parser.print_usage()
    else:
        return parser.parse_args()


def execute_sql(connexion, commande, payload, commit=False, fetchall=False):
    """ execute commande, always return id
    SQL inserts MUST returning ids, else fetchone() will fail """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(commande, payload)
            if commit:
                connexion.commit()
            log.debug('status: {}'.format(cursor.statusmessage))
            if fetchall:
                return cursor.fetchall()
            else:
                return cursor.fetchone()

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

    # sql_str = ''.join(['SELECT ', id_name, ' FROM ', table, ' WHERE ', name, ' LIKE (%s);'])
    sql_str = """ SELECT groupes.group_name, sum(job_.cpu) AS sum_cpu, count(job_.id_job_) AS nb_job
                  FROM job_, groupes
                  WHERE job_.id_groupe = groupes.id_groupe
                  AND start_time >= (%s)
                  AND start_time <= (%s)
                  GROUP BY groupes.group_name
                  ORDER BY sum_cpu DESC; """

    result = execute_sql(conn, sql_str, payload, fetchall=True)
    log.debug('select: {}'.format(result))
    return result


if __name__ == '__main__':
    """ """
    args = get_args()

    if args.debug:
        log.setLevel('DEBUG')
        log.debug(get_args(helper=True))

    # prepare la config locale pgsql
    param_conn_db = config.parserIni(filename='infodb.ini', section='postgresql')
    log.debug(param_conn_db)

    data = []

    try:
        with psycopg2.connect(**param_conn_db) as conn:
            log.debug(conn)

            for epoch in YEARS:
                start, end = epoch
                year = datetime.datetime.fromtimestamp(start).strftime('%Y')
                print('année: {}'.format(year))
                resultats = prepare_select(conn, epoch)
                log.debug('resultats: {}'.format(resultats))

                for (groupe, secondes, jobs) in resultats:
                    heures = int(secondes / 3600)
                    log.debug('resultat: {}, {}, {}'.format(groupe, jobs, heures))

                    data.append([groupe, year, 'time', heures])
                    data.append([groupe, year, 'jobs', jobs])

            # pprint(data)
            df_long = pd.DataFrame(data, columns=['groupes', 'year', 'type', 'results'])

    except psycopg2.Error as e:
        log.debug(e.diag.message_primary)

    log.debug(df_long.columns)
    # pprint(df_long.describe())
    df_wide = df_long.pivot_table(index='groupes',
                                  columns=['year', 'type'],
                                  values='results',
                                  fill_value=0)
    pprint(df_wide)
    df_wide.to_csv('accounting_groups_.csv', encoding='utf-8')
