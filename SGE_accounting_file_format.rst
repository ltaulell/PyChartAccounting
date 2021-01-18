==========================
SGE accounting file format
==========================

:date: 2020-02-21
:status: draft
:licence: SPDX-License-Identifier: BSD-2-Clause


extract examples
================

* v6.2u5 (Sun Grid Engine):

.. code-block:: bash

    # Version: 6.2u5
    # 
    # DO NOT MODIFY THIS FILE MANUALLY!
    # 
    r410lin24ibA:r410lin1.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:2:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-q r410lin24ibA -pe r410_128 128:0.000000:NONE:0.000000:0:0
    r410lin24ibA:r410lin24.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:2:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-q r410lin24ibA -pe r410_128 128:0.000000:NONE:0.000000:0:0
    r410lin24ibA:r410lin21.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:4:sge:0:1265881759:1265881771:1265881813:12:1:42:4.939242:3.530455:0.000000:0:0:0:0:237083:1538:0:0.000000:0:0:0:0:142603:7369:NONE:defaultdepartment:r410_128:128:0:8.552755:0.387701:0.058077:-q r410lin24ibA -pe r410_128 128:0.000000:NONE:19155009536.000000:0:0
    r410lin24ibA:r410lin4.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:5:sge:0:1265881946:1265881950:1265881951:12:129:1:0.583911:0.679895:0.000000:0:0:0:0:27013:113:0:0.000000:0:0:0:0:44637:714:NONE:defaultdepartment:r410_128:16:0:1.263806:0.000000:0.000000:-q r410lin24ibA -pe r410_128 16:0.000000:NONE:0.000000:0:0


* v8.1.9 (Son of Grid Engine)

.. code-block:: bash

    # Version: 8.1.9
    # 
    # DO NOT MODIFY THIS FILE MANUALLY!
    # 
    E5-2667v2h6deb128:c8220node216:psmn:ltaulell:envtestmpi:1:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-U STAFF -q E5-2667v2h6deb128 -pe mpi_debian 2:0.000000:NONE:0.000000:0:0
    E5-2667v2h6deb128:c8220node218:psmn:ltaulell:envtestmpi:1:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-U STAFF -q E5-2667v2h6deb128 -pe mpi_debian 2:0.000000:NONE:0.000000:0:0
    E5-2667v2h6deb128:c8220node211:psmn:gilquin:envtest:2:sge:0:1514123433:1514123473:1514123473:0:0:0:0.000000:0.004000:4044.000000:0:0:0:0:824:3:0:504.000000:16:0:0:0:106:12:NONE:defaultdepartment:NONE:1:0:0.004000:0.000000:0.000000:-U STAFF -q E5-2667v2h6deb128:0.000000:NONE:0.000000:0:0
    E5-2667v2h6deb128:c8220node213:psmn:gilquin:envtest:3:sge:0:1514125071:1514125093:1514125792:100:152:699:0.000000:0.144000:3972.000000:0:0:0:0:709:3:0:504.000000:808:0:0:0:45215:27:NONE:defaultdepartment:NONE:1:0:21540.800000:2567485.677115:1.884987:-U STAFF -q E5-2667v2h6deb128:0.000000:NONE:128215048192.000000:0:0


Description du contenu
======================

Headers: 4 lines of commentaries, with version (no change, except version, between 6.2u5 and 8.1.9)

One line per job, 45 columns (0 to 44), with fields divided by ':', described as follow:

* [0] queue_name (str)
* [1] hostname (str)
* [2] group (str)
* [3] owner (str)                   # $login
* [4] job_name (str)                # by user, not unique...
* [5] job_number (int, not unique)  # $JOB_ID
* *[6] account (str)*                 # default 'sge'
* *[7] priority (int)*
* [8] submission_time (epoch)
* [9] start_time (epoch)
* [10] end_time (epoch)
* [11] failed (int)
* [12] exit_status (int)
* [13] ru_wallclock (float)         # end_time minus start_time
* [14] ru_utime (float)             # total amount of time spent executing in user mode (seconds)
* [15] ru_stime (float)             # total amount of time spent executing in kernel mode (seconds)
* [16] ru_maxrss (float)            # maximum resident set size used (kilobytes, largest child)
* *[17] ru_ixrss (float)*             # unused on Linux, see man getrusage (for all ru_ fields)
* *[18] ru_ismrss (float)*            # unused on Linux, see man getrusage (for all ru_ fields)
* *[19] ru_idrss (float)*             # unused on Linux, see man getrusage (for all ru_ fields)
* *[20] ru_isrss (float)*             # unused on Linux, see man getrusage (for all ru_ fields)
* *[21] ru_minflt (float)*            # page reclaims (soft page faults) (nb)
* *[22] ru_majflt (float)*            # page faults (hard page faults) (nb)
* *[23] ru_nswap (float)*             # unused on Linux, see man getrusage (for all ru_ fields)
* *[24] ru_inblock (float)*           # block input operations (nb)
* *[25] ru_oublock (float)*           # block output operations (nb)
* *[26] ru_msgsnd (float)*            # unused on Linux, see man getrusage (for all ru_ fields)
* *[27] ru_msgrcv (float)*            # unused on Linux, see man getrusage (for all ru_ fields)
* *[28] ru_nsignals (float)*          # unused on Linux, see man getrusage (for all ru_ fields)
* *[29] ru_nvcsw (float)*             # voluntary context switches (nb)
* *[30] ru_nivcsw (float)*            # involuntary context switches (nb)
* [31] project (str)                # default 'NONE'
* *[32] department (str)*             # default 'defaultdepartment'
* *[33] granted_pe (str)*             # default 'NONE'
* [34] slots (int)
* *[35] task_number (int)*            # Array job index number
* [36] cpu (float)                  # total cpu time usage (seconds)
* [37] mem (float)                  # integral memory usage (GB seconds ?!)
* [38] io (float)                   # amount of data transferred in i/o ops (in GB)
* *[39] category (str)*               # SGE Userset, queue name, Parallel Environment, etc (-U -q -pe)
* *[40] iow (float)*                  # io wait time (seconds), default '0' on linux
* *[41] pe_taskid (str)*              # default 'NONE'
* [42] maxvmem (float)              # real peakmem, (bytes)
* *[43] arid (int)*
* *[44] ar_submission_time (int)*

``man 5 accounting`` contient (un peu) plus d'info sur les champs du fichier d'accounting.

``man 2 getrusage`` contient (un peu) plus d'info sur les champs ``ru_`` (resource usage).

Les champs en *italique* ont peu, voire pas du tout, d'intérêt.



default CSV header:

for reference and scripts.

.. code:: csv

    qname:host:group:owner:job_name:job_id:account:priority:submit_time:start:end:fail:exit_status:ru_wallclock:ru_utime:ru_stime:ru_maxrss:ru_ixrss:ru_ismrss:ru_idrss:ru_isrss:ru_minflt:ru_majflt:ru_nswap:ru_inblock:ru_oublock:ru_msgsnd:ru_msgrcv:ru_nsignals:ru_nvcsw:ru_nivcsw:project:department:granted_pe:slots:task_number:cpu:mem:io:category:iow:pe_taskid:maxvmem:arid:ar_submission_time

