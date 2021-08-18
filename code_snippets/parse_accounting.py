#!/usr/bin/python3
# -*- coding: utf-8 -*-

# PSMN: $Id: parse_accounting.py | Wed Sep 27 17:55:07 2017 +0200 | Loïs Taulelle  $
# SPDX-License-Identifier: CECILL-B OR BSD-2-Clause

"""
DOC:
    parsing du fichier d'accounting SGE, évaluation des consommations
    par user, groupe, etc.

TODO:

FIXME:

DONE:
    See @END
"""

#import sys
import os.path
import argparse
import datetime


def filtreDate(ligne):
    """
        filter line against args.* and import into the list of lists
    """
    # Madame is right: first, filter by date (boundaries), then filter the rest
    butoir = int(datetime.datetime.fromtimestamp(
        int(ligne[9])).strftime('%Y%m%d'))
    if args.b and butoir > debut:
        if args.e and butoir <= fin:
            if args.d:
                print(debut, "< ", butoir, "< ", fin)
            filtreLigne(ligne)
        elif not args.e:
            filtreLigne(ligne)
    elif not args.b:
        if args.e and butoir <= fin:
            filtreLigne(ligne)
        elif not args.e:
            filtreLigne(ligne)


def filtreLigne(ligne):
    # filtering discriminative AND restrictive
    # first all 4 args, then 3 args, then 2 args, then 1 args, then none of all.
    # if user and group and queue and project
    if args.u and args.g and args.q and args.P:
        if user == ligne[3] and group == ligne[2] and queue in ligne[0] and projet == ligne[31]:
            lol.append(ligne)
    # or user and queue and project and NO group
    elif args.u and args.q and args.P and not args.g:
        if user == ligne[3] and queue in ligne[0] and projet == ligne[31]:
            lol.append(ligne)
    # or user and group and project and NO queue
    elif args.u and args.g and args.P and not args.q:
        if user == ligne[3] and group == ligne[2] and projet == ligne[31]:
            lol.append(ligne)
    # or user and group and queue and NO project
    elif args.u and args.g and args.q and not args.P:
        if user == ligne[3] and group == ligne[2] and queue in ligne[0]:
            lol.append(ligne)
    # or group and queue and project (CSSI typical) and NO user
    elif args.g and args.q and args.P and not args.u:
        if group == ligne[2] and queue in ligne[0] and projet == ligne[31]:
            lol.append(ligne)
    # or user and group and NO queue and NO project
    elif args.u and args.g and not args.q and not args.P:
        if user == ligne[3] and group == ligne[2]:
            lol.append(ligne)
    # or user and project and NO group and NO queue
    elif args.u and args.P and not args.g and not args.q:
        if user == ligne[3] and projet == ligne[31]:
            lol.append(ligne)
    # or user and queue and NO group and NO project
    elif args.u and args.q and not args.g and not args.P:
        if user == ligne[3] and queue in ligne[0]:
            lol.append(ligne)
    # or group and queue and NO user and NO project
    elif args.g and args.q and not args.u and not args.P:
        if group == ligne[2] and queue in ligne[0]:
            lol.append(ligne)
    # or group and project and NO user and NO queue
    elif args.g and args.P and not args.u and not args.q:
        if group == ligne[2] and projet == ligne[31]:
            lol.append(ligne)
    # or queue and project and NO user and NO group
    elif args.q and args.P and not args.u and not args.g:
        if queue in ligne[0] and projet == ligne[31]:
            lol.append(ligne)
    # or only user
    elif args.u and not args.g and not args.q and not args.P and user == ligne[3]:
        lol.append(ligne)
    # or only group
    elif args.g and not args.u and not args.q and not args.P and group == ligne[2]:
        lol.append(ligne)
    # or only queue
    elif args.q and not args.u and not args.g and not args.P and queue in ligne[0]:
        lol.append(ligne)
    # or only project
    elif args.P and not args.u and not args.g and not args.q and projet == ligne[31]:
        lol.append(ligne)
    # or none (shit happens)
    elif not args.u and not args.g and not args.q and not args.P:
        lol.append(ligne)


"""
    Parse command line args
"""
parser = argparse.ArgumentParser(
    description="Accounting SGE, consommation CPU (beta), all arguments are optionnals")
parser.add_argument("-d", action="store_true", help="debug ON")
parser.add_argument("-i", nargs=1, help="Accounting file")
parser.add_argument("-b", nargs=1, help="begin, job started after (YYYYMMDD)")
parser.add_argument("-e", nargs=1, help="end, job started before (YYYYMMDD)")
parser.add_argument("-u", nargs=1, help="Username")
parser.add_argument("-g", nargs=1, help="Group")
parser.add_argument("-q", nargs=1, help="Queue (inclusive match)")
parser.add_argument("-P", nargs=1, help="Project (exact match)")
parser.add_argument("-s", action="store_true", help="Show some statistics")
parser.add_argument(
    "-c",
    action="store_true",
    help="Output in csv compatible format")

args = parser.parse_args()

"""
    Set flags and defaults
"""
if args.d:
    print("debug mode ON")
    print(args)

if args.i:
    ifile = str(args.i[0])
else:
    if args.d:
        print("automatic search for accounting file")
    if os.path.isfile("/gridware/sge/default/common/accounting"):
        ifile = "/gridware/sge/default/common/accounting"
    elif os.path.isfile(os.path.expanduser("~/tmp/accounting")):
        if args.d:
            print("default SGE accounting file not found")
        ifile = os.path.expanduser("~/tmp/accounting")
    elif os.path.isfile("accounting"):
        if args.d:
            print("~/tmp/ accounting file not found")
        ifile = "accounting"
    else:
        print("accounting file not found, please specify one.")
        exit(1)
    if args.d:
        print("using:", ifile)

if args.u:
    user = str(args.u[0])

if args.b:
    debut = int(args.b[0])

if args.e:
    fin = int(args.e[0])

if args.g:
    group = str(args.g[0])

if args.P:
    projet = str(args.P[0])
# liste des projets: qconf -sprjl

if args.q:
    queue = str(args.q[0])
# liste des queues: qconf -sql

"""
    Read line by line and pass to filter()
"""
lol = []
with open(ifile, "r", encoding='latin1') as fichier:
    # debug
    # if args.d:
    #    nbline = 0
    for var in fichier:
        line = var.rstrip().split(":")
        # debug
        # if args.d:
        #    nbline += 1
        if len(line) >= 10:
            # debug
            # if args.d:
            #    print(line)
            #    print()
            filtreDate(line)
    # debug
    # if args.d:
    #    if nbline >= 10:
    #        print(lol)
    #        print("exit")
    #        break

"""
    Print out the lines that passed all tests
"""
# debug de brutasse (kind of mountain troll)
# awk -F':'  '{SUM += $15} END {print SUM/3600}' accounting => utime
# awk -F':'  '{SUM += $37} END {print SUM/3600}' accounting => cpu
if args.d:
    for i in range(len(lol)):
        # See man accouting
        #print("=== suivant ==================================================")
        #print("qname        {}".format(lol[i][0]))
        #print("hostname     {}".format(lol[i][1]))
        #print("group        {}".format(lol[i][2]))
        #print("owner        {}".format(lol[i][3]))
        #print("job_name     {}".format(lol[i][4]))
        #print("job_number       {}".format(lol[i][5]))
        #print("account      {}".format(lol[i][6]))
        #print("priority     {}".format(lol[i][7]))
        #print("submission_time      {}".format(datetime.datetime.fromtimestamp(int(lol[i][8])).strftime('%Y-%m-%d %H:%M:%S')))
        #print("start_time       {}".format(datetime.datetime.fromtimestamp(int(lol[i][9])).strftime('%Y-%m-%d %H:%M:%S')))
        #print("end_time     {}".format(datetime.datetime.fromtimestamp(int(lol[i][10])).strftime('%Y-%m-%d %H:%M:%S')))
        #print("failed       {}".format(lol[i][11]))
        #print("exit_status      {}".format(lol[i][12]))
        # See man getrusage
        # print("ru_wallclock     {}".format(lol[i][13]))  # end_time minus start_time
        # print("   ru_utime      {}".format(lol[i][14]))  # total amount of time spent executing in user mode (seconds)
        # print("   ru_stime      {}".format(lol[i][15]))  # total amount of time spent executing in kernel mode (seconds)
        # print("   ru_maxrss     {}".format(lol[i][16]))  # maximum resident set size used (kilobytes)
        #print("   ru_ixrss      {}".format(lol[i][17]))
        #print("   ru_ismrss     {}".format(lol[i][18]))
        #print("   ru_idrss      {}".format(lol[i][19]))
        #print("   ru_isrss      {}".format(lol[i][20]))
        #print("   ru_minflt     {}".format(lol[i][21]))
        #print("   ru_majflt     {}".format(lol[i][22]))
        #print("   ru_nswap      {}".format(lol[i][23]))
        #print("   ru_inblock        {}".format(lol[i][24]))
        #print("   ru_oublock        {}".format(lol[i][25]))
        #print("   ru_msgsnd     {}".format(lol[i][26]))
        #print("   ru_msgrcv     {}".format(lol[i][27]))
        #print("   ru_nsignals       {}".format(lol[i][28]))
        #print("   ru_nvcsw      {}".format(lol[i][29]))
        #print("   ru_nivcsw     {}".format(lol[i][30]))
        #print("project      {}".format(lol[i][31]))
        #print("department       {}".format(lol[i][32]))
        #print("granted_pe       {}".format(lol[i][33]))
        #print("slots        {}".format(lol[i][34]))
        #print("task_number      {}".format(lol[i][35]))
        # print("cpu      {}".format(lol[i][36]))  # total cpu time usage in seconds
        # print("mem      {}".format(lol[i][37]))  # integral memory usage in Gbytes cpu seconds ?!
        # print("io       {}".format(lol[i][38]))  # amount of data transferred in i/o ops
        #print("category     {}".format(lol[i][39]))
        # print("iow      {}".format(lol[i][40]))  # io wait time in seconds, always 0, yeah!
        #print("pe_taskid        {}".format(lol[i][41]))
        # print("maxvmem      {}".format(lol[i][42]))  # in bytes
        #print("arid     {}".format(lol[i][43]))
        #print("ar_submission_time       {}".format(lol[i][44]))
        # print("==============================================================")
        # print(lol[i])
        #
        print("job_number   : {}".format(lol[i][5]))
        print("  start_time : {}".format(datetime.datetime.fromtimestamp(
            int(lol[i][9])).strftime('%Y%m%d %H:%M')))
        print("  ru_wallclk : {}".format(float(lol[i][13]) / 3600))
        print("    ru_utime : {}".format(float(lol[i][14]) / 3600))
        print("    ru_stime : {}".format(float(lol[i][15]) / 3600))
        print("         cpu : {}".format(float(lol[i][36]) / 3600))
        print("    end_time : {}".format(datetime.datetime.fromtimestamp(
            int(lol[i][10])).strftime('%Y%m%d %H:%M')))

"""
    Store & Add
"""

#utime, stime, cpu, maxrss, inblock, oublock, mem, io, iow = 0, 0, 0, 0, 0, 0, 0, 0, 0
utime, stime, cpu = 0, 0, 0

for i in range(len(lol)):
    utime += float(lol[i][14])
    stime += float(lol[i][15])
    #maxrss += float(lol[i][16])
    #inblock += float(lol[i][24])
    #oublock += float(lol[i][25])
    cpu += float(lol[i][36])
    #mem += float(lol[i][37])
    #io += float(lol[i][38])
    #iow += (float(lol[i][13]) - float(lol[i][14]))

# y'a un truc crétin sur le cumul de ces valeurs :
# en job para, ru_wallclock est petit vs ru_utime => iow négatif
# mem, c'est des Gbytes / cpu / secondes, non-sens cumulé
# in/oublock, c'est un nb d'accès, pas des bytes
# maxrss, c'est un peakmem, non-sens cumulé
# io, on a pas l'unité !
# iow, sous linux, toujours 0, donc recalcul => ~stime ?

"""
    Print out results
"""

if not args.c:
    print("using:", ifile)
    if args.u:
        print("user: {}".format(user))
    if args.g:
        print("group: {}".format(group))
    if args.P:
        print("project: {}".format(projet))
    if args.q:
        print("on queue(s) containing: {}".format(queue))
    if args.b and args.e:
        print("Period from {} to {}:".format(debut, fin))
    print("jobs: {}".format(int(len(lol))))
    #print(" utime = {} heures".format(int(utime / 3600)))
    print(" cpu = {} heures".format(int(cpu / 3600)))
    if args.s:
        print("with:")
        print("utime = {} heures".format(int(utime / 3600)))
        print("stime = {} heures".format(int(stime / 3600)))
        #print("maxrss = {} Gbytes".format(int(maxrss / 1048576)))
        #print("inblock = {} k".format(int(inblock / 1000)))
        #print("oublock = {} k".format(int(oublock / 1000)))
        #print("mem = {} Gbytes".format(int(mem / 1048576)))
        #print("io = {} Mbytes".format(int(io / 1024)))
        #print("iow = {} heures".format(int(iow / 3600)))
        #print("maxvmem = {} Gbytes".format(int(maxvmem / 1048576)))

    # a little air, if into a 'for' shell loop
    print("")

elif args.c:
    # print("{};".format(user),"{};".format(group),"{};".format(queue),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)))
    # if user and group and queue and project
    if args.u and args.g and args.q and args.P:
        if args.s:
            if args.d:
                # print("user;group;queue;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;group;queue;projet;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(group),"{};".format(queue),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(group),
                  "{};".format(queue),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;group;queue;projet;jobs;cpu")
            print("{};".format(user),
                  "{};".format(group),
                  "{};".format(queue),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or user and queue and project and NO group
    elif args.u and args.q and args.P and not args.g:
        if args.s:
            if args.d:
                # print("user;queue;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;queue;projet;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(queue),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(queue),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;queue;projet;jobs;cpu")
            print("{};".format(user), "{};".format(queue), "{};".format(
                projet), "{};".format(int(len(lol))), "{};".format(int(cpu / 3600)))
# or user and group and project and NO queue
    elif args.u and args.g and args.P and not args.q:
        if args.s:
            if args.d:
                # print("user;group;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;group;projet;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(group),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(group),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;group;projet;jobs;cpu")
            print("{};".format(user), "{};".format(group), "{};".format(
                projet), "{};".format(int(len(lol))), "{};".format(int(cpu / 3600)))
# or user and group and queue and NO project
    elif args.u and args.g and args.q and not args.P:
        if args.s:
            if args.d:
                # print("user;group;queue;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;group;queue;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(group),"{};".format(queue),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(group),
                  "{};".format(queue),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;group;queue;jobs;cpu")
            print("{};".format(user), "{};".format(group), "{};".format(
                queue), "{};".format(int(len(lol))), "{};".format(int(cpu / 3600)))
# or group and queue and project (CSSI typical) and NO user
    elif args.g and args.q and args.P and not args.u:
        if args.s:
            if args.d:
                # print("group;queue;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print(
                    "group;queue;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
            # print("{};".format(group),"{};".format(queue),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(group),
                  "{};".format(queue),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("group;queue;projet;jobs;cpu")
            print("{};".format(group), "{};".format(queue), "{};".format(
                projet), "{};".format(int(len(lol))), "{};".format(int(cpu / 3600)))
# or user and group and NO queue and NO project
    elif args.u and args.g and not args.q and not args.P:
        if args.s:
            if args.d:
                # print("user;group;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;group;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(group),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(group),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;group;jobs;cpu")
            print("{};".format(user), "{};".format(group), "{};".format(
                int(len(lol))), "{};".format(int(cpu / 3600)))
# or user and project and NO group and NO queue
    elif args.u and args.P and not args.g and not args.q:
        if args.s:
            if args.d:
                # print("user;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;projet;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;projet;jobs;cpu")
            print("{};".format(user), "{};".format(projet), "{};".format(
                int(len(lol))), "{};".format(int(cpu / 3600)))
# or user and queue and NO group and NO project
    elif args.u and args.q and not args.g and not args.P:
        if args.s:
            if args.d:
                # print("user;queue;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;queue;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(queue),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(queue),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;queue;jobs;cpu")
            print("{};".format(user), "{};".format(queue), "{};".format(
                int(len(lol))), "{};".format(int(cpu / 3600)))
# or group and queue and NO user and NO project
    elif args.g and args.q and not args.u and not args.P:
        if args.s:
            if args.d:
                # print("group;queue;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("group;queue;jobs;cpu;utime;stime")
            # print("{};".format(group),"{};".format(queue),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(group),
                  "{};".format(queue),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("group;queue;jobs;cpu")
            print("{};".format(group), "{};".format(queue), "{};".format(
                int(len(lol))), "{};".format(int(cpu / 3600)))
# or group and project and NO user and NO queue
    elif args.g and args.P and not args.u and not args.q:
        if args.s:
            if args.d:
                # print("group;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("group;projet;jobs;cpu;utime;stime")
            # print("{};".format(group),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(group),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("group;projet;jobs;cpu")
            print("{};".format(group),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or queue and project and NO user and NO group
    elif args.q and args.P and not args.u and not args.g:
        if args.s:
            if args.d:
                # print("queue;projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("queue;projet;jobs;cpu;utime;stime")
            # print("{};".format(queue),"{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(queue),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("queue;projet;jobs;cpu")
            print("{};".format(queue),
                  "{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or only user
    elif args.u and not args.g and not args.q and not args.P:
        if args.s:
            if args.d:
                # print("user;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("user;jobs;cpu;utime;stime")
            # print("{};".format(user),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(user),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("user;jobs;cpu")
            print("{};".format(user),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or only group
    elif args.g and not args.u and not args.q and not args.P:
        if args.s:
            if args.d:
                # print("group;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("group;jobs;cpu;utime;stime")
            # print("{};".format(group),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(group),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("group;jobs;cpu")
            print("{};".format(group),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or only queue
    elif args.q and not args.u and not args.g and not args.P:
        if args.s:
            if args.d:
                # print("queue;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("queue;jobs;cpu;utime;stime")
            # print("{};".format(queue),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(queue),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("queue;jobs;cpu")
            print("{};".format(queue),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or only project
    elif args.P and not args.u and not args.g and not args.q:
        if args.s:
            if args.d:
                # print("projet;jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("projet;jobs;cpu;utime;stime")
            # print("{};".format(projet),"{};".format(int(len(lol))),"{};".format(int(cpu/3600)),"{};".format(int(utime/3600)),"{};".format(int(stime/3600)),"{};".format(int(maxrss/1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem/1024)),"{};".format(int(io/1024)),"{};".format(int(iow/3600)))
            print("{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("projet;jobs;cpu")
            print("{};".format(projet),
                  "{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)))
# or none (shit happens)
    elif not args.u and not args.g and not args.q and not args.P:
        if args.s:
            if args.d:
                # print("jobs;cpu;utime;stime;maxrss;inblock;oublock;mem;io;iow")
                print("jobs;cpu;utime;stime")
            #print("{};".format(int(len(lol))),"{};".format(int(cpu / 3600)),"{};".format(int(utime / 3600)),"{};".format(int(stime / 3600)),"{};".format(int(maxrss / 1048576)),"{};".format(int(inblock)),"{};".format(int(oublock)),"{};".format(int(mem / 1024)),"{};".format(int(io / 1024)),"{};".format(int(iow / 3600)))
            print("{};".format(int(len(lol))),
                  "{};".format(int(cpu / 3600)),
                  "{};".format(int(utime / 3600)),
                  "{};".format(int(stime / 3600)))
        else:
            if args.d:
                print("jobs;cpu")
            print("{};".format(int(len(lol))), "{};".format(int(cpu / 3600)))


"""
Successfull TODO/FIXME->DONE documented:
    * translate to python3: ~OK
    File "sge/sge-acct/parse_acct2.py", line 76, in <module>
        for var in fichier:
    File "/usr/lib/python3.4/codecs.py", line 313, in decode
        (result, consumed) = self._buffer_decode(data, self.errors, final)
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 4261: invalid continuation byte
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 4551: ordinal not in range(128)
    => encoding choice must be done at opening AND match source file:
    cmd file (ascii, latin1, latin9)
    #fichier = open(ifile, "r", encoding='ascii') # not always a win
    match, try latin1 or latin9
    #fichier = open(ifile, "r") # python2

    * there's a problem with selection range, results are minored against
    legacy qacct
    - qacct -e : The  latest  *start time* for jobs to be summarized (so,
    do not filter on 'lol[i][10](end_time)' column, but on
    'lol[i][9](start_time)' column
    - same, strict test (> and <), for automated inclusion of %H%M

    * filter directly at file reading, otherwise, it's too long and too
    RAM greedy (-> ram consumption reduced to 0%)

    * filter by date range first, then filter the rest

    * accounting file by default (os.path.isfile("/path/file"))

    * discriminative filter (if user AND group AND queue AND project OR if user AND project...)

    * add some statistics, ondemand

    * add csv output, ondemand, header with debug mode
"""
