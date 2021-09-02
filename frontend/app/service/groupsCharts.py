from app.utils import splitDict
from app.service.charts import Charts

class groupsCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)

    def charts(self, form):
        charts = list()
        recall = dict()
        error = False

        # Variables input
        date = self.pickDate(form, recall)[0]
        groupName = form.groups.data
        recall["Groupe"] = groupName


        #if Catch erreurs then stop
        sql = """
            SELECT COUNT(job_.id_job_) AS nb_job
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe     
                AND groupes.group_name = '{groupName}'
                {date}
            GROUP BY groupes.id_groupe;
            """

        jobsTotal = self.e.fetch(command=sql.format(date=date, groupName=groupName))

        if(super().detectError(jobsTotal)):
            return charts, recall, True

        
        # Group, conso

        sql = """
            SELECT COUNT(job_.id_job_) as nb_job
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                {test}
                {date}
            GROUP BY groupes.id_groupe;
            """ 

        jobsSuccess = self.e.fetch(command=sql.format(   date=date,
                                                        test = 'AND (job_.failed = 0 OR job_.exit_status = 0)',
                                                        groupName = groupName))
        
        jobsFailed = self.e.fetch(command=sql.format(   date=date,
                                                        test = 'AND job_.failed != 0 AND job_.exit_status != 0',
                                                        groupName = groupName))

        jobsSuccess = super().nameDict("Jobs réussi", super().isNullDict("nb_job", jobsSuccess))
        jobsFailed = super().nameDict("Jobs mauvais", super().isNullDict("nb_job", jobsFailed))

        jobsSuccessFailed = (jobsSuccess, jobsFailed)


        # Group, Exec time

        sql = """
            SELECT min(job_.ru_wallclock) as min, avg(job_.ru_wallclock) as avg, max(job_.ru_wallclock) as max
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                {date}
            GROUP BY groupes.group_name ;
            """
        
        execTimeMAM = self.e.fetch(command=sql.format(  date=date,
                                                        groupName = groupName))
        execTimeMAM = splitDict(execTimeMAM)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                -- avg donné par requête imbriquée
                AND job_.ru_wallclock {test} (
                    SELECT AVG(job_.ru_wallclock)
                    FROM job_, groupes
                    WHERE job_.id_groupe = groupes.id_groupe
                        AND groupes.group_name = '{groupName}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY groupes.group_name)
            GROUP BY groupes.group_name ;
            """
        
        execTimeSupAvg = self.e.fetch(command=sql.format(   select='sup_avg',
                                                            date=date, 
                                                            test = ">",
                                                            groupName = groupName))
        
        execTimeInfAvg = self.e.fetch(command=sql.format(   select='inf_avg',
                                                            date=date, 
                                                            test = "<",
                                                            groupName = groupName))

        execTimeSupAvg = super().nameDict("Temps d'éxecution moyen supérieur", super().isNullDict("sup_avg", execTimeSupAvg))
        execTimeInfAvg = super().nameDict("Temps d'éxecution moyen inférieur", super().isNullDict("inf_avg", execTimeInfAvg))

        execTimeComparaison = (execTimeSupAvg, execTimeInfAvg)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.ru_wallclock {test}
            GROUP BY groupes.group_name ;
            """
        
        execTime1 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " < 86400 ",
                                                        groupName=groupName))

        execTime2 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 86400 AND job_.ru_wallclock < 604800 ",
                                                        groupName=groupName))

        execTime3 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 604800 AND job_.ru_wallclock < 18144000 ",
                                                        groupName=groupName))
        
        execTime4 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 18144000 ",
                                                        groupName=groupName))

        execTime1 = super().nameDict("< 24", super().isNullDict("exectime", execTime1))
        execTime2 = super().nameDict("[24; 168]", super().isNullDict("exectime", execTime2))
        execTime3 = super().nameDict("[168; 5 040]", super().isNullDict("exectime", execTime3))
        execTime4 = super().nameDict("> 5 040", super().isNullDict("exectime", execTime4))

        execTime = (execTime1, execTime2, execTime3, execTime4) #Posibilité que des valeurs disparaissent car value = 0.


        # Mem Usage

        sql = """
            SELECT MAX(job_.maxvmem) AS max, AVG(job_.maxvmem) AS avg, MIN(job_.maxvmem) AS min
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY groupes.group_name ;
            """
        
        memUseMAM = self.e.fetch(command=sql.format(  date=date, 
                                                            groupName=groupName))
        memUseMAM = splitDict(memUseMAM)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.maxvmem {test} (
                    SELECT AVG(job_.maxvmem)
                    FROM job_, groupes
                    WHERE job_.id_groupe = groupes.id_groupe
                        AND groupes.group_name = '{groupName}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY groupes.group_name)
            GROUP BY groupes.group_name ;
            """
        
        memUseSupAvg = self.e.fetch(command=sql.format( select='jobs_sup_avg',
                                                        date=date, 
                                                        test = ">",
                                                        groupName=groupName))
        
        memUseInfAvg = self.e.fetch(command=sql.format( select='jobs_inf_avg',
                                                        date=date, 
                                                        test = "<",
                                                        groupName=groupName))

        memUseSupAvg = super().nameDict("Utilisation de la mémoire moyenne supérieur", super().isNullDict("jobs_sup_avg", memUseSupAvg))
        memUseInfAvg = super().nameDict("Utilisation de la mémoire moyenne inférieur", super().isNullDict("jobs_inf_avg", memUseInfAvg))

        memUseComparaison = (memUseSupAvg, memUseInfAvg)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                {test}
            GROUP BY groupes.group_name ;
            """
        
        mUsage1 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " < 1073741824 ",
                                                    groupName=groupName))

        mUsage2 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 1073741824 AND job_.maxvmem < 4294967296 ",
                                                    groupName=groupName))

        mUsage3 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 4294967296 AND job_.maxvmem < 858993459 ",
                                                    groupName=groupName))

        mUsage4 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 8589934592 AND job_.maxvmem < 17179869184 ",
                                                    groupName=groupName))

        mUsage5 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 17179869184 AND job_.maxvmem < 34359738368 ",
                                                    groupName=groupName))

        mUsage6 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 34359738368 AND job_.maxvmem < 68719476736 ",
                                                    groupName=groupName))

        mUsage7 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 68719476736 AND job_.maxvmem < 137438953472 ",
                                                    groupName=groupName))

        mUsage8 = self.e.fetch(command=sql.format(  select='musage',
                                                    date=date, 
                                                    test = " > 137438953472 ",
                                                    groupName=groupName))

        mUsage1 = super().nameDict("< 1", super().isNullDict("musage", mUsage1))
        mUsage2 = super().nameDict("[1; 4]", super().isNullDict("musage", mUsage2))
        mUsage3 = super().nameDict("[4; 8]", super().isNullDict("musage", mUsage3))
        mUsage4 = super().nameDict("[8; 16]", super().isNullDict("musage", mUsage4))
        mUsage5 = super().nameDict("[16; 32]", super().isNullDict("musage", mUsage5))
        mUsage6 = super().nameDict("[32; 64]", super().isNullDict("musage", mUsage6))
        mUsage7 = super().nameDict("[64; 128]", super().isNullDict("musage", mUsage7))
        mUsage8 = super().nameDict("> 128", super().isNullDict("musage", mUsage8))

        memUsage = (mUsage1, mUsage2, mUsage3, mUsage4, mUsage5, mUsage6, mUsage7, mUsage8) #Posibilité que des valeurs disparaissent car value = 0.


        # Slots usage

        sql = """
            SELECT min(job_.slots) as min, avg(job_.slots) as avg, max(job_.slots) as max
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY groupes.group_name ;
            """
        
        slotsPerJobsMAM = self.e.fetch(command=sql.format(  date=date,
                                                            groupName=groupName))
        slotsPerJobsMAM = splitDict(slotsPerJobsMAM)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.slots {test} (
                    SELECT AVG(job_.slots)
                    FROM job_, groupes
                    WHERE job_.id_groupe = groupes.id_groupe
                        AND groupes.group_name = '{groupName}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY groupes.group_name)
            GROUP BY groupes.group_name ;
            """
        
        slotsPerJobsSupAvg = self.e.fetch(command=sql.format(   select='jobs_sup_avg',
                                                                date=date, 
                                                                test = ">",
                                                                groupName=groupName))
        
        slotsPerJobsInfAvg = self.e.fetch(command=sql.format(   select='jobs_inf_avg',
                                                                date=date, 
                                                                test = "<",
                                                                groupName=groupName))

        slotsPerJobsSupAvg = super().nameDict("Slots par job moyen supérieur", super().isNullDict("jobs_sup_avg", slotsPerJobsSupAvg))
        slotsPerJobsInfAvg = super().nameDict("Slots par job moyen inférieur", super().isNullDict("jobs_inf_avg", slotsPerJobsInfAvg))

        slotsPerJobsComparaison = (slotsPerJobsSupAvg, slotsPerJobsInfAvg)

        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, groupes
            WHERE job_.id_groupe = groupes.id_groupe
                AND groupes.group_name = '{groupName}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.slots {test}
            GROUP BY groupes.group_name;
            """
        
        slots1 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " = 1 ",
                                                    groupName=groupName))

        slots2 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 1 AND job_.slots <= 4 ",
                                                    groupName=groupName))

        slots3 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 5 AND job_.slots <= 8 ",
                                                    groupName=groupName))

        slots4 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 9 AND job_.slots <= 16 ",
                                                    groupName=groupName))

        slots5 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 17 AND job_.slots <= 32 ",
                                                    groupName=groupName))

        slots6 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 33 AND job_.slots <= 64 ",
                                                    groupName=groupName))

        slots7 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 65 AND job_.slots <= 128 ",
                                                    groupName=groupName))

        slots8 = self.e.fetch(command=sql.format(   select='slots',
                                                    date=date, 
                                                    test = " > 128 ",
                                                    groupName=groupName))

        slots1 = super().nameDict("= 1", super().isNullDict("slots", slots1))
        slots2 = super().nameDict("[1; 4]", super().isNullDict("slots", slots2))
        slots3 = super().nameDict("[5; 8]", super().isNullDict("slots", slots3))
        slots4 = super().nameDict("[9; 16]", super().isNullDict("slots", slots4))
        slots5 = super().nameDict("[17; 32]", super().isNullDict("slots", slots5))
        slots6 = super().nameDict("[33; 64]", super().isNullDict("slots", slots6))
        slots7 = super().nameDict("[65; 128]", super().isNullDict("slots", slots7))
        slots8 = super().nameDict("> 128", super().isNullDict("slots", slots8))

        slotsPerJob = (slots1, slots2, slots3, slots4, slots5, slots6, slots7, slots8)                                                        


        charts.append(  {"id": "chart1", "name" : "Information utilisateur/groupe", "charts" : (
                            {"id":"jobsSuccessFailed", "type": "PieChart", "values" : jobsSuccessFailed, "title" : "Taux réussite"},
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
  
        return charts, recall, error
