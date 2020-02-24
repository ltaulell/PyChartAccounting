# SGE accounting file format

## extract examples

  * v6.2u5 (Sun Grid Engine)


    # Version: 6.2u5
    # 
    # DO NOT MODIFY THIS FILE MANUALLY!
    # 
    r410lin24ibA:r410lin1.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:2:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-q r410lin24ibA -pe r410_128 128:0.000000:NONE:0.000000:0:0
    r410lin24ibA:r410lin24.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:2:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-q r410lin24ibA -pe r410_128 128:0.000000:NONE:0.000000:0:0
    r410lin24ibA:r410lin21.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:4:sge:0:1265881759:1265881771:1265881813:12:1:42:4.939242:3.530455:0.000000:0:0:0:0:237083:1538:0:0.000000:0:0:0:0:142603:7369:NONE:defaultdepartment:r410_128:128:0:8.552755:0.387701:0.058077:-q r410lin24ibA -pe r410_128 128:0.000000:NONE:19155009536.000000:0:0
    r410lin24ibA:r410lin4.ens-lyon.fr:umpa:gilquin:batchopenmpiintelrun:5:sge:0:1265881946:1265881950:1265881951:12:129:1:0.583911:0.679895:0.000000:0:0:0:0:27013:113:0:0.000000:0:0:0:0:44637:714:NONE:defaultdepartment:r410_128:16:0:1.263806:0.000000:0.000000:-q r410lin24ibA -pe r410_128 16:0.000000:NONE:0.000000:0:0


  * v8.1.9 (Son of Grid Engine)


    # Version: 8.1.9
    # 
    # DO NOT MODIFY THIS FILE MANUALLY!
    # 
    E5-2667v2h6deb128:c8220node216:psmn:ltaulell:envtestmpi:1:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-U STAFF -q E5-2667v2h6deb128 -pe mpi_debian 2:0.000000:NONE:0.000000:0:0
    E5-2667v2h6deb128:c8220node218:psmn:ltaulell:envtestmpi:1:sge:0:0:0:0:9:0:0:0.000000:0.000000:0.000000:0:0:0:0:0:0:0:0.000000:0:0:0:0:0:0:NONE:defaultdepartment:NONE:0:0:0.000000:0.000000:0.000000:-U STAFF -q E5-2667v2h6deb128 -pe mpi_debian 2:0.000000:NONE:0.000000:0:0
    E5-2667v2h6deb128:c8220node211:psmn:ltaulell:envtest:2:sge:0:1514123433:1514123473:1514123473:0:0:0:0.000000:0.004000:4044.000000:0:0:0:0:824:3:0:504.000000:16:0:0:0:106:12:NONE:defaultdepartment:NONE:1:0:0.004000:0.000000:0.000000:-U STAFF -q E5-2667v2h6deb128:0.000000:NONE:0.000000:0:0
    E5-2667v2h6deb128:c8220node213:psmn:ltaulell:envtest:3:sge:0:1514125071:1514125093:1514125792:100:152:699:0.000000:0.144000:3972.000000:0:0:0:0:709:3:0:504.000000:808:0:0:0:45215:27:NONE:defaultdepartment:NONE:1:0:21540.800000:2567485.677115:1.884987:-U STAFF -q E5-2667v2h6deb128:0.000000:NONE:128215048192.000000:0:0


## Description du contenu

4 lines of commentaries (headers), then, one line by job, with fields divided by ':', described below:

* queue_name (str)
* hostname (str)
* group (str)
* owner (login, str)
* job_name (str)
* job_number (int, not unique)  # $JOB_ID
* account (str, always 'sge')
* priority (int)
* submission_time (epoch)
* start_time (epoch)
* end_time (epoch)
* failed (int)
* exit_status (int)
  # See man getrusage (for all ru_ fields):
  * ru_wallclock (float)        # end_time minus start_time
  * ru_utime (float)            # total amount of time spent executing in user mode (seconds)
  * ru_stime (float)            # total amount of time spent executing in kernel mode (seconds)
  * ru_maxrss (float)           # maximum resident set size used (kilobytes)
  * ru_ixrss (float)
  * ru_ismrss (float)
  * ru_idrss (float)
  * ru_isrss (float)
  * ru_minflt (float)
  * ru_majflt (float)
  * ru_nswap (float)
  * ru_inblock (float)
  * ru_oublock (float)
  * ru_msgsnd (float)
  * ru_msgrcv (float)
  * ru_nsignals (float)
  * ru_nvcsw (float)
  * ru_nivcsw (float)
* project (str/NONE)
* department (str, always 'defaultdepartment')
* granted_pe (str/NONE)
* slots (int)
* task_number (int)
* cpu (float)                   # total cpu time usage (seconds)
* mem (float)                   # integral memory usage (Gbytes cpu seconds ?!)
* io (float)                    # amount of data transferred in i/o ops (in ?)
* category (str)                # SGE group + queue (-U -q)
* iow (float, always 0)         # io wait time (seconds), always 0 on linux
* pe_taskid (str/NONE)
* maxvmem (float)               # real peakmem, (bytes)
* arid (int)
* ar_submission_time (int)

`man accounting` et `parse_accounting.py` contiennent plus d'info sur les champs
du fichier d'accounting.



