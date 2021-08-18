
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

-- WITH date_insert AS (SELECT CURRENT_TIMESTAMP)
-- INSERT INTO history(last_offset_position, date_insert) VALUES(%s, %s) RETURNING id_insertion;

-- utiliser explain, pour les query plan
-- pour voir où ça bouffe du temps

-- # https://www.epochconverter.com/
-- epoch (2010-01-01) 1262304000
-- epoch (2011-01-01) 1293840000
-- epoch (2012-01-01) 1325376000
-- epoch (2013-01-01) 1356998400
-- epoch (2014-01-01) 1388534400
-- epoch (2015-01-01) 1420070400
-- epoch (2016-01-01) 1451606400
-- epoch (2017-01-01) 1483228800
-- epoch (2018-01-01) 1514764800
-- epoch (2019-01-01) 1546300800
-- epoch (2020-01-01) 1577836800
-- epoch (2021-01-01) 1609459200
-- epoch (2022-01-01) 1640995200

-- # https://sql.sh/cours/jointures
-- # https://www.postgresqltutorial.com/postgresql-count-function/

-- total cpu d'un user (cmichel)
SELECT users.login, sum(job_.cpu)
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


-- total cpu d'un groupe (icbms)
SELECT groupes.group_name, sum(job_.cpu)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'icbms'
GROUP BY groupes.group_name ;

-- same-same avec cpu pour comparer avec les anciennes stats "excel"
SELECT groupes.group_name, sum(job_.cpu) AS sum_cpu, count(job_.id_job_) AS nb_job
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND (job_.failed = 0 OR job_.exit_status = 0)
    -- AND job_.start_time >= 1325376000
    -- AND job_.start_time <= 1356998400
GROUP BY groupes.group_name
ORDER BY sum_cpu DESC ;

-- total cpu d'un group (chimie) entre 01-01-2012 et 31-12-2012 (start_time)
SELECT sum(job_.cpu)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
  ;

-- total cpu, par groupe, entre 01-01-2012 et 31-12-2012 (start_time), plus rapide
SELECT groupes.group_name, sum(job_.cpu) AS sum_cpu
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND start_time >= 1325376000
    AND start_time <= 1356998400
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

-- min slots (sur tous les jobs) d'un groupe (chimie)
-- average slots (sur tous les jobs) d'un groupe (chimie)
-- max slots (sur tous les jobs) d'un groupe (chimie)
SELECT groupes.group_name, 
    min(job_.slots),
    avg(job_.slots),
    max(job_.slots)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
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

-- top ten, with hostname, par cluster
-- pareil, plus rapide (X5, 2012)
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


-- nb jobs réussis, queue r815lin128ib, 2012, durée inférieure à 1 jour (86400)
SELECT queues.queue_name,
    COUNT(job_.id_job_)
FROM job_, queues
WHERE 
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock < 86400
GROUP BY queues.queue_name ;
-- same-same
SELECT queues.queue_name, COUNT(job_.id_job_)
FROM queues
JOIN job_ ON job_.id_queue = queues.id_queue
WHERE
    queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock < 86400
GROUP BY queues.queue_name ;



-- users in multiple groups
SELECT
    users.login
FROM
    users_in_groupes, users, groupes
WHERE
    users.id_user = users_in_groupes.id_user
    AND groupes.id_groupe = users_in_groupes.id_groupe
GROUP BY users.login
HAVING count(users_in_groupes.id_user) > 1 ;

-- les groupes qui correspondent, pour chaque résultat
SELECT
    users.login, groupes.group_name
FROM
    users_in_groupes, users, groupes
WHERE
    users.id_user = users_in_groupes.id_user
    AND groupes.id_groupe = users_in_groupes.id_groupe
    -- voir requête précédente
    AND users.login = %login%
GROUP BY groupes.group_name, users.login 
ORDER BY groupes.group_name ;



