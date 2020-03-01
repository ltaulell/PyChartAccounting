===============
Pseudo-Analysis
===============

:date: 2020-02-29
:modified: 2020-03-01
:status: draft
:licence: SPDX-License-Identifier: BSD-2-Clause

Dates
=====

Submission date
---------------

When the owner submitted the job. Identified by 'submission_time (epoch), line[8]'.

Start date
----------

When the job is actually submitted to the node. Identified by 'start_time (epoch), line[9]'.

End date
--------

When the job is actually finished by the node. Identified by 'end_time (epoch), line[10]'


Theses 3 dates together can form a unique key.

Job
===

Work submitted, by a User to a Queue, at Submission date. Identified by 'job_number, line[5]'. NOT UNIQUE.

User
====

Submitter of a job. Identified by 'owner, line[3]'. Will appear and disappear over the years. Can be in multiples groups over the years.

Queue
=====

Groupe of nodes to which the job is submitted. Identified by 'queue_name, line[0]'. Will appear and disappear over the years.


Node
====

Node (or master_node, if multiples nodes) which run the job. Can be in multiples Queues over the years. Will appear and disappear over the years.

