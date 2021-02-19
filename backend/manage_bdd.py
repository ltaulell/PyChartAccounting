#!/usr/bin/env python3
# coding: utf-8

# $Id$
# SPDX-License-Identifier: BSD-2-Clause

# Copyright 2021 Damien LE BORGNE
# Copyright 2021 Loïs Taulelle

"""
WITHOUT module bdd_interact

create, or purge, database.

"""

import argparse
import logging
import distutils.util
import sys
import psycopg2

import config

log = logging.getLogger()
stream_handler = logging.StreamHandler()
log.addHandler(stream_handler)


def get_args(helper=False):
    """ read parser and return args (as args namespace),
        if helper=True, show usage() or help()
    """
    parser = argparse.ArgumentParser(description='(re)create/cleanup database (tests era)')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug ON')
    parser.add_argument('-c', '--create', action='store_true', help='create tables')
    parser.add_argument('-i', '--insert', action='store_true', help='insert preliminary tables')
    parser.add_argument('-p', '--purge', action='store_true', help='purge tables (drop)')
    parser.add_argument('-r', '--redo', action='store_true', help='purge tables, then create, then insert')

    if helper:
        return parser.print_usage()
        # return parser.print_help()
    else:
        return parser.parse_args()


def query_yesno(question):
    """ Ask a yes/no question via input() and return 1 if yes, 0 elsewhere.

    import distutils(.util)
    """
    print("\n" + question + " [y/n]?")
    while True:
        try:
            return distutils.util.strtobool(input().lower())
        except ValueError:
            print('Please reply "y" or "n".')


def db_transaction(params, fichier, action=None):
    """ using params, connect to db, execute SQL fichier """

    gonogo = query_yesno(' '.join((action, fichier)))

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curs:
                if gonogo == 1:
                    curs.execute(open(fichier, "r").read())

    except (Exception, psycopg2.Error) as db_err:
        print(db_err.pgerror)
        print(db_err.diag.message_primary)
        logging.warning(db_err)


if __name__ == '__main__':
    """ pointless-string-statement """

    args = get_args()

    if args.debug:
        log.setLevel('DEBUG')
        log.debug(get_args(helper=True))

    paramConDb = config.parserIni(filename='infodb.ini', section='postgresql')
    log.debug(paramConDb)

    if args.redo:
        args.purge = True
        args.create = True
        args.insert = True

    if args.purge:
        db_transaction(paramConDb, 'sql/cleanup.sql', action='drop')

    if args.create:
        args.insert = True
        db_transaction(paramConDb, 'sql/bdd.sql', action='create')

    if args.insert:
        db_transaction(paramConDb, 'sql/clusters_insert.sql', action='insert')
        db_transaction(paramConDb, 'sql/metagroupes_insert.sql', action='insert')

    else:
        get_args(helper=True)
        sys.exit(1)
