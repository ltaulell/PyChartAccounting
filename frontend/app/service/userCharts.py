from app.utils import combineDict
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
        if(Charts.detectError(jobsTotal)):
            return charts, recall, True


        #User, groupe

        sql = """
           SELECT COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu) AS sum_cpu
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

        jobSuccessHours = self.e.fetch(command=sql.format(  select=', SUM(job_.cpu) AS sum_cpu',
                                                            date=date,
                                                            test = 'AND (job_.failed = 0 OR job_.exit_status = 0)',
                                                            group = multiGroup,
                                                            user=user))

        jobsFailed = self.e.fetch(command=sql.format(   select = '',
                                                        date=date,
                                                        test = 'AND job_.failed != 0 AND job_.exit_status != 0',
                                                        group = multiGroup,
                                                        user=user))

        jobsSuccess = Charts.nameDict("Jobs réussi", Charts.isNullDict("nb_job", jobSuccessHours))
        jobsFailed = Charts.nameDict("Jobs mauvais", Charts.isNullDict("nb_job", jobsFailed))

        hoursGroup = Charts.nameDict("Nombre d'heures du groupe", Charts.isNullDict("sum_cpu",nbhoursGroup))
        jobsGroup = Charts.nameDict("Nombre de jobs du groupe", Charts.isNullDict("nb_job",nbhoursGroup))
        hoursUser = Charts.nameDict("Nombre d'heures de l'utilisateur", Charts.isNullDict("sum_cpu", jobSuccessHours))
        jobsUser = Charts.nameDict("Nombre de jobs de l'utilisateur", Charts.isNullDict("nb_job", jobSuccessHours))

        jobsSuccessFailed = combineDict(jobsSuccess, jobsFailed)
        nbHoursGroupUser = combineDict(hoursGroup, hoursUser)
        nbJobsGroupUser = combineDict(jobsGroup, jobsUser)


        #Exec time
        
        sql = """
            SELECT MAX(job_.ru_wallclock) AS max, AVG(job_.ru_wallclock) AS avg, MIN(job_.ru_wallclock) AS min 
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {multiGroup}
                {date}
            GROUP BY users.login ;
            """

        execTimeMAM = self.e.fetch(command=sql.format(  date=date,
                                                        multiGroup = "",
                                                        user=user))

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.ru_wallclock {test} (
                    SELECT AVG(job_.ru_wallclock)
                    FROM job_, users
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """      

        execTimeSupAvg = self.e.fetch(command=sql.format(   select='sup_avg',
                                                            date=date, 
                                                            test = ">",
                                                            user=user))
        
        execTimeInfAvg = self.e.fetch(command=sql.format(   select='inf_avg',
                                                            date=date, 
                                                            test = "<",
                                                            user=user))

        execTimeSupAvg = Charts.nameDict("Temps d'éxecution moyen supérieur", Charts.isNullDict("sup_avg", execTimeSupAvg))
        execTimeInfAvg = Charts.nameDict("Temps d'éxecution moyen inférieur", Charts.isNullDict("inf_avg", execTimeInfAvg))

        execTimeComparaison = combineDict(execTimeSupAvg, execTimeInfAvg)


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

        execTime1 = Charts.nameDict("< 86400", Charts.isNullDict("exectime", execTime1))
        execTime2 = Charts.nameDict("[86400; 604800]", Charts.isNullDict("exectime", execTime2))
        execTime3 = Charts.nameDict("[604800; 18144000]", Charts.isNullDict("exectime", execTime3))
        execTime4 = Charts.nameDict("> 18144000", Charts.isNullDict("exectime", execTime4))

        execTime = combineDict(execTime1, execTime2, execTime3, execTime4) #Posibilité que des valeurs disparaissent car value = 0.


        #Memory usage

        sql = """
            SELECT MAX(job_.maxvmem) AS max, AVG(job_.maxvmem) AS avg, MIN(job_.maxvmem) AS min
            FROM job_, users 
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY users.login ;
            """

        memUseMaxAvgMin = self.e.fetch(command=sql.format(  date=date, 
                                                            test = '',
                                                            user=user))

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

        memUseSupAvg = Charts.nameDict("Utilisation de la mémoire moyenne supérieur", Charts.isNullDict("jobs_sup_avg", memUseSupAvg))
        memUseInfAvg = Charts.nameDict("Utilisation de la mémoire moyenne inférieur", Charts.isNullDict("jobs_inf_avg", memUseInfAvg))

        memUseComparaison = combineDict(memUseSupAvg, memUseInfAvg)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {test}
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

        mUsage1 = Charts.nameDict("< 1073741824", Charts.isNullDict("musage", mUsage1))
        mUsage2 = Charts.nameDict("[1073741824; 4294967296]", Charts.isNullDict("musage", mUsage2))
        mUsage3 = Charts.nameDict("[4294967296; 858993459]", Charts.isNullDict("musage", mUsage3))
        mUsage4 = Charts.nameDict("[858993459; 17179869184]", Charts.isNullDict("musage", mUsage4))
        mUsage5 = Charts.nameDict("[17179869184; 34359738368]", Charts.isNullDict("musage", mUsage5))
        mUsage6 = Charts.nameDict("[34359738368; 68719476736]", Charts.isNullDict("musage", mUsage6))
        mUsage7 = Charts.nameDict("[68719476736; 137438953472]", Charts.isNullDict("musage", mUsage7))
        mUsage8 = Charts.nameDict("> 137438953472", Charts.isNullDict("musage", mUsage8))

        memUsage = combineDict(mUsage1, mUsage2, mUsage3, mUsage4, mUsage5, mUsage6, mUsage7, mUsage8) #Posibilité que des valeurs disparaissent car value = 0.


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
                                                            test = '',
                                                            user=user))

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                -- avg donné par requête imbriquée
                AND job_.slots  {test} (
                    SELECT AVG(job_.slots)
                    FROM job_, users
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """

        slotsPerJobsSupAvg = self.e.fetch(command=sql.format(   select='jobs_sup_avg',
                                                                date=date, 
                                                                test = ">",
                                                                user=user))
        
        slotsPerJobsInfAvg = self.e.fetch(command=sql.format(   select='jobs_inf_avg',
                                                                date=date, 
                                                                test = "<",
                                                                user=user))

        slotsPerJobsSupAvg = Charts.nameDict("Slots par job moyen supérieur", Charts.isNullDict("jobs_sup_avg", slotsPerJobsSupAvg))
        slotsPerJobsInfAvg = Charts.nameDict("Slots par job moyen inférieur", Charts.isNullDict("jobs_inf_avg", slotsPerJobsInfAvg))

        slotsPerJobsComparaison = combineDict(slotsPerJobsSupAvg, slotsPerJobsInfAvg)


        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.slots {test}
            GROUP BY users.login ;
            """

        slots1 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " = 1 ",
                                                    user=user))

        slots2 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 1 AND job_.slots <= 4 ",
                                                    user=user))

        slots3 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 5 AND job_.slots <= 8 ",
                                                    user=user))

        slots4 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 9 AND job_.slots <= 16 ",
                                                    user=user))

        slots5 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 17 AND job_.slots <= 32 ",
                                                    user=user))

        slots6 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 33 AND job_.slots <= 64 ",
                                                    user=user))

        slots7 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 65 AND job_.slots <= 128 ",
                                                    user=user))

        slots8 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 128 ",
                                                    user=user))

        slots1 = Charts.nameDict("= 1", Charts.isNullDict("slots", slots1))
        slots2 = Charts.nameDict("[1; 4]", Charts.isNullDict("slots", slots2))
        slots3 = Charts.nameDict("[5; 8]", Charts.isNullDict("slots", slots3))
        slots4 = Charts.nameDict("[9; 16]", Charts.isNullDict("slots", slots4))
        slots5 = Charts.nameDict("[17; 32]", Charts.isNullDict("slots", slots5))
        slots6 = Charts.nameDict("[33; 64]", Charts.isNullDict("slots", slots6))
        slots7 = Charts.nameDict("[65; 128]", Charts.isNullDict("slots", slots7))
        slots8 = Charts.nameDict("> 128", Charts.isNullDict("slots", slots8))

        slotsPerJob = combineDict(slots1, slots2, slots3, slots4, slots5, slots6, slots7, slots8)                                                        


        #Temps d'attente
        
        sql = """
            SELECT MAX(job_.start_time - job_.submit_time) as max, AVG(job_.start_time - job_.submit_time) as avg, -- MIN(job_.start_time - job_.submit_time) as min
            CASE WHEN MIN(job_.start_time - job_.submit_time) < 0 THEN 0
            ELSE MIN(job_.start_time - job_.submit_time)
            END 
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date} 
            GROUP BY users.login ;
            """
        
        waitingTimeMAM = self.e.fetch(command=sql.format(   date=date, 
                                                            test = '',
                                                            user=user))

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                -- avg donné par requête imbriquée
                AND (job_.start_time - job_.submit_time) > (
                    SELECT AVG(job_.start_time - job_.submit_time)
                    FROM job_, users
                    WHERE job_.id_user = users.id_user
                        AND users.login = '{user}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY users.login)
            GROUP BY users.login ;
            """

        waitingTimeSupAvg = self.e.fetch(command=sql.format(    select='wt_sup_avg',
                                                                date=date, 
                                                                test = ">",
                                                                user=user))
        
        waitingTimeInfAvg = self.e.fetch(command=sql.format(    select='wt_inf_avg',
                                                                date=date, 
                                                                test = "<",
                                                                user=user))

        waitingTimeSupAvg = Charts.nameDict("Slots par job moyen supérieur", Charts.isNullDict("wt_sup_avg", waitingTimeSupAvg))
        waitingTimeInfAvg = Charts.nameDict("Slots par job moyen inférieur", Charts.isNullDict("wt_inf_avg", waitingTimeInfAvg))

        waitingTimeComparaison = combineDict(waitingTimeSupAvg, waitingTimeInfAvg)


        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, users
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND (job_.start_time - job_.submit_time) {test}
            GROUP BY users.login;
            """

        waitingTime1 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "< 3600",
                                                            user=user))

        waitingTime2 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 3600 AND (job_.start_time - job_.submit_time) < 21600",
                                                            user=user))

        waitingTime3 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 21600 AND (job_.start_time - job_.submit_time) < 43200",
                                                            user=user))

        waitingTime4 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 43200 AND (job_.start_time - job_.submit_time) < 86400",
                                                            user=user))

        waitingTime5 = self.e.fetch(command=sql.format(     select='waitingtime',
                                                            date=date, 
                                                            test = "> 86400",
                                                            user=user))

        waitingTime1 = Charts.nameDict("< 3600", Charts.isNullDict("waitingtime", waitingTime1))
        waitingTime2 = Charts.nameDict("[3600; 21600]", Charts.isNullDict("waitingtime", waitingTime2))
        waitingTime3 = Charts.nameDict("[21600; 43200]", Charts.isNullDict("waitingtime", waitingTime3))
        waitingTime4 = Charts.nameDict("[43200; 86400]", Charts.isNullDict("waitingtime", waitingTime4))
        waitingTime5 = Charts.nameDict("> 86400", Charts.isNullDict("waitingtime", waitingTime5))

        waitingTime = combineDict(waitingTime1, waitingTime2, waitingTime3, waitingTime4, waitingTime5) 


        #Top ten
        
        sql = """
            SELECT queues.queue_name, {test} AS sum_
            FROM users, queues, job_
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND job_.id_queue = queues.id_queue
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY queues.queue_name
            ORDER BY sum_ DESC LIMIT 10 ;
        """

        topTenUsedQueues = self.e.fetch(command=sql.format(     date=date, 
                                                                test = 'sum(job_.cpu)',
                                                                user=user))

        topTenUsedNodes = self.e.fetch(command=sql.format(      date=date, 
                                                                test = 'count(job_.id_job_)',
                                                                user=user))

        topTenUsedQueues = Charts.multiDict(topTenUsedQueues, ['queue_name', 'sum_'])
        topTenUsedNodes = Charts.multiDict(topTenUsedNodes, ['queue_name', 'sum_'])

        sql = """
            SELECT hosts.hostname, {test} AS sum_
            FROM users, hosts, job_
            WHERE job_.id_user = users.id_user
                AND users.login = '{user}'
                AND job_.id_host = hosts.id_host
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY hosts.hostname
            ORDER BY sum_ DESC LIMIT 10 ;
            """
        
        topTenHostnameHours = self.e.fetch(command=sql.format(      date=date, 
                                                                    test = 'sum(job_.cpu)',
                                                                    user=user))

        topTenHostnameNbJobs = self.e.fetch(command=sql.format(     date=date, 
                                                                    test = 'count(job_.id_job_)',
                                                                    user=user))
        
        topTenHostnameHours = Charts.multiDict(topTenHostnameHours, ['hostname', 'sum_'])
        topTenHostnameNbJobs = Charts.multiDict(topTenHostnameNbJobs, ['hostname', 'sum_'])


        charts.append(  {"id": "chart1", "name" : "Information utilisateur/groupe", "charts" : (
                            {"id":"jobsSuccessFailed", "type": "PieChart", "values" : jobsSuccessFailed, "title" : "Taux réussite"},
                            {"id":"nbJobsGroupUser", "type": "PieChart", "values" : nbJobsGroupUser, "title" : "Nombre de jobs : Groupe"},
                            {"id":"nbHoursGroupUser", "type": "PieChart", "values" : nbHoursGroupUser, "title" : "Nombre d'heures : Groupe"}
                        )})

        charts.append(  {"id": "chart2", "name" : "Temps d'éxecution", "charts": (
                            {"id":"execTimeMAM", "type": "BarChart", "values" : execTimeMAM, "title" : "Temps d'exécution"},
                            {"id":"execTimeComparaison", "type": "PieChart", "values" : execTimeComparaison, "title" : "Temps d'exécution moyen"},
                            {"id":"execTime", "type": "BarChart", "values" : execTime, "title" : "Temps d'exécution"}
                        )})

        charts.append(  {"id": "chart3", "name" : "Utilisation de la mémoire", "charts": (
                            {"id":"memUseMaxAvgMin", "type": "BarChart", "values" : memUseMaxAvgMin, "title" : "Utilisation de la mémoire"},
                            {"id":"memUseComparaison", "type": "PieChart", "values" : memUseComparaison, "title" : "Utilisation de la mémoire moyenne"},
                            {"id":"memUsage", "type": "BarChart", "values" : memUsage, "title" : "Utilisation de la mémoire"}
                        )})

        charts.append(  {"id": "chart4", "name" : "Slots par jobs", "charts": (
                            {"id":"slotsPerJobsMAM", "type": "BarChart", "values" : slotsPerJobsMAM, "title" : "Slots par job"},
                            {"id":"slotsPerJobsComparaison", "type": "PieChart", "values" : slotsPerJobsComparaison, "title" : "Slots par job moyenne"},
                            {"id":"slotsPerJob", "type": "BarChart", "values" : slotsPerJob, "title" : "Slots par job"}
                        )})
        
        charts.append(  {"id": "chart5", "name" : "Temps d'attente", "charts": (
                            {"id":"waitingTimeMAM", "type": "BarChart", "values" : waitingTimeMAM, "title" : "Temps d'attente"},
                            {"id":"waitingTimeComparaison", "type": "PieChart", "values" : waitingTimeComparaison, "title" : "Temps d'attente moyen"},
                            {"id":"waitingTime", "type": "BarChart", "values" : waitingTime, "title" : "Temps d'attente"}
                        )})
        
        charts.append(  {"id": "chart6", "name" : "Top 10", "charts": (
                            {"id":"topTenUsedQueues", "type": "BarChart", "values" : topTenUsedQueues, "title" : "Top 10 des queues utilisées"},
                            {"id":"topTenUsedNodes", "type": "BarChart", "values" : topTenUsedNodes, "title" : "Top 10 des nodes utilisés"},
                            {"id":"topTenHostnameHours", "type": "BarChart", "values" : topTenHostnameHours, "title" : "Top 10 Hostnames (Heures)"},
                            {"id":"topTenHostnameNbJobs", "type": "BarChart", "values" : topTenHostnameNbJobs, "title" : "Top 10 Hostnames (nombre de jobs)"}
                        )})
  
        return charts, recall, error
    
