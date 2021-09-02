from app.utils import splitDict
from app.service.charts import Charts

class userCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)
    
    def charts(self, form):
        charts = list()
        recall = dict()
        error = False

        # Variables input
        date = self.pickDate(form, recall)[0]
        user = form.users.data
        multiGroup = self.pickGroup(form)
        groupName = form.groups.data
        recall["Utilisateur"] = user
        recall["Groupe"] = groupName

        #if Catch erreurs then stop
        sql = """
            SELECT COUNT(job_.id_job_) AS nb_job
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                {group}
                {date}
            GROUP BY users.login;
            """
        
        jobsTotal = self.e.fetch(command=sql.format(  date=date,
                                                    group = multiGroup,
                                                    user=user))
        if(super().detectError(jobsTotal)):
            return charts, recall, True


        #User, groupe

        sql = """
           SELECT COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu)/3600 AS sum_cpu
            FROM job_, groupes, users
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND users.login != '{user}' 
            GROUP BY groupes.id_groupe ; 
            """
            
        nbhoursGroup = self.e.fetch(command=sql.format( date=date,
                                                    groupName = groupName,
                                                    user=user))
        print("nbhoursGroup")
        sql = """
            SELECT COUNT(job_.id_job_) AS nb_job {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                {test}
                {group}
                {date}
            GROUP BY users.login;
            """

        jobSuccessHours = self.e.fetch(command=sql.format(  select=', SUM(job_.cpu)/3600 AS sum_cpu',
                                                            date=date,
                                                            test = 'AND (job_.failed = 0 OR job_.exit_status = 0)',
                                                            group = multiGroup,
                                                            user=user))

        jobsFailed = self.e.fetch(command=sql.format(   select = '',
                                                        date=date,
                                                        test = 'AND job_.failed != 0 AND job_.exit_status != 0',
                                                        group = multiGroup,
                                                        user=user))

        jobsSuccess = super().nameDict("Jobs réussi", super().isNullDict("nb_job", jobSuccessHours))
        jobsFailed = super().nameDict("Jobs mauvais", super().isNullDict("nb_job", jobsFailed))

        hoursGroup = super().nameDict("Nombre d'heures du groupe", super().isNullDict("sum_cpu",nbhoursGroup))
        jobsGroup = super().nameDict("Nombre de jobs du groupe", super().isNullDict("nb_job",nbhoursGroup))
        hoursUser = super().nameDict("Nombre d'heures de l'utilisateur", super().isNullDict("sum_cpu", jobSuccessHours))
        jobsUser = super().nameDict("Nombre de jobs de l'utilisateur", super().isNullDict("nb_job", jobSuccessHours))

        jobsSuccessFailed = (jobsSuccess, jobsFailed)
        nbHoursGroupUser = (hoursGroup, hoursUser)
        nbJobsGroupUser = (jobsGroup, jobsUser)

        print("jobsSuccessFailed")

        #Exec time
        
        sql = """
            SELECT MAX(job_.ru_wallclock)/3600 AS max, AVG(job_.ru_wallclock)/3600 AS avg, MIN(job_.ru_wallclock)/3600 AS min 
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {group}
                {date}
            GROUP BY users.login ;
            """

        execTimeMAM = self.e.fetch(command=sql.format(  date=date,
                                                        group = multiGroup,
                                                        user=user))

        execTimeMAM = splitDict(execTimeMAM)
        print("execTimeMAM")
        
        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
                AND job_.ru_wallclock {test} (
                    SELECT AVG(job_.ru_wallclock)
                    FROM job_, users
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                        {group}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """      

        execTimeSupAvg = self.e.fetch(command=sql.format(   select='sup_avg',
                                                            date=date, 
                                                            test = ">",
                                                            group = multiGroup,
                                                            user=user))
        
        execTimeInfAvg = self.e.fetch(command=sql.format(   select='inf_avg',
                                                            date=date, 
                                                            test = "<",
                                                            group = multiGroup,
                                                            user=user))

        execTimeSupAvg = super().nameDict("Temps d'éxecution moyen supérieur", super().isNullDict("sup_avg", execTimeSupAvg))
        execTimeInfAvg = super().nameDict("Temps d'éxecution moyen inférieur", super().isNullDict("inf_avg", execTimeInfAvg))

        execTimeComparaison = (execTimeSupAvg, execTimeInfAvg)
        print("execTimeComparaison")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.ru_wallclock {test}
            GROUP BY users.login ;
            """

        execTime1 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " < 86400 ",
                                                        user=user))

        execTime2 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 86400 AND job_.ru_wallclock < 604800 ",
                                                        user=user))

        execTime3 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 604800 AND job_.ru_wallclock < 18144000 ",
                                                        user=user))
        
        execTime4 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 18144000 ",
                                                        user=user))

        execTime1 = super().nameDict("< 24", super().isNullDict("exectime", execTime1))
        execTime2 = super().nameDict("[24; 168]", super().isNullDict("exectime", execTime2))
        execTime3 = super().nameDict("[168; 5 040]", super().isNullDict("exectime", execTime3))
        execTime4 = super().nameDict("> 5 040", super().isNullDict("exectime", execTime4))

        execTime = (execTime1, execTime2, execTime3, execTime4) #Posibilité que des valeurs disparaissent car value = 0.
        print("execTime")

        #Memory usage

        sql = """
            SELECT MAX(job_.maxvmem)/ 1024 / 1024 / 1024 AS max, AVG(job_.maxvmem)/ 1024 / 1024 / 1024 AS avg, MIN(job_.maxvmem)/ 1024 / 1024 / 1024 AS min
            FROM job_, users 
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY users.login ;
            """

        memUseMAM = self.e.fetch(command=sql.format(  date=date,
                                                        user=user))
        memUseMAM = splitDict(memUseMAM)
        print("memUseMAM")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.maxvmem {test} (
                    SELECT AVG(job_.maxvmem)
                    FROM job_, users
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """
        
        memUseSupAvg = self.e.fetch(command=sql.format( select='jobs_sup_avg',
                                                        date=date, 
                                                        test = ">",
                                                        user=user))
        
        memUseInfAvg = self.e.fetch(command=sql.format( select='jobs_inf_avg',
                                                        date=date, 
                                                        test = "<",
                                                        user=user))

        memUseSupAvg = super().nameDict("Utilisation de la mémoire moyenne supérieur", super().isNullDict("jobs_sup_avg", memUseSupAvg))
        memUseInfAvg = super().nameDict("Utilisation de la mémoire moyenne inférieur", super().isNullDict("jobs_inf_avg", memUseInfAvg))

        memUseComparaison = (memUseSupAvg, memUseInfAvg)
        print("memUseComparaison")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.maxvmem {test}
            GROUP BY users.login ;
            """

        mUsage1 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " < 1073741824 ",
                                                    user=user))

        mUsage2 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 1073741824 AND job_.maxvmem < 4294967296 ",
                                                    user=user))

        mUsage3 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 4294967296 AND job_.maxvmem < 858993459 ",
                                                    user=user))

        mUsage4 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 8589934592 AND job_.maxvmem < 17179869184 ",
                                                    user=user))

        mUsage5 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 17179869184 AND job_.maxvmem < 34359738368 ",
                                                    user=user))

        mUsage6 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 34359738368 AND job_.maxvmem < 68719476736 ",
                                                    user=user))

        mUsage7 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 68719476736 AND job_.maxvmem < 137438953472 ",
                                                    user=user))

        mUsage8 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 137438953472 ",
                                                    user=user))

        mUsage1 = super().nameDict("< 1", super().isNullDict("musage", mUsage1))
        mUsage2 = super().nameDict("[1; 4]", super().isNullDict("musage", mUsage2))
        mUsage3 = super().nameDict("[4; 8]", super().isNullDict("musage", mUsage3))
        mUsage4 = super().nameDict("[8; 16]", super().isNullDict("musage", mUsage4))
        mUsage5 = super().nameDict("[16; 32]", super().isNullDict("musage", mUsage5))
        mUsage6 = super().nameDict("[32; 64]", super().isNullDict("musage", mUsage6))
        mUsage7 = super().nameDict("[64; 128]", super().isNullDict("musage", mUsage7))
        mUsage8 = super().nameDict("> 128", super().isNullDict("musage", mUsage8))

        memUsage = (mUsage1, mUsage2, mUsage3, mUsage4, mUsage5, mUsage6, mUsage7, mUsage8) #Posibilité que des valeurs disparaissent car value = 0.
        print("memUsage")

        #slots usage

        sql = """
            SELECT MAX(job_.slots) AS max_slots, AVG(job_.slots) AS avg_slots, MIN(job_.slots) AS min_slots
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY users.login ;
            """

        slotsPerJobsMAM = self.e.fetch(command=sql.format(  date=date,
                                                            user=user))
        slotsPerJobsMAM = splitDict(slotsPerJobsMAM)
        print("slotsPerJobsMAM")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
                -- avg donné par requête imbriquée
                AND job_.slots  {test} (
                    SELECT AVG(job_.slots)
                    FROM job_, users, groupes
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                        {group}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """

        slotsPerJobsSupAvg = self.e.fetch(command=sql.format(   select='jobs_sup_avg',
                                                                date=date, 
                                                                test = ">",
                                                                group = multiGroup,
                                                                user=user))
        
        slotsPerJobsInfAvg = self.e.fetch(command=sql.format(   select='jobs_inf_avg',
                                                                date=date, 
                                                                test = "<",
                                                                group = multiGroup,
                                                                user=user))
        
        slotsPerJobsSupAvg = super().nameDict("Slots par job moyen supérieur", super().isNullDict("jobs_sup_avg", slotsPerJobsSupAvg))
        slotsPerJobsInfAvg = super().nameDict("Slots par job moyen inférieur", super().isNullDict("jobs_inf_avg", slotsPerJobsInfAvg))
        
        slotsPerJobsComparaison = (slotsPerJobsSupAvg, slotsPerJobsInfAvg)
        print("slotsPerJobsComparaison")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
                AND job_.slots {test}
            GROUP BY users.login ;
            """

        slots1 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " = 1 ",
                                                    group = multiGroup,
                                                    user=user))

        slots2 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 1 AND job_.slots <= 4 ",
                                                    group = multiGroup,
                                                    user=user))

        slots3 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 5 AND job_.slots <= 8 ",
                                                    group = multiGroup,
                                                    user=user))

        slots4 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 9 AND job_.slots <= 16 ",
                                                    group = multiGroup,
                                                    user=user))

        slots5 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 17 AND job_.slots <= 32 ",
                                                    group = multiGroup,
                                                    user=user))

        slots6 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 33 AND job_.slots <= 64 ",
                                                    group = multiGroup,
                                                    user=user))

        slots7 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 65 AND job_.slots <= 128 ",
                                                    group = multiGroup,
                                                    user=user))

        slots8 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 128 ",
                                                    group = multiGroup,
                                                    user=user))

        slots1 = super().nameDict("= 1", super().isNullDict("slots", slots1))
        slots2 = super().nameDict("[1; 4]", super().isNullDict("slots", slots2))
        slots3 = super().nameDict("[5; 8]", super().isNullDict("slots", slots3))
        slots4 = super().nameDict("[9; 16]", super().isNullDict("slots", slots4))
        slots5 = super().nameDict("[17; 32]", super().isNullDict("slots", slots5))
        slots6 = super().nameDict("[33; 64]", super().isNullDict("slots", slots6))
        slots7 = super().nameDict("[65; 128]", super().isNullDict("slots", slots7))
        slots8 = super().nameDict("> 128", super().isNullDict("slots", slots8))

        slotsPerJob = (slots1, slots2, slots3, slots4, slots5, slots6, slots7, slots8)                                                        
        print("slotsPerJob")

        #Temps d'attente
        
        sql = """
            SELECT MAX(job_.start_time - job_.submit_time)/3600 as max, AVG(job_.start_time - job_.submit_time)/3600 as avg, -- MIN(job_.start_time - job_.submit_time)/3600 as min
            CASE WHEN MIN(job_.start_time - job_.submit_time) < 0 THEN 0
            ELSE MIN(job_.start_time - job_.submit_time)
            END 
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date} 
                {group}
            GROUP BY users.login ;
            """
        
        waitingTimeMAM = self.e.fetch(command=sql.format(   date=date,
                                                            group = multiGroup,
                                                            user=user))
        waitingTimeMAM = splitDict(waitingTimeMAM)
        print("waitingTimeMAM")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
                -- avg donné par requête imbriquée
                AND (job_.start_time - job_.submit_time) > (
                    SELECT AVG(job_.start_time - job_.submit_time)
                    FROM job_, users, groupes
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                        {group}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """

        waitingTimeSupAvg = self.e.fetch(command=sql.format(    select='wt_sup_avg',
                                                                date=date, 
                                                                test = ">",
                                                                group = multiGroup,
                                                                user=user))
        
        waitingTimeInfAvg = self.e.fetch(command=sql.format(    select='wt_inf_avg',
                                                                date=date, 
                                                                test = "<",
                                                                group = multiGroup,
                                                                user=user))

        waitingTimeSupAvg = super().nameDict("Slots par job moyen supérieur", super().isNullDict("wt_sup_avg", waitingTimeSupAvg))
        waitingTimeInfAvg = super().nameDict("Slots par job moyen inférieur", super().isNullDict("wt_inf_avg", waitingTimeInfAvg))

        waitingTimeComparaison = (waitingTimeSupAvg, waitingTimeInfAvg)
        print("waitingTimeComparaison")

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
                AND (job_.start_time - job_.submit_time) {test}
            GROUP BY users.login;
            """

        waitingTime1 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "< 3600",
                                                            group = multiGroup,
                                                            user=user))

        waitingTime2 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 3600 AND (job_.start_time - job_.submit_time) < 21600",
                                                            group = multiGroup,
                                                            user=user))

        waitingTime3 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 21600 AND (job_.start_time - job_.submit_time) < 43200",
                                                            group = multiGroup,
                                                            user=user))

        waitingTime4 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 43200 AND (job_.start_time - job_.submit_time) < 86400",
                                                            group = multiGroup,
                                                            user=user))

        waitingTime5 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 86400",
                                                            group = multiGroup,
                                                            user=user))

        waitingTime1 = super().nameDict("< 1", super().isNullDict("waitingtime", waitingTime1))
        waitingTime2 = super().nameDict("[1; 6]", super().isNullDict("waitingtime", waitingTime2))
        waitingTime3 = super().nameDict("[6; 12]", super().isNullDict("waitingtime", waitingTime3))
        waitingTime4 = super().nameDict("[12; 24]", super().isNullDict("waitingtime", waitingTime4))
        waitingTime5 = super().nameDict("> 24", super().isNullDict("waitingtime", waitingTime5))

        waitingTime = (waitingTime1, waitingTime2, waitingTime3, waitingTime4, waitingTime5) 
        print("waitingTime")

        #Top ten
        
        sql = """
            SELECT queues.queue_name, {select} AS sum_
            FROM users, queues, job_, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND job_.id_queue = queues.id_queue
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
            GROUP BY queues.queue_name
            ORDER BY sum_ DESC LIMIT 10 ;
        """

        topTenUsedQueues = self.e.fetch(command=sql.format(     date=date, 
                                                                select = 'sum(job_.cpu)/3600',
                                                                group = multiGroup,
                                                                user=user))

        topTenUsedNodes = self.e.fetch(command=sql.format(      date=date, 
                                                                select = 'count(job_.id_job_)',
                                                                group = multiGroup,
                                                                user=user))
        topTenUsedQueues = super().multiDict(topTenUsedQueues, ['queue_name', 'sum_'])
        topTenUsedNodes = super().multiDict(topTenUsedNodes, ['queue_name', 'sum_'])
        print("topTenUsedNodes")

        sql = """
            SELECT hosts.hostname, {select} AS sum_
            FROM users, hosts, job_, groupes
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND job_.id_host = hosts.id_host
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {group}
            GROUP BY hosts.hostname
            ORDER BY sum_ DESC LIMIT 10 ;
            """
        
        topTenHostnameHours = self.e.fetch(command=sql.format(      date=date, 
                                                                    select = 'sum(job_.cpu)/3600',
                                                                    group = multiGroup,
                                                                    user=user))

        topTenHostnameNbJobs = self.e.fetch(command=sql.format(     date=date, 
                                                                    select = 'count(job_.id_job_)',
                                                                    group = multiGroup,
                                                                    user=user))
        
        topTenHostnameHours = super().multiDict(topTenHostnameHours, ['hostname', 'sum_'])
        topTenHostnameNbJobs = super().multiDict(topTenHostnameNbJobs, ['hostname', 'sum_'])
        print("topTenHostnameHours")

        charts.append(  {"id": "chart1", "name" : "Information utilisateur/groupe", "charts" : (
                            {"id":"jobsSuccessFailed", "type": "PieChart", "values" : jobsSuccessFailed, "title" : "Taux réussite"},
                            {"id":"nbJobsGroupUser", "type": "PieChart", "values" : nbJobsGroupUser, "title" : "Nombre de jobs / Groupe"},
                            {"id":"nbHoursGroupUser", "type": "PieChart", "values" : nbHoursGroupUser, "title" : "Nombre d'heures / Groupe"}
                        )})

        charts.append(  {"id": "chart2", "name" : "Temps d'éxecution", "charts": (
                            {"id":"execTimeMAM", "type": "BarChart", "values" : execTimeMAM, "title" : "Temps d'exécution (heures)"},
                            {"id":"execTimeComparaison", "type": "PieChart", "values" : execTimeComparaison, "title" : "Temps d'exécution moyen (heures)"},
                            {"id":"execTime", "type": "BarChart", "values" : execTime, "title" : "Temps d'exécution (heures)"}
                        )})

        charts.append(  {"id": "chart3", "name" : "Utilisation de la mémoire", "charts": (
                            {"id":"memUseMAM", "type": "BarChart", "values" : memUseMAM, "title" : "Utilisation de la mémoire (GiB)"},
                            {"id":"memUseComparaison", "type": "PieChart", "values" : memUseComparaison, "title" : "Utilisation de la mémoire moyenne (GiB)"},
                            {"id":"memUsage", "type": "BarChart", "values" : memUsage, "title" : "Utilisation de la mémoire (GiB)"}
                        )})

        charts.append(  {"id": "chart4", "name" : "Slots par jobs", "charts": (
                            {"id":"slotsPerJobsMAM", "type": "BarChart", "values" : slotsPerJobsMAM, "title" : "Slots par job"},
                            {"id":"slotsPerJobsComparaison", "type": "PieChart", "values" : slotsPerJobsComparaison, "title" : "Slots par job moyenne"},
                            {"id":"slotsPerJob", "type": "BarChart", "values" : slotsPerJob, "title" : "Slots par job"}
                        )})

        charts.append(  {"id": "chart5", "name" : "Temps d'attente", "charts": (
                            {"id":"waitingTimeMAM", "type": "BarChart", "values" : waitingTimeMAM, "title" : "Temps d'attente (heures)"},
                            {"id":"waitingTimeComparaison", "type": "PieChart", "values" : waitingTimeComparaison, "title" : "Temps d'attente moyen (heures)"},
                            {"id":"waitingTime", "type": "BarChart", "values" : waitingTime, "title" : "Temps d'attente (heures)"}
                        )})
        
        charts.append(  {"id": "chart6", "name" : "Top 10", "charts": (
                            {"id":"topTenUsedQueues", "type": "BarChart", "values" : topTenUsedQueues, "title" : "Top 10 des queues utilisées (heures)"},
                            {"id":"topTenUsedNodes", "type": "BarChart", "values" : topTenUsedNodes, "title" : "Top 10 des nodes utilisés (nombre de jobs)"},
                            {"id":"topTenHostnameHours", "type": "BarChart", "values" : topTenHostnameHours, "title" : "Top 10 Hostnames (heures)"},
                            {"id":"topTenHostnameNbJobs", "type": "BarChart", "values" : topTenHostnameNbJobs, "title" : "Top 10 Hostnames (nombre de jobs)"}
                        )})
  
        return charts, recall, error
    
