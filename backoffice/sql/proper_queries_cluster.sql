--
-- proper SQL, for database queries
--
-- fixed example:
-- cluster = X5 OR all
-- year = 2012 (in epoch, 01-01-2012, 01-01-2013), OR all
--


-- top ten, with cluster_name, hostname, tout clusters confondus
SELECT 
  clusters.cluster_name, 
  hosts.hostname, 
  sum(job_.cpu) AS sum_cpu_value,
  sum(job_.ru_utime) AS sum_cpu_utime
FROM 
  job_, 
  clusters, 
  hosts_in_clusters, 
  hosts
WHERE 
  hosts_in_clusters.id_cluster = clusters.id_cluster 
  AND hosts.id_host = job_.id_host 
  AND hosts.id_host = hosts_in_clusters.id_host
GROUP BY
  clusters.cluster_name, hosts.hostname
ORDER BY
  sum_cpu_value DESC
LIMIT 10;

-- top ten, with hostname, par cluster (X5, 2012)
SELECT hosts.hostname, sum(job_.cpu) AS sum_cpu
FROM job_,
    hosts,
    hosts_in_clusters,
    clusters
WHERE job_.id_host = hosts.id_host 
    AND hosts.id_host = hosts_in_clusters.id_host 
    AND hosts_in_clusters.id_cluster = clusters.id_cluster 
    AND clusters.cluster_name = 'X5'
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY hosts.hostname, job_.id_host
ORDER BY sum_cpu DESC
LIMIT 10 ;

