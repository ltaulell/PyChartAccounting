from app.utils import splitDict
from app.service.charts import Charts

class queuesCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)
    
    def charts(self, form):
        charts = list()
        recall = dict()
        error = False

        # Variables input
        date = self.pickDate(form, recall)[0]
        queue = form.queue.data
        recall["queue"] = queue

        #if 0, Catch erreurs then stop
        sql = """
            SELECT COUNT(queues.queue_name) AS nb_job
            FROM job_, queues
            WHERE job_.id_queue = queues.id_queue
                AND queues.queue_name = '{queue}'
                {date}
            GROUP BY queues.queue_name;
            """
        
        jobsTotal = self.e.fetch(command=sql.format(    date=date,
                                                        queue = queue))
        
        if(super().detectError(jobsTotal)):
            return charts, recall, True


        # Exec time

        sql = """
            SELECT MAX(job_.ru_wallclock) AS max, AVG(job_.ru_wallclock) AS avg, MIN(job_.ru_wallclock) AS min
            FROM job_, queues
            WHERE job_.id_queue = queues.id_queue
                AND queues.queue_name = '{queue}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
            GROUP BY queues.queue_name ;
            """
        
        execTimeMAM = self.e.fetch(command=sql.format(  date=date,
                                                        queue=queue))
        execTimeMAM = splitDict(execTimeMAM)
        
        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, queues
            WHERE job_.id_queue = queues.id_queue
                AND queues.queue_name = '{queue}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                -- avg donné par requête imbriquée
                AND job_.ru_wallclock {test} (
                    SELECT AVG(job_.ru_wallclock)
                    FROM job_, queues
                    WHERE job_.id_queue = queues.id_queue
                        AND queues.queue_name = '{queue}'
                        AND (job_.failed = 0 OR job_.exit_status = 0)
                        {date}
                    GROUP BY queues.queue_name)
            GROUP BY queues.queue_name ;
            """
        
        execTimeSupAvg = self.e.fetch(command=sql.format(   select='sup_avg',
                                                            date=date, 
                                                            test = ">",
                                                            queue=queue))
        
        execTimeInfAvg = self.e.fetch(command=sql.format(   select='inf_avg',
                                                            date=date, 
                                                            test = "<",
                                                            queue=queue))

        execTimeSupAvg = super().nameDict("Temps d'exécution > moyenne", super().isNullDict("sup_avg", execTimeSupAvg))
        execTimeInfAvg = super().nameDict("Temps d'exécution < moyenne", super().isNullDict("inf_avg", execTimeInfAvg))

        execTimeComparaison = (execTimeSupAvg, execTimeInfAvg)


        sql = """
            SELECT COUNT(job_.id_job_) as {select}
            FROM job_, queues
            WHERE job_.id_queue = queues.id_queue
                AND queues.queue_name = '{queue}'
                AND (job_.failed = 0 OR job_.exit_status = 0)
                {date}
                AND job_.ru_wallclock {test}
            GROUP BY queues.queue_name ;
            """
        
        execTime1 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " < 86400 ",
                                                        queue=queue))

        execTime2 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 86400 AND job_.ru_wallclock < 604800 ",
                                                        queue=queue))

        execTime3 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 604800 AND job_.ru_wallclock < 18144000 ",
                                                        queue=queue))
        
        execTime4 = self.e.fetch(command=sql.format(    select='exectime',
                                                        date=date, 
                                                        test = " > 18144000 ",
                                                        queue=queue))

        execTime1 = super().nameDict("< 24", super().isNullDict("exectime", execTime1))
        execTime2 = super().nameDict("[24; 168]", super().isNullDict("exectime", execTime2))
        execTime3 = super().nameDict("[168; 5 040]", super().isNullDict("exectime", execTime3))
        execTime4 = super().nameDict("> 5 040", super().isNullDict("exectime", execTime4))

        execTime = (execTime1, execTime2, execTime3, execTime4) #Posibilité que des valeurs disparaissent car value = 0.


        # Queue exec jobs

        sql = """
            SELECT COUNT(job_.id_job_) AS nb_job
            FROM job_, queues
            WHERE job_.id_queue = queues.id_queue
                AND queues.queue_name = '{queue}'
                {test}
                {date}
            GROUP BY queues.queue_name ;
            """

        jobsSuccess = self.e.fetch(command=sql.format(   date=date,
                                                        test = 'AND (job_.failed = 0 OR job_.exit_status = 0)',
                                                        queue = queue))
        
        jobsFailed = self.e.fetch(command=sql.format(   date=date,
                                                        test = 'AND job_.failed != 0 AND job_.exit_status != 0',
                                                        queue = queue))

        jobsSuccess = super().nameDict("Jobs réussi", super().isNullDict("nb_job", jobsSuccess))
        jobsFailed = super().nameDict("Jobs mauvais", super().isNullDict("nb_job", jobsFailed))

        jobsSuccessFailed = (jobsSuccess, jobsFailed)

        charts.append(  {"id": "chart1", "name" : "Information Queue", "charts" : (
                            {"id":"jobsSuccessFailed", "type": "pie", "values" : jobsSuccessFailed, "title" : "Taux réussite"},
                        )})

        charts.append(  {"id": "chart2", "name" : "Temps d'exécution", "charts": (
                            {"id":"execTimeMAM", "type": "bar", "values" : execTimeMAM, "title" : "Temps d'exécution (heures)"},
                            {"id":"execTimeComparaison", "type": "pie", "values" : execTimeComparaison, "title" : "Temps d'exécution moyen (heures)"},
                            {"id":"execTime", "type": "bar", "values" : execTime, "title" : "Temps d'exécution (heures, répartition)"}
                        )})

        return charts, recall, error
