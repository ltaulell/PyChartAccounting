
--
-- \dt+    -> tables
-- \ds+    -> sequences
-- \dS+ <table>    -> types et contraintes
--

select * from users;
select * from users where login = 'ltaulell';
select * from hosts where hostname like 'r410%';

ALTER TABLE job_ ALTER COLUMN job_name TYPE varchar(255);
ALTER TABLE job_ ALTER COLUMN job_name DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN ru_wallclock DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN ru_utime DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN ru_stime DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN slots DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN cpu DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN mem DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN io DROP NOT NULL;
ALTER TABLE job_ ALTER COLUMN maxvmem DROP NOT NULL;

-- utiliser explain, pour les query plan
-- pour voir où ça bouffe du temps

-- # https://www.epochconverter.com/
-- epoch (2010-01-01) 1262304000
-- epoch (2010-12-31) 1293753600
-- epoch (2011-12-31) 1325289600
-- epoch (2012-12-31) 1356912000
-- epoch (2013-12-31) 1388448000
-- epoch (2014-12-31) 1419984000
-- epoch (2015-12-31) 1451520000
-- epoch (2016-12-31) 1483142400
-- epoch (2017-12-31) 1514678400
-- epoch (2018-12-31) 1546214400
-- epoch (2019-12-31) 1577750400
-- epoch (2020-12-31) 1609372800
-- epoch (2021-12-31) 1640908800

-- # https://sql.sh/cours/jointures

-- total utime d'un user (cmichel)
SELECT users.login, sum(job_.ru_utime)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
GROUP BY users.login ;

-- nb de jobs d'un user (cmichel)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel' 
GROUP BY users.login ;

-- nb de jobs plantés d'un user (cmichel)
-- # https://www.postgresqltutorial.com/postgresql-count-function/
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND job_.failed != 0
    AND job_.exit_status != 0
GROUP BY users.login ;

-- nb de jobs réussis d'un user (cmichel)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
GROUP BY users.login ;

-- total utime d'un groupe (icbms)
SELECT groupes.group_name, sum(job_.ru_utime)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'icbms'
GROUP BY groupes.group_name ;

-- total utime de tous les groupes (jobs réussis)
SELECT groupes.group_name, sum(job_.ru_utime) AS sum_utime, count(job_.id_job_) AS nb_job
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND (job_.failed = 0 OR job_.exit_status = 0)
    -- AND job_.start_time >= 1325289600
    -- AND job_.start_time <= 1356912000
GROUP BY groupes.group_name
ORDER BY sum_utime DESC ;

-- same-same avec cpu pour comparer avec les anciennes stats "excel"
SELECT groupes.group_name, sum(job_.cpu) AS sum_cpu, count(job_.id_job_) AS nb_job
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND (job_.failed = 0 OR job_.exit_status = 0)
    -- AND job_.start_time >= 1325289600
    -- AND job_.start_time <= 1356912000
GROUP BY groupes.group_name
ORDER BY sum_cpu DESC ;


-- total cpu d'un group (chimie) entre 01-01-2012 et 31-12-2012 (start_time)
SELECT sum(job_.cpu)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
  AND groupes.group_name = 'chimie'
  AND job_.start_time >= 1325289600
  AND job_.start_time <= 1356912000
  ;

-- total cpu, par groupe, entre 01-01-2012 et 31-12-2012 (start_time), plus rapide
SELECT groupes.group_name, sum(job_.cpu) AS sum_cpu
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
  AND start_time >= 1325289600
  AND start_time <= 1356912000
GROUP BY groupes.group_name
ORDER BY sum_cpu DESC;

-- max wallclock d'un groupe (icbms)
SELECT groupes.group_name, max(job_.ru_wallclock)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'icbms'
GROUP BY groupes.group_name ;

-- max wallclock (sur tous les jobs) d'un groupe (chimie)
SELECT groupes.group_name, max(job_.ru_wallclock)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
GROUP BY groupes.group_name ;

-- average slots (sur tous les jobs) d'un groupe (chimie)
SELECT groupes.group_name, avg(job_.slots)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
GROUP BY groupes.group_name ;

-- average slots (sur tous les jobs réussis) pour tous les groupes
SELECT groupes.group_name, avg(job_.slots) AS avg_slots, count(job_.id_job_) AS nb_job
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND (job_.failed = 0 OR job_.exit_status = 0)
GROUP BY groupes.group_name
ORDER BY avg_slots DESC ;

-- max slots (sur tous les jobs) d'un groupe (chimie)
SELECT groupes.group_name, max(job_.slots), count(job_.id_job_)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
GROUP BY groupes.group_name ;


-- dernier job ?
select * from job_ where start_time = (select max(start_time) from job_);
select * from job_ where submit_time = (select max(submit_time) from job_);
select * from job_ where end_time = (select max(end_time) from job_);

-- dernier job inséré
select max(id_job_) from job_;

-- info sur le dernier job inséré
SELECT q.queue_name, h.hostname, g.group_name, u.login, j.job_id, j.submit_time
FROM job_ j
INNER JOIN queues q ON j.id_queue = q.id_queue
INNER JOIN hosts h ON j.id_host = h.id_host
INNER JOIN groupes g ON j.id_groupe = g.id_groupe
INNER JOIN users u ON j.id_user = u.id_user
WHERE j.id_job_ = 
    (SELECT max(id_job_) FROM job_)
    ;

select job_id, cpu from job_ where failed != 0 AND exit_status != 0;


-- top ten, id_host, par cluster
SELECT j.id_host, sum(ru_utime) AS sum_value
FROM job_ j
WHERE id_host = ANY 
    (SELECT id_host 
    FROM hosts_in_clusters 
    WHERE id_cluster = 
        (SELECT id_cluster 
        FROM clusters 
        WHERE cluster_name = 'E5'
        )
    )
GROUP BY j.id_host
ORDER BY sum_value DESC
LIMIT 10 ;

-- top ten, with hostname, par cluster
SELECT h.hostname, sum(j.cpu), sum(j.ru_utime) AS sum_value
FROM job_ j
INNER JOIN hosts h ON j.id_host = h.id_host
WHERE j.id_host = ANY 
    (SELECT id_host 
    FROM hosts_in_clusters 
    WHERE id_cluster = 
        (SELECT id_cluster 
        FROM clusters 
        WHERE cluster_name = 'E5'
        )
    )
GROUP BY h.hostname, j.id_host
ORDER BY sum_value DESC
LIMIT 10 ;
-- pareil, plus rapide
SELECT hosts.hostname, 
    sum(job_.cpu) AS sum_cpu, 
    sum(job_.ru_utime) AS sum_utime
FROM job_,
    hosts,
    hosts_in_clusters,
    clusters
WHERE job_.id_host = hosts.id_host AND 
    hosts.id_host = hosts_in_clusters.id_host AND
    hosts_in_clusters.id_cluster = clusters.id_cluster AND
    clusters.cluster_name = 'E5'
GROUP BY hosts.hostname, job_.id_host
ORDER BY sum_cpu DESC
LIMIT 10 ;

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
  hosts_in_clusters.id_cluster = clusters.id_cluster AND
  hosts.id_host = job_.id_host AND
  hosts.id_host = hosts_in_clusters.id_host
GROUP BY
  clusters.cluster_name, hosts.hostname
ORDER BY
  sum_cpu_value DESC
LIMIT 10;

