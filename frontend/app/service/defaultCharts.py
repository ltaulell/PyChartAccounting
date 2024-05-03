from app.utils import splitDict
from app.service.charts import Charts

class defaultCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)
    
    def charts(self, form):
        charts = list()
        recall = dict()
        error = False

        # Variables input
        date = self.pickDate(form, recall)[0]
        recall["default"] = "oui"


        sql = """
            SELECT groupes.group_name, {select}
            FROM {fromC}
            WHERE job_.id_groupe = groupes.id_groupe
                AND job_.id_queue = queues.id_queue 
                AND (job_.failed = 0 OR job_.exit_status = 0) 
                {date}
            GROUP BY groupes.group_name, {group}
            ORDER BY {order}
            LIMIT 10 ;
            """
            
        topTenUsedQueuesByHours = self.e.fetch(command=sql.format(  date=date,
                                                                    select = 'queues.queue_name, sum(job_.cpu) / 3600 AS sum_cpu',
                                                                    fromC = 'groupes, queues, job_',
                                                                    group = 'queues.queue_name',
                                                                    order = 'sum_cpu DESC'
                                                                    ))

        topTenUsedQueuesByJobs = self.e.fetch(command=sql.format(  date=date,
                                                                    select = 'queues.queue_name, count(job_.id_job_) AS sum_job',
                                                                    fromC = 'groupes, queues, job_',
                                                                    group = 'queues.queue_name',
                                                                    order = 'sum_job DESC '
                                                                    )) 
        
        topTenUsedHostByHours = self.e.fetch(command=sql.format(    date=date,
                                                                    select = 'hosts.hostname, sum(job_.cpu) / 3600 AS sum_cpu',
                                                                    fromC = 'groupes, hosts, job_',
                                                                    group = 'hosts.hostname',
                                                                    order = 'sum_cpu DESC'
                                                                    ))  

        topTenUsedHostByJobs = self.e.fetch(command=sql.format(    date=date,
                                                                    select = 'hosts.hostname, count(job_.id_job_) AS sum_job',
                                                                    fromC = 'groupes, hosts, job_',
                                                                    group = 'hosts.hostname',
                                                                    order = 'sum_job DESC'
                                                                    ))                                                                     

        topTenMaxvmem = self.e.fetch(command=sql.format(    date=date,
                                                                    select = 'job_.maxvmem',
                                                                    fromC = 'job_, groupes',
                                                                    group = 'job_.maxvmem ',
                                                                    order = 'job_.maxvmem DESC'
                                                                    ))

        topTenTempsAttente = self.e.fetch(command=sql.format(    date=date,
                                                                    select = '(job_.start_time - job_.submit_time) / 3600 AS await',
                                                                    fromC = 'job_, groupes',
                                                                    group = 'await',
                                                                    order = 'await DESC'
                                                                    ))
                                                                    
        topTenUsedQueuesByHours = super().multiDict(topTenUsedQueuesByHours, [['queue_name', 'sum_cpu'], ['group_name']])

        sql = """
            SELECT
                queues.queue_name,
                max(job_.cpu) as max_cpu
            FROM 
                job_, queues
            WHERE
                job_.id_queue = queues.id_queue
                {date}
            GROUP BY queues.queue_name
            ORDER BY max_cpu DESC
            LIMIT 10;
        """

        topTenUsedQueues = self.e.fetch(command=sql.format(    date=date))



        charts.append(  {"id": "chart5", "name" : "Temps d'attente", "charts": (
                            {"id":"waitingTimeMAM", "type": "bar", "values" : topTenUsedQueuesByHours, "title" : "Temps d'attente"},
                            {"id":"waitingTimeComparaison", "type": "pie", "values" : topTenUsedQueuesByJobs, "title" : "Temps d'attente moyen"},
                            {"id":"waitingTimeComparaison", "type": "pie", "values" : topTenUsedHostByJobs, "title" : "Temps d'attente moyen"},
                            {"id":"waitingTimeComparaison", "type": "pie", "values" : topTenMaxvmem, "title" : "Temps d'attente moyen"},
                            {"id":"waitingTimeComparaison", "type": "pie", "values" : topTenTempsAttente, "title" : "Temps d'attente moyen"},
                            {"id":"waitingTime", "type": "bar", "values" : topTenUsedHostByHours, "title" : "Temps d'attente"}
                        )})
        
        charts.append(  {"id": "chart6", "name" : "Top 10", "charts": (
                            {"id":"topTenUsedQueues", "type": "bar", "values" : topTenUsedQueues, "title" : "Top 10 des queues utilisées"},
                        )})

       
        return charts, recall, error