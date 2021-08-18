--
-- proper SQL, for database queries
--
-- fixed example:
-- user = cmichel,
-- groupe = chimie,
-- year = 2012 (in epoch, 01-01-2012, 01-01-2013)
--

-- composite cmichel vs chimie
-- nb de jobs réussis, nb d'heures consommées d'un user (cmichel, 2012)
SELECT users.login, COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu) AS sum_cpu
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;
-- nb de jobs réussis, nb d'heures d'un groupe (chimie, 2012) moins un user particulier
SELECT groupes.group_name, COUNT(job_.id_job_) AS nb_job, SUM(job_.cpu) AS sum_cpu
FROM job_, groupes, users
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.id_user = users.id_user
    AND users.login != 'cmichel'
GROUP BY groupes.id_groupe ;

-- taux de réussite
-- nb de jobs réussis d'un user (cmichel, 2012)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;
-- nb de jobs plantés d'un user (cmichel, 2012)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND job_.failed != 0
    AND job_.exit_status != 0
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;

-- execution time
-- max, avg, min for ru_wallclock, user cmichel, 2012
SELECT
    users.login,
    MAX(job_.ru_wallclock) AS max_wall,
    AVG(job_.ru_wallclock) AS avg_wall,
    MIN(job_.ru_wallclock) AS min_wall
FROM 
    job_, users
WHERE
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;
-- jobs au dessus de avg(ru_wallclock), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.ru_wallclock > (
    SELECT 
        AVG(job_.ru_wallclock)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY users.login
    )
GROUP BY users.login ;
-- jobs en dessous de avg(ru_wallclock), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.ru_wallclock < (
    SELECT 
        AVG(job_.ru_wallclock)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY users.login
    )
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, durée inférieure à 1 jour (86400)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock < 86400
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, durée entre 1 jour (86400) et 1 week (604800)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 86400
    AND job_.ru_wallclock < 604800
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, durée entre 1 week (604800) et 1 mois (18144000)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 604800
    AND job_.ru_wallclock < 18144000
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, durée supérieure à 1 mois (18144000)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 18144000
GROUP BY users.login ;

-- memory usage
-- max, avg, min for maxvmem, user cmichel, 2012
SELECT
    users.login,
    MAX(job_.maxvmem) AS max_mem,
    AVG(job_.maxvmem) AS avg_mem,
    MIN(job_.maxvmem) AS min_mem
FROM 
    job_, users
WHERE
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;
-- jobs au dessus de avg(maxvmem), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.maxvmem > (
    SELECT 
        AVG(job_.maxvmem)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY users.login
    )
GROUP BY users.login ;
-- jobs en dessous de avg(maxvmem), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.maxvmem < (
    SELECT 
        AVG(job_.maxvmem)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY users.login
    )
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem inférieure à 1G (1073741824)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem < 1073741824
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem entre 1G (1073741824) et 4G (4294967296)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 1073741824
    AND job_.maxvmem < 4294967296
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem entre 4G (4294967296) et 8G (8589934592)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 4294967296
    AND job_.maxvmem < 8589934592
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem entre 8G (8589934592) et 16G (17179869184)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 8589934592
    AND job_.maxvmem < 17179869184
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem entre 16G (17179869184) et 32G (34359738368)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 17179869184
    AND job_.maxvmem < 34359738368
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem entre 32G (34359738368) et 64G (68719476736)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 34359738368
    AND job_.maxvmem < 68719476736
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem entre 64G (68719476736) et 128G (137438953472)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 68719476736
    AND job_.maxvmem < 137438953472
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, maxvmem supérieure à 128G (137438953472)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 137438953472
GROUP BY users.login ;

-- slots usage
-- max, avg, min for slots, user cmichel, 2012
SELECT
    users.login,
    MAX(job_.slots) AS max_slots,
    AVG(job_.slots) AS avg_slots,
    MIN(job_.slots) AS min_slots
FROM 
    job_, users
WHERE
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY users.login ;
-- jobs au dessus de avg(slots), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.slots > (
    SELECT 
        AVG(job_.slots)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY users.login
    )
GROUP BY users.login ;
-- jobs en dessous de avg(slots), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.slots < (
    SELECT 
        AVG(job_.slots)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY users.login
    )
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots = 1
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots = 1
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots entre 2 et 4
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 1
    AND job_.slots <= 4
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots entre 5 et 8
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 4
    AND job_.slots <= 8
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots entre 9 et 16
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 8
    AND job_.slots <= 16
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots entre 17 et 32
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 16
    AND job_.slots <= 32
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots entre 33 et 64
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 32
    AND job_.slots <= 64
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots entre 65 et 128
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 64
    AND job_.slots <= 128
GROUP BY users.login ;
-- nb jobs réussis, user cmichel, 2012, slots > 128
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 128
GROUP BY users.login ;

-- temps d'attente
-- max, avg, min de start_time - submit_time, user cmichel, 2012
SELECT users.login, 
    MAX(job_.start_time - job_.submit_time),
    AVG(job_.start_time - job_.submit_time),
    -- MIN(job_.start_time - job_.submit_time) NE devrait PAS être inférieur à 0
    CASE
        WHEN MIN(job_.start_time - job_.submit_time) < 0 THEN 0
        ELSE MIN(job_.start_time - job_.submit_time)
    END
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400 
GROUP BY users.login ;
-- jobs au dessus de avg(attente), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND (job_.start_time - job_.submit_time) > (
    SELECT 
        AVG(job_.start_time - job_.submit_time)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400 
    GROUP BY users.login 
    )
GROUP BY users.login ;
-- jobs en dessous de avg(attente), user cmichel, 2012
SELECT 
    users.login, COUNT(job_.id_job_)
FROM 
    job_, users
WHERE 
    job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND (job_.start_time - job_.submit_time) < (
    SELECT 
        AVG(job_.start_time - job_.submit_time)
    FROM 
        job_, users
    WHERE 
        job_.id_user = users.id_user
        AND users.login = 'cmichel'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400 
    GROUP BY users.login 
    )
GROUP BY users.login ;
-- jobs réussis, user cmichel, 2012, temps d'attente < 1h (3600)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) < 3600
GROUP BY users.login ;
-- jobs réussis, user cmichel, 2012, temps d'attente entre 1h (3600) et 6h (21600)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 3600
    AND (job_.start_time - job_.submit_time) < 21600
GROUP BY users.login ;
-- jobs réussis, user cmichel, 2012, temps d'attente entre 6h (21600) et 12h (43200)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 21600
    AND (job_.start_time - job_.submit_time) < 43200
GROUP BY users.login ;
-- jobs réussis, user cmichel, 2012, temps d'attente entre 12h (43200) et 24h (86400)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 43200
    AND (job_.start_time - job_.submit_time) < 86400
GROUP BY users.login ;
-- jobs réussis, user cmichel, 2012, temps d'attente > 1 jour (86400)
SELECT users.login, COUNT(job_.id_job_)
FROM job_, users
WHERE job_.id_user = users.id_user
    AND users.login = 'cmichel'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 86400
GROUP BY users.login ;

-- Top Tens
-- top ten used queues, by hours, user cmichel, 2012
SELECT 
    users.login, 
    queues.queue_name, 
    sum(job_.cpu) / 3600 AS sum_cpu 
FROM 
    users, 
    queues, 
    job_ 
WHERE 
    job_.id_user = users.id_user 
    AND users.login = 'cmichel' 
    AND job_.id_queue = queues.id_queue 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    users.login, 
    queues.queue_name 
ORDER BY 
    sum_cpu DESC 
LIMIT 10 ;
-- top ten used queues, by jobs, user cmichel, 2012
SELECT 
    users.login, 
    queues.queue_name, 
    count(job_.id_job_) AS sum_job 
FROM 
    users, 
    queues, 
    job_ 
WHERE 
    job_.id_user = users.id_user 
    AND users.login = 'cmichel' 
    AND job_.id_queue = queues.id_queue 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    users.login, 
    queues.queue_name 
ORDER BY 
    sum_job DESC 
LIMIT 10 ;
-- top ten used hosts, by hours, user cmichel, 2012
SELECT 
    users.login, 
    hosts.hostname, 
    sum(job_.cpu) / 3600 AS sum_cpu 
FROM 
    users, 
    hosts, 
    job_ 
WHERE 
    job_.id_user = users.id_user 
    AND users.login = 'cmichel' 
    AND job_.id_host = hosts.id_host 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    users.login, 
    hosts.hostname 
ORDER BY 
    sum_cpu DESC 
LIMIT 10 ;
-- top ten used hosts, by jobs, user cmichel, 2012
SELECT 
    users.login, 
    hosts.hostname, 
    count(job_.id_job_) AS sum_job 
FROM 
    users, 
    hosts, 
    job_ 
WHERE 
    job_.id_user = users.id_user 
    AND users.login = 'cmichel' 
    AND job_.id_host = hosts.id_host 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    users.login, 
    hosts.hostname 
ORDER BY 
    sum_job DESC 
LIMIT 10 ;
-- top ten maxvmem
SELECT
    users.login, 
    job_.maxvmem
FROM 
    job_, users
WHERE
    job_.id_user = users.id_user 
    AND users.login = 'cmichel' 
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    users.login, 
    job_.maxvmem
ORDER BY 
    job_.maxvmem DESC
LIMIT 10 ;
-- top ten temps d'attente (en heures)
SELECT
    users.login, 
    (job_.start_time - job_.submit_time) / 3600 AS await
FROM 
    job_, users
WHERE
    job_.id_user = users.id_user 
    AND users.login = 'cmichel' 
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    users.login, 
    await
ORDER BY 
    await DESC
LIMIT 10 ;
