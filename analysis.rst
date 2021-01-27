===============
Pseudo-Analysis
===============

:date: 2020-02-29
:modified: 2021-01-26
:status: draft
:licence: SPDX-License-Identifier: BSD-2-Clause


Data source is 'accounting' file, from GridEngine scheduler. ASCII text, ':' as separator.

The file format is describe in ``SGE_accounting_file_format.rst``.

Job:
====

One line from accouting file identify a job. Each ``[int element]`` indicate the rank in the line, starting from 0 (as they may have multiple names in documentation and our analysis).

A job is a work submitted by a User[3] to a Queue[0], at Submission[8] date. Runned from Start[9] date to End[10] date on Hostname[1]. Identified by job_ID[5] in the scheduler.

Dates:
======

submission_time[8]
------------------

When the user (owner[3]) submitted the job. epoch type of field.

start_time[9]
-------------

When the job is actually submitted to the node (hostname[1]). epoch type of field.

end_time[10]
------------

When the job is actually finished on the node (or stopped by scheduler). epoch type of field.

Theses 3 dates together may form a unique key.

General fields:
===============

owner[3]
--------

System user (as in login), submitter of a job. Will appear and disappear over the years. Can be in multiples groups over the years.

queue_name[0]
-------------

Groupe of nodes (in the scheduler configuration) to which the job is submitted. Identified by 'queue_name, line[0]'. Will appear and disappear over the years. May not contend the same nodes over the years.

hostname[1]
-----------

Hostname[1] is the node (or master_node, if multiples nodes) which run the job. Can be in multiples Queues over the years. Will appear and disappear over the years.

project[31]
-----------

The project identifier, if used (default to ``NONE``). May be used as a filter's key.

slots[34]
---------

Number of slots resources requested. One slot usually correspond to one single core of a CPU (default GridEngine configuration).


Results:
========

Once the job has runned, it's scheduling results are stored in accounting file. Fields of interest:

failed[11]
----------

An indicator if the run was successfull, from GridEngine point of view. See ``man 5 sge_status`` for a list.

exit_status[12]
---------------

Exit status of the job script, from GridEngine point of view.

ru_wallclock[13]
----------------

Overall Resources Utilization (``ru_``), correspond to ``end_time`` minus ``start_time`` (seconds).

ru_utime[14]
------------

Total amount of time spent in user mode (seconds).

ru_stime[15]
------------

Total amount of time spent in system/kernel mode (seconds)

ru_maxrss[16]
-------------

Maximum resident set size used (kilobytes). ``This is the resident set size of the largest child, not the maximum resident set size of the process tree``.

cpu[36]
-------

Total cpu time usage (seconds). May differ from ru_wallclock, ru_stime and ru_stime on multi slots jobs (multicores/multihosts).

mem[37]
-------

Integral memory usage (GB seconds ?!)

io[38]
------

The amount of data transferred in input/output operations in GB (if available, otherwise 0). On Linux, it includes i/o via cache, and may not reflect data actually written to filing system.

maxvmem[42]
-----------

The maximum vmem size in bytes used by the job (on the master node, if multiples nodes).

Users results:
==============

Most requested analysis/statistics are ''sum of cpu'', with detailed ''sum of utime'', ''sum of stime'' for a user, a group or a project.

See README.md for more new requested statistics.

