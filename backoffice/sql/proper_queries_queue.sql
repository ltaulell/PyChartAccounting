--
-- proper SQL, for database queries
--
-- fixed example:
-- queue = r815lin128ib OR all
-- year = 2012 (in epoch, 01-01-2012, 01-01-2013), OR all
--

-- top ten queues by max cpu usage, 2012
SELECT
    queues.queue_name,
    max(job_.cpu) as max_cpu
FROM 
    job_, queues
WHERE
    job_.id_queue = queues.id_queue
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY queues.queue_name
ORDER BY max_cpu DESC
LIMIT 10;

-- max, avg, min for ru_wallclock, queue r815lin128ib, 2012
SELECT
    queues.queue_name,
    MAX(job_.ru_wallclock) AS max_wall,
    AVG(job_.ru_wallclock) AS avg_wall,
    MIN(job_.ru_wallclock) AS min_wall
FROM 
    job_, queues
WHERE
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY queues.queue_name ;

-- nb jobs réussis, queue r815lin128ib, 2012
SELECT
    queues.queue_name,
    COUNT(job_.id_job_)
FROM 
    job_, queues
WHERE
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY queues.queue_name ;
-- nb jobs failed, queue r815lin128ib, 2012
SELECT
    queues.queue_name,
    COUNT(job_.id_job_)
FROM 
    job_, queues
WHERE
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND job_.failed != 0
    AND job_.exit_status != 0
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY queues.queue_name ;
-- total jobs, queue r815lin128ib, 2012 (vérification, nograph)
SELECT
    queues.queue_name,
    COUNT(job_.id_job_)
FROM 
    job_, queues
WHERE
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
GROUP BY queues.queue_name ;

-- au dessus de avg
SELECT 
    queues.queue_name, COUNT(job_.id_job_)
FROM
    job_, queues
WHERE 
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.ru_wallclock > (
    SELECT 
        AVG(job_.ru_wallclock)
    FROM 
        job_, queues
    WHERE 
        job_.id_queue = queues.id_queue
        AND queues.queue_name = 'r815lin128ib'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY queues.queue_name
    )
GROUP BY queues.queue_name ;
-- en dessous de avg
SELECT
    queues.queue_name, COUNT(job_.id_job_)
FROM
    job_, queues
WHERE
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    -- avg donné par requête imbriquée
    AND job_.ru_wallclock < (
    SELECT
        AVG(job_.ru_wallclock)
    FROM
        job_, queues
    WHERE
        job_.id_queue = queues.id_queue
        AND queues.queue_name = 'r815lin128ib'
        AND (job_.failed = 0 OR job_.exit_status = 0)
        AND job_.start_time >= 1325376000
        AND job_.start_time <= 1356998400
    GROUP BY queues.queue_name
    )
GROUP BY queues.queue_name ;

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
-- same-same (même plan d'execution au final)
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
-- nb jobs réussis, queue r815lin128ib, 2012, durée entre 1 jour (86400) et 1 week (604800)
SELECT queues.queue_name,
    COUNT(job_.id_job_)
FROM job_, queues
WHERE 
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 86400
    AND job_.ru_wallclock < 604800
GROUP BY queues.queue_name ;
-- nb jobs réussis, queue r815lin128ib, 2012, durée entre 1 week (604800) et 1 mois (18144000)
SELECT queues.queue_name,
    COUNT(job_.id_job_)
FROM job_, queues
WHERE 
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 604800
    AND job_.ru_wallclock < 18144000
GROUP BY queues.queue_name ;
-- nb jobs réussis, queue r815lin128ib, 2012, durée supérieure à 1 mois (18144000)
SELECT queues.queue_name,
    COUNT(job_.id_job_)
FROM job_, queues
WHERE 
    job_.id_queue = queues.id_queue
    AND queues.queue_name = 'r815lin128ib'
    AND (job_.failed = 0 OR job_.exit_status = 0)
    AND job_.start_time >= 1325376000
    AND job_.start_time <= 1356998400
    AND job_.ru_wallclock > 18144000
GROUP BY queues.queue_name ;

