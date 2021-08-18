--
-- proper SQL, for database queries
--
-- fixed example:
-- groupe = chimie,
-- year = 2012 (in epoch, 01-01-2012, 01-01-2013)
--

-- combo (nb jobs réussi, nb jobs plantés) -> taux de réussite
-- nb de jobs réussis, nb heures consommées d'un groupe (chimie, 2012)
SELECT groupes.group_name, COUNT(job_.id_job_), SUM(job_.cpu) AS sum_cpu
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY groupes.id_groupe ;
-- nb de jobs plantés d'un groupe (chimie, 2012)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.failed != 0
    AND job_.exit_status != 0
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY groupes.id_groupe ;

-- execution time
-- min, avg, max for ru_wallclock, groupe chimie, 2012
SELECT 
    groupes.group_name, 
    MIN(job_.ru_wallclock),
    AVG(job_.ru_wallclock),
    MAX(job_.ru_wallclock)::INTEGER
    -- cast pour forcer la sortie (exemple)
FROM 
    job_, groupes 
WHERE job_.id_groupe = groupes.id_groupe 
    AND groupes.group_name = 'chimie' 
    AND job_.start_time >= 1325376000 
    AND job_.start_time <= 1356998400 
GROUP BY groupes.group_name ;
-- au dessus de avg, groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.ru_wallclock > (
    SELECT 
        AVG(job_.ru_wallclock)
    FROM 
        job_, groupes
    WHERE 
        job_.id_groupe = groupes.id_groupe
        AND groupes.group_name = 'chimie'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY groupes.group_name
    )
GROUP BY groupes.group_name ;
-- en dessous de avg, groupe chimie, 2012
SELECT 
    groupes.group_name, COUNT(job_.id_job_)
FROM 
    job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.ru_wallclock < (
    SELECT 
        AVG(job_.ru_wallclock)
    FROM 
        job_, groupes
    WHERE 
        job_.id_groupe = groupes.id_groupe
        AND groupes.group_name = 'chimie'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY groupes.group_name
    )
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, durée inférieure à 1 jour (86400)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock < 86400
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, durée entre 1 jour (86400) et 1 week (604800)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 86400
    AND job_.ru_wallclock < 604800
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, durée entre 1 week (604800) et 1 mois (18144000)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 604800
    AND job_.ru_wallclock < 18144000
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, durée supérieure à 1 mois (18144000)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 18144000
GROUP BY groupes.group_name ;

-- memory usage (1Gi, 4, 8, 16, 32, 64, 128+)
SELECT
    groupes.group_name,
    MAX(job_.maxvmem)::INTEGER AS max_mem,
    AVG(job_.maxvmem) AS avg_mem,
    MIN(job_.maxvmem) AS min_mem
FROM 
    job_, groupes
WHERE
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY groupes.group_name ;
-- jobs au dessus de avg(maxvmem), groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > (
        SELECT AVG(job_.maxvmem)
        FROM job_, groupes
        WHERE
            job_.id_groupe = groupes.id_groupe
            AND groupes.group_name = 'chimie'
            AND (job_.failed = 0 OR job_.exit_status = 0)
            AND job_.start_time >= 1325376000
            AND job_.start_time <= 1356998400
        GROUP BY groupes.group_name
        )
GROUP BY groupes.group_name ;
-- jobs en dessous de avg(maxvmem), groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem < (
        SELECT AVG(job_.maxvmem)
        FROM job_, groupes
        WHERE
            job_.id_groupe = groupes.id_groupe
            AND groupes.group_name = 'chimie'
            AND (job_.failed = 0 OR job_.exit_status = 0)
            AND job_.start_time >= 1325376000
            AND job_.start_time <= 1356998400
        GROUP BY groupes.group_name
        )
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem inférieure à 1G (1073741824)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem < 1073741824
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem entre 1G (1073741824) et 4G (4294967296)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 1073741824
    AND job_.maxvmem < 4294967296
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem entre 4G (4294967296) et 8G (8589934592)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 4294967296
    AND job_.maxvmem < 8589934592
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem entre 8G (8589934592) et 16G (17179869184)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 8589934592
    AND job_.maxvmem < 17179869184
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem entre 16G (17179869184) et 32G (34359738368)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 17179869184
    AND job_.maxvmem < 34359738368
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem entre 32G (34359738368) et 64G (68719476736)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 34359738368
    AND job_.maxvmem < 68719476736
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem entre 64G (68719476736) et 128G (137438953472)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 68719476736
    AND job_.maxvmem < 137438953472
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, maxvmem supérieure à 128G (137438953472)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.maxvmem > 137438953472
GROUP BY groupes.group_name ;

-- slots usage (1, 2-4, 5-8, 9-16, 17-32, 33-64, 65-128, 128+)
-- min, avg, max for slots, groupe chimie, 2012
SELECT 
    groupes.group_name, 
    MIN(job_.slots),
    AVG(job_.slots),
    MAX(job_.slots)
FROM 
    job_, groupes 
WHERE 
    job_.id_groupe = groupes.id_groupe 
    AND groupes.group_name = 'chimie' 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000 
    AND job_.start_time <= 1356998400 
GROUP BY groupes.group_name ;
-- jobs au dessus de avg(slots), groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > (
        SELECT AVG(job_.slots)
        FROM job_, groupes
        WHERE job_.id_groupe = groupes.id_groupe 
            AND groupes.group_name = 'chimie' 
            AND (job_.failed = 0 OR job_.exit_status = 0)
            AND job_.start_time >= 1325376000 
            AND job_.start_time <= 1356998400 
        GROUP BY groupes.group_name
        )
GROUP BY groupes.group_name ;
-- jobs en dessous de avg(slots), groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots < (
        SELECT AVG(job_.slots)
        FROM job_, groupes
        WHERE job_.id_groupe = groupes.id_groupe 
            AND groupes.group_name = 'chimie' 
            AND (job_.failed = 0 OR job_.exit_status = 0)
            AND job_.start_time >= 1325376000 
            AND job_.start_time <= 1356998400 
        GROUP BY groupes.group_name
        )
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots = 1
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots = 1
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots entre 2 et 4
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 1
    AND job_.slots <= 4
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots entre 5 et 8
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 5
    AND job_.slots <= 8
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots entre 9 et 16
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 9
    AND job_.slots <= 16
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots entre 17 et 32
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 17
    AND job_.slots <= 32
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots entre 33 et 64
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 33
    AND job_.slots <= 64
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots entre 65 et 128
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 65
    AND job_.slots <= 128
GROUP BY groupes.group_name ;
-- nb jobs réussis, groupe chimie, 2012, slots > 128
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.slots > 128
GROUP BY groupes.group_name ;

-- temps d'attente (1h, 6h, 12h, 24h -> 1j+)
-- min, avg, max for attente (start_time - submit_time), groupe chimie, 2012
SELECT 
    groupes.group_name,
    MAX(job_.start_time - job_.submit_time),
    AVG(job_.start_time - job_.submit_time),
    CASE
        WHEN MIN(job_.start_time - job_.submit_time) < 0 THEN 0
        ELSE MIN(job_.start_time - job_.submit_time)
    END
FROM 
    job_, groupes 
WHERE 
    job_.id_groupe = groupes.id_groupe 
    AND groupes.group_name = 'chimie' 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000 
    AND job_.start_time <= 1356998400 
GROUP BY groupes.group_name ;
-- jobs au dessus de avg(attente), groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > (
        SELECT 
            AVG(job_.start_time - job_.submit_time)
        FROM job_, groupes
        WHERE
            job_.id_groupe = groupes.id_groupe
            AND groupes.group_name = 'chimie'
            AND (job_.failed = 0 OR job_.exit_status = 0)
            AND job_.start_time >= 1325376000
            AND job_.start_time <= 1356998400
        GROUP BY groupes.group_name
        )
GROUP BY groupes.group_name ;
-- jobs en dessous de avg(attente), groupe chimie, 2012
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) < (
        SELECT 
            AVG(job_.start_time - job_.submit_time)
        FROM job_, groupes
        WHERE
            job_.id_groupe = groupes.id_groupe
            AND groupes.group_name = 'chimie'
            AND (job_.failed = 0 OR job_.exit_status = 0)
            AND job_.start_time >= 1325376000
            AND job_.start_time <= 1356998400
        GROUP BY groupes.group_name
        )
GROUP BY groupes.group_name ;
-- jobs, groupe chimie, 2012, temps d'attente < 1h (3600)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) < 3600
GROUP BY groupes.group_name ;
-- jobs, groupe chimie, 2012, temps d'attente entre 1h (3600) et 6h (21600)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 3600
    AND (job_.start_time - job_.submit_time) < 21600
GROUP BY groupes.group_name ;
-- jobs, groupe chimie, 2012, temps d'attente entre 6h (21600) et 12h (43200)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 21600
    AND (job_.start_time - job_.submit_time) < 43200
GROUP BY groupes.group_name ;
-- jobs, groupe chimie, 2012, temps d'attente entre 12h (43200) et 24h (86400)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 43200
    AND (job_.start_time - job_.submit_time) < 86400
GROUP BY groupes.group_name ;
-- jobs, groupe chimie, 2012, temps d'attente > 1 jour (86400)
SELECT groupes.group_name, COUNT(job_.id_job_)
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND (job_.start_time - job_.submit_time) > 86400
GROUP BY groupes.group_name ;

-- TODO
-- Tops Tens
-- top ten users, by hours, groupe chimie, 2012

-- top ten users, by jobs,  groupe chimie, 2012

-- top ten used queues, by hours, groupe chimie, 2012
SELECT 
    groupes.group_name, 
    queues.queue_name, 
    sum(job_.cpu) / 3600 AS sum_cpu 
FROM 
    groupes, 
    queues, 
    job_ 
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.id_queue = queues.id_queue 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    groupes.group_name, 
    queues.queue_name 
ORDER BY 
    sum_cpu DESC 
LIMIT 10 ;
-- top ten used queues, by jobs, groupe chimie, 2012
SELECT 
    groupes.group_name, 
    queues.queue_name, 
    count(job_.id_job_) AS sum_job 
FROM 
    groupes, 
    queues, 
    job_ 
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.id_queue = queues.id_queue 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    groupes.group_name, 
    queues.queue_name 
ORDER BY 
    sum_job DESC 
LIMIT 10 ;
-- top ten used queues, by hours, groupe chimie, 2012
SELECT 
    groupes.group_name, 
    hosts.hostname, 
    sum(job_.cpu) / 3600 AS sum_cpu 
FROM 
    groupes, 
    hosts, 
    job_ 
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.id_host = hosts.id_host 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    groupes.group_name, 
    hosts.hostname 
ORDER BY 
    sum_cpu DESC 
LIMIT 10 ;
-- top ten used queues, by jobs, groupe chimie, 2012
SELECT 
    groupes.group_name, 
    hosts.hostname, 
    count(job_.id_job_) AS sum_job 
FROM 
    groupes, 
    hosts, 
    job_ 
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND job_.id_host = hosts.id_host 
    AND (job_.failed = 0 OR job_.exit_status = 0) 
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    groupes.group_name, 
    hosts.hostname 
ORDER BY 
    sum_job DESC 
LIMIT 10 ;
-- top ten maxvmem
SELECT 
    groupes.group_name, 
    job_.maxvmem
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    groupes.group_name, 
    job_.maxvmem 
ORDER BY 
    job_.maxvmem DESC
LIMIT 10 ;
-- top ten temps d'attente (en heures)
SELECT 
    groupes.group_name, 
    (job_.start_time - job_.submit_time) / 3600 AS await
FROM job_, groupes
WHERE 
    job_.id_groupe = groupes.id_groupe
    AND groupes.group_name = 'chimie'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY 
    groupes.group_name, 
    await 
ORDER BY 
    await DESC
LIMIT 10 ;

