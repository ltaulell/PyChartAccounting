-- $Id$
-- bootstrap

-- table 'history'
CREATE TABLE IF NOT EXISTS history (
    id_insertion bigserial PRIMARY KEY,
    last_offset_position bigint NOT NULL,
    date_insert timestamp without time zone NOT NULL
    );

INSERT INTO history(last_offset_position, date_insert) VALUES ('0', current_timestamp) RETURNING id_insertion;
