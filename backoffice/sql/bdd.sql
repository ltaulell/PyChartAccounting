-- $Id$
-- create proper schema
create table IF NOT EXISTS users (
    id_user bigserial PRIMARY KEY,
    login varchar(255) NOT NULL UNIQUE
    );

create table IF NOT EXISTS hosts (
    id_host bigserial PRIMARY KEY,
    hostname varchar(255) NOT NULL UNIQUE
    );

create table IF NOT EXISTS groupes (
    id_groupe bigserial PRIMARY KEY,
    group_name varchar(255) NOT NULL UNIQUE
    );

create table IF NOT EXISTS queues (
    id_queue bigserial PRIMARY KEY,
    queue_name  varchar(255) NOT NULL UNIQUE
    );

-- added tables
create table IF NOT EXISTS metagroupes (
    id_metagroupe bigserial PRIMARY KEY,
    meta_name varchar(255) NOT NULL UNIQUE
    );

create table IF NOT EXISTS clusters (
    id_cluster bigserial PRIMARY KEY,
    cluster_name varchar(255) NOT NULL UNIQUE
    );

-- liaison users/groupes
create table IF NOT EXISTS users_in_groupes (
    id_groupe bigint NOT NULL,
    id_user bigint NOT NULL,
    PRIMARY KEY (id_groupe, id_user),
    FOREIGN KEY (id_groupe) REFERENCES groupes (id_groupe),
    FOREIGN KEY (id_user) REFERENCES users (id_user)
    );

-- liaison hosts/queues
create table IF NOT EXISTS hosts_in_queues (
    id_queue bigint NOT NULL,
    id_host bigint NOT NULL,
    PRIMARY KEY (id_queue, id_host),
    FOREIGN KEY (id_queue) REFERENCES queues (id_queue),
    FOREIGN KEY (id_host) REFERENCES hosts (id_host)
    );

-- liaison hosts/clusters
create table IF NOT EXISTS hosts_in_clusters (
    id_cluster bigint NOT NULL,
    id_host bigint NOT NULL,
    PRIMARY KEY (id_cluster, id_host),
    FOREIGN KEY (id_cluster) REFERENCES clusters (id_cluster),
    FOREIGN KEY (id_host) REFERENCES hosts (id_host)
    );

-- liaison groupes/metagroupes
create table IF NOT EXISTS groupes_in_metagroupes (
    id_metagroupe bigint NOT NULL,
    id_groupe bigint NOT NULL,
    PRIMARY KEY (id_metagroupe, id_groupe),
    FOREIGN KEY (id_metagroupe) REFERENCES metagroupes (id_metagroupe),
    FOREIGN KEY (id_groupe) REFERENCES groupes (id_groupe)
    );

-- liaison users/metagroupes
create table IF NOT EXISTS users_in_metagroupes (
    id_metagroupe bigint NOT NULL,
    id_user bigint NOT NULL,
    PRIMARY KEY (id_metagroupe, id_user),
    FOREIGN KEY (id_metagroupe) REFERENCES metagroupes (id_metagroupe),
    FOREIGN KEY (id_user) REFERENCES users (id_user)
    );

-- table centrale
create table IF NOT EXISTS job_ (
    id_job_ bigserial NOT NULL,
    id_queue bigint NOT NULL,
    id_host bigint NOT NULL,
    id_groupe bigint NOT NULL,
    id_user bigint NOT NULL,
    FOREIGN KEY (id_queue) REFERENCES queues (id_queue),
    FOREIGN KEY (id_host) REFERENCES hosts (id_host),
    FOREIGN KEY (id_groupe) REFERENCES groupes (id_groupe),
    FOREIGN KEY (id_user) REFERENCES users (id_user),
    job_name varchar(255),
    job_id integer NOT NULL,
    submit_time bigint NOT NULL,
    start_time bigint NOT NULL,
    end_time bigint NOT NULL,
    failed integer,
    exit_status integer,
    ru_wallclock real,
    ru_utime real,
    ru_stime real,
    project varchar(255),
    slots integer,
    cpu real,
    mem real,
    io real,
    maxvmem real,
    PRIMARY KEY (id_queue, id_host, id_user, job_id, start_time, end_time)
    );

-- table 'history'
CREATE TABLE IF NOT EXISTS history (
    id_insertion bigserial PRIMARY KEY,
    last_offset_position bigint NOT NULL,
    date_insert timestamp without time zone NOT NULL
    );
