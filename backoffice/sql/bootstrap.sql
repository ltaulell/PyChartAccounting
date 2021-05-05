-- $Id$
-- bootstrap script
-- create users, database and preload data

-- createdb procedure (also system cmd)
-- createuser --no-superuser --no-createrole --createdb chartwrite
-- psql -c "ALTER USER chartwrite WITH PASSWORD 'pychart';"
CREATE ROLE chartwrite WITH PASSWORD 'pychart' LOGIN NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;
-- createdb -E UTF8 -O chartwrite accounting
CREATE DATABASE accounting WITH ENCODING 'UTF8' OWNER chartwrite ;
\c accounting
-- chartread user
CREATE ROLE chartread WITH PASSWORD 'pychart' LOGIN NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
GRANT CONNECT ON DATABASE accounting TO chartread;
GRANT USAGE ON SCHEMA public TO chartread;
GRANT SELECT ON ALL TABLES IN SCHEMA public to chartread;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO chartread;
-- update pg_hab.conf
-- psql -c "CREATE EXTENSION adminpack;" accounting
CREATE EXTENSION adminpack;
-- apt-get install postgresql-plpython3-11
-- psql -c "CREATE EXTENSION plpython3u;" accounting
CREATE EXTENSION plpython3u;

-- execute bdd.sql

-- insert metagroupes data
create table IF NOT EXISTS metagroupes (
    id_metagroupe bigserial PRIMARY KEY,
    meta_name varchar(255) NOT NULL UNIQUE
    );

INSERT INTO metagroupes(meta_name) VALUES ('autres_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('chimie_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('chimie_UdL') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('bio_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('physique_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('cral_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('partenaires_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('geol_ENS') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('lmfa_ECL') RETURNING id_metagroupe;
INSERT INTO metagroupes(meta_name) VALUES ('lip_ENS') RETURNING id_metagroupe;
-- INSERT INTO metagroupes(meta_name) VALUES ('') RETURNING id_metagroupe;

-- insert clusters data
create table IF NOT EXISTS clusters (
    id_cluster bigserial PRIMARY KEY,
    cluster_name varchar(255) NOT NULL UNIQUE
    );

INSERT INTO clusters(cluster_name) VALUES ('default') RETURNING id_cluster;
INSERT INTO clusters(cluster_name) VALUES ('X5') RETURNING id_cluster;
INSERT INTO clusters(cluster_name) VALUES ('E5') RETURNING id_cluster;
INSERT INTO clusters(cluster_name) VALUES ('Lake') RETURNING id_cluster;
INSERT INTO clusters(cluster_name) VALUES ('Epyc') RETURNING id_cluster;
-- INSERT INTO clusters(cluster_name) VALUES ('') RETURNING id_cluster;

-- table 'history'
CREATE TABLE IF NOT EXISTS history (
    id_insertion bigserial PRIMARY KEY,
    last_offset_position bigint NOT NULL,
    date_insert timestamp without time zone NOT NULL
    );

INSERT INTO history(last_offset_position, date_insert) VALUES ('0', current_timestamp) RETURNING id_insertion;
