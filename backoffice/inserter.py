#!/usr/bin/env python3
# coding: utf-8

# $Id$
# SPDX-License-Identifier: BSD-2-Clause

# Copyright 2021 Loïs Taulelle
# Copyright 2021 Damien LE BORGNE

"""
Insert data from accounting file into database

go easy, go simple.

TODO/FIXME:

- use last_offset from history to seek() csv file -> speedup on restart
    - do not save last_offset at -each- line? save @end of process? NO! each line!
    -> howto @end of process ?
    - rewrite the read procedure to include offset <- DONE
    -> test_read_tell.py <- OK
- get rid of decomment() by ricochet <- OK

- except(s)
    https://www.psycopg.org/docs/errors.html

"""

import argparse
import logging
import csv
import sys
import psycopg2
import yaml
import datetime as dt

import config

log = logging.getLogger()
stream_handler = logging.StreamHandler()
log.addHandler(stream_handler)

CLUSTERS_FILE = 'config/clusters.yml'
METAGROUPES_FILE = 'config/metagroups.yml'
HEADER_LIST = ['qname', 'host', 'group', 'owner', 'job_name', 'job_id', 'account', 'priority', 'submit_time', 'start', 'end', 'fail', 'exit_status', 'ru_wallclock', 'ru_utime', 'ru_stime', 'ru_maxrss', 'ru_ixrss', 'ru_ismrss', 'ru_idrss', 'ru_isrss', 'ru_minflt', 'ru_majflt', 'ru_nswap', 'ru_inblock', 'ru_oublock', 'ru_msgsnd', 'ru_msgrcv', 'ru_nsignals', 'ru_nvcsw', 'ru_nivcsw', 'project', 'department', 'granted_pe', 'slots', 'task_number', 'cpu', 'mem', 'io', 'category', 'iow', 'pe_taskid', 'maxvmem', 'arid', 'ar_submission_time']


def get_args(helper=False):
    """ read parser and return args (as args namespace),
        if helper=True, show usage() or help()
    """
    parser = argparse.ArgumentParser(description='upload accounting file into database')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug ON')
    parser.add_argument('-v', '--verbose', action='store_true', help='toggle verbose ON')
    # parser.add_argument('-n', '--dryrun', action='store_true', help='dry run')
    parser.add_argument('-i', '--input', nargs=1, type=str, help='input (accounting file')

    if helper:
        return parser.print_usage()
    else:
        return parser.parse_args()


def execute_sql(connexion, commande, payload, commit=False):
    """ execute commande, always return id
    SQL inserts MUST returning ids, else fetchone() will fail """
    try:
        with connexion.cursor() as cursor:
            cursor.execute(commande, payload)
            if commit:
                connexion.commit()
            log.debug(cursor.statusmessage)
            return cursor.fetchone()
    except psycopg2.errors.StringDataRightTruncation as e:
        # if job_name or project is too long, ignore job, there's a problem.
        log.warning('insertion error: {}'.format(e))
        pass
    except psycopg2.errors.NotNullViolation as e:
        # if any of 'NOT NULL' field is null, ignore job, there's a problem.
        log.warning('notnull error: {}'.format(e))
        pass


def select_or_insert(conn, table, id_name, payload, name=None, multi=False, insert=True):
    """ Prepare the SQL statements, payload MUST be a list """

    log.debug('payload: {}'.format(payload))

    if multi is False:
        sql_str = ''.join(['SELECT ', id_name, ' FROM ', table, ' WHERE ', name, ' LIKE (%s);'])
        result = execute_sql(conn, sql_str, payload)
        log.debug('select: {}'.format(result))

        if result is None and insert is True:
            sql_str = ''.join(['INSERT INTO ', table, '(', name, ') VALUES (%s) RETURNING ', id_name, ';'])
            result = execute_sql(conn, sql_str, payload, commit=True)
            log.debug('insert: {}'.format(result))

    else:
        id1, id2 = id_name
        sql_str = ''.join(['SELECT ', id1, ',', id2, ' FROM ', table, ' WHERE ', id1, ' = (%s) AND ', id2, ' = (%s);'])
        result = execute_sql(conn, sql_str, payload)
        log.debug('select: {}'.format(result))

        if result is None and insert is True:
            sql_str = ''.join(['INSERT INTO ', table, '(', id1, ',', id2, ') VALUES (%s, %s) RETURNING ', id1, ',', id2, ';'])
            result = execute_sql(conn, sql_str, payload, commit=True)
            log.debug('insert: {}'.format(result))

    return result


def load_yaml_file(yamlfile):
    """ Load yamlfile, return a dict

        yamlfile is mandatory, using safe_load
        Throw yaml errors, with positions, if any, and quit.
        return a dict
    """
    try:
        with open(yamlfile, 'r') as f:
            contenu = yaml.safe_load(f)
            return contenu
    except IOError:
        log.critical('Unable to read/load config file: {}'.format(f.name))
        sys.exit(1)
    except yaml.MarkedYAMLError as erreur:
        if hasattr(erreur, 'problem_mark'):
            mark = erreur.problem_mark
            msg_erreur = "YAML error position: ({}:{}) in ".format(mark.line + 1,
                                                                   mark.column)
            log.critical('{} {}'.format(msg_erreur, f.name))
        sys.exit(1)


def lire_fichier(fichier, offset=0):
    """ try read without direct csv.DictReader and use an offset """
    try:
        with open(fichier, "rt", encoding='latin1') as csvfile:
            # encodings: us-ascii < latin1 < utf-8
            # but read with 'latin1' because of
            # "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3..."

            log.debug('current offset: {}'.format(offset))

            if offset != 0:
                csvfile.seek(offset, 0)  # wc match ok

            ligne = csvfile.readline()

            while ligne:
                offset = csvfile.tell()

                if not ligne.startswith('#'):  # decomment()
                    reader = csv.DictReader([ligne], fieldnames=HEADER_LIST, delimiter=':')
                    yield offset, reader

                ligne = csvfile.readline()

    except IndexError:
        log.critical('cannot read {}, not found'.format(csvfile))


if __name__ == '__main__':
    """
        pd.read_csv autodetecte des types qui sont ensuite poussés vers la base,
        et ça bloque à l'insert. LT: je reviens sur un open simple (de toute façon,
        c'est du ligne à ligne, ça va pas plus vite)
    """

    args = get_args()

    if args.debug:
        log.setLevel('DEBUG')
        log.debug(get_args(helper=True))
    elif args.verbose:
        log.setLevel('INFO')

    if args.input:
        fichier = ''.join(args.input)
        log.debug('input: {}'.format(fichier))
    else:
        log.warning('no input file!')
        sys.exit(1)

    # prepare yaml dictionnaries
    CLUSTERS = load_yaml_file(CLUSTERS_FILE)
    METAGROUPES = load_yaml_file(METAGROUPES_FILE)

    # prepare la config locale pgsql
    param_conn_db = config.parserIni(filename='infodb.ini', section='insertion')
    log.debug(param_conn_db)

    conn = psycopg2.connect(**param_conn_db)
    # conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    # conn.set_session(isolation_level=psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE, autocommit=True)
    log.debug(conn)

    # get last offset (and test conn)
    sql = ("SELECT last_offset_position FROM history WHERE id_insertion = (SELECT MAX(id_insertion) FROM history);")
    res = execute_sql(conn, sql, [])
    last_offset = int(res[0])

    for offset, datarow in lire_fichier(fichier, offset=last_offset):
        for line in datarow:
            log.debug('{}, {}, {}, {}'.format(line['qname'], line['host'], line['group'], line['cpu']))

            with conn:
                # queue
                idQueue = select_or_insert(conn, table='queues', id_name='id_queue', name='queue_name', payload=[line['qname']])

                # host
                idHost = select_or_insert(conn, table='hosts', id_name='id_host', name='hostname', payload=[line['host']])

                # group
                idGroup = select_or_insert(conn, table='groupes', id_name='id_groupe', name='group_name', payload=[line['group']])

                # user/login/owner
                idUser = select_or_insert(conn, table='users', id_name='id_user', name='login', payload=[line['owner']])

                # hosts_in_queues
                newload = [idQueue, idHost]
                id_HostinQueue = select_or_insert(conn, table='hosts_in_queues', id_name=['id_queue', 'id_host'], payload=newload, multi=True)

                # users_in_groupes
                newload = [idGroup, idUser]
                id_HostinQueue = select_or_insert(conn, table='users_in_groupes', id_name=['id_groupe', 'id_user'], payload=newload, multi=True)

                # hosts_in_clusters
                try:
                    cluster = [key for key in CLUSTERS for value in CLUSTERS[key].split() if value in line['host']][0]
                except IndexError:
                    # fallback to default
                    cluster = 'default'

                idCluster = select_or_insert(conn, table='clusters', id_name='id_cluster', name='cluster_name', payload=[cluster], insert=False)

                if idCluster:
                    newload = [idCluster, idHost]
                    id_HostinCluster = select_or_insert(conn, table='hosts_in_clusters', id_name=['id_cluster', 'id_host'], payload=newload, multi=True)

                # groupes_in_metagroupes
                try:
                    metagroupe_group = [key for key in METAGROUPES for value in METAGROUPES[key].split() if value in line['group']][0]
                except IndexError:
                    # fallback to default
                    metagroupe_group = 'autres_ENS'

                idMetaGroup = select_or_insert(conn, table='metagroupes', id_name='id_metagroupe', name='meta_name', payload=[metagroupe_group], insert=False)

                if idMetaGroup:
                    newload = [idMetaGroup, idGroup]
                    id_GroupinMeta = select_or_insert(conn, table='groupes_in_metagroupes', id_name=['id_metagroupe', 'id_groupe'], payload=newload, multi=True)

                # users_in_metagroupes
                # il y a trés peu d'users dans les metagroupes
                try:
                    metagroupe_user = [key for key in METAGROUPES for value in METAGROUPES[key].split() if value == line['owner']][0]

                    idMetaUser = select_or_insert(conn, table='metagroupes', id_name='id_metagroupe', name='meta_name', payload=[metagroupe_user], insert=False)

                    if idMetaUser:
                        newload = [idMetaUser, idUser]
                        id_UserinMeta = select_or_insert(conn, table='users_in_metagroupes', id_name=['id_metagroupe', 'id_user'], payload=newload, multi=True)

                except IndexError:
                    # no default, simply move on
                    pass

                # finally, job

                sql = ("SELECT id_queue, id_host, id_user, job_id, start_time, end_time FROM job_ WHERE id_queue = (%s) AND id_host = (%s) AND id_user = (%s) AND job_id = (%s) AND start_time = (%s) AND end_time = (%s);")
                data = [idQueue[0], idHost[0], idUser[0], line['job_id'], line['start'], line['end']]
                jobExist = execute_sql(conn, sql, data)

                if jobExist is None:
                    sql = (""" INSERT INTO job_(id_queue,
                                            id_host,
                                            id_groupe,
                                            id_user,
                                            job_name,
                                            job_id,
                                            submit_time,
                                            start_time,
                                            end_time,
                                            failed,
                                            exit_status,
                                            ru_wallclock,
                                            ru_utime,
                                            ru_stime,
                                            project,
                                            slots,
                                            cpu,
                                            mem,
                                            io,
                                            maxvmem)
                            VALUES (%s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s)
                            RETURNING id_job_; """)
                    data = [idQueue[0],
                            idHost[0],
                            idGroup[0],
                            idUser[0],
                            line['job_name'],
                            line['job_id'],
                            line['submit_time'],
                            line['start'],
                            line['end'],
                            line['fail'],
                            line['exit_status'],
                            line['ru_wallclock'],
                            line['ru_utime'],
                            line['ru_stime'],
                            line['project'],
                            line['slots'],
                            line['cpu'],
                            line['mem'],
                            line['io'],
                            line['maxvmem'],
                            ]

                    jobCommit = execute_sql(conn, sql, data, commit=True)
                    log.info('commited: {}, {}, {}'.format(line['job_id'], line['qname'], line['host']))

                    # add offset to database
                    date_insert = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    sql = ("""INSERT INTO history(last_offset_position, date_insert) 
                        VALUES(%s, %s) RETURNING id_insertion; """)
                    data = [offset, date_insert]
                    insertCommit = execute_sql(conn, sql, data, commit=True)

                else:
                    log.info('job {} already exist in database'.format(line['job_id']))

    conn.close()
