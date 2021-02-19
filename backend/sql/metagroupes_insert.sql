-- $Id$
-- insert metagroupes data

-- create table IF NOT EXISTS metagroupes (
--    id_metagroupe bigserial PRIMARY KEY,
--    meta_name varchar(255) NOT NULL UNIQUE
--    );

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
