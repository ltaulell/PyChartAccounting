from app.utils import combineDict
from app.service.charts import Charts


class clusterCharts(Charts):
    def __init__(self, bddCon):
        super().__init__(bddCon)
    
    def charts(self, form):
        charts = list()
        recall = dict()
        error = False

        # Variables input
        date = self.pickDate(form, recall)[0]
        cluster = form.cluster.data
        recall["cluster"] = cluster

        sql = """
            SELECT hosts.hostname, sum(job_.cpu) AS sum_cpu
            FROM job_, hosts, hosts_in_clusters, clusters
            WHERE job_.id_host = hosts.id_host
                AND hosts.id_host = hosts_in_clusters.id_host
                AND hosts_in_clusters.id_cluster = clusters.id_cluster
                AND clusters.cluster_name = '{cluster}'
                {date}
            GROUP BY hosts.hostname, job_.id_host 
            ORDER BY sum_cpu DESC LIMIT 10 ;
            """
        
        topTenUsedCluster = self.e.fetch(command=sql.format(    date=date, 
                                                                cluster=cluster))
        #if 0, Catch erreurs then stop
        if(type(topTenUsedCluster) == int):
            return charts, recall, True

        topTenUsedCluster = Charts.multiDict(topTenUsedCluster, ['hostname', 'sum_cpu'])

        charts.append(  {"id": "chart6", "name" : "Top 10", "charts": (
                            {"id":"topTenUsedCluster", "type": "BarChart", "values" : topTenUsedCluster, "title" : "Top 10 des cluster utilisées"},
                        )})
        
        return charts, recall, error