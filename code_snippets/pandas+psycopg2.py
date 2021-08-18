#!/usr/bin/env python3
# coding: utf-8
#
# $Id: log2csv.py 1486 2021-02-12 17:38:09Z gruiick $
# SPDX-License-Identifier: BSD-2-Clause

"""

from https://gist.github.com/jakebrinkmann/de7fd185efe9a1f459946cf72def057e

"""

import pandas as pd
import psycopg2


conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, username, pwd))
sql = "select count(*) from table;"
dat = pd.read_sql_query(sql, conn)
conn.close()
