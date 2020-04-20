CREATE TABLE artist (
    artist_id  INTEGER NOT NULL,
    name       VARCHAR2(254)
)
LOGGING;

ALTER TABLE artist ADD CONSTRAINT artist_pk PRIMARY KEY ( artist_id );

CREATE TABLE artist_artwork (
    artwork_id  INTEGER NOT NULL,
    artist_id   INTEGER NOT NULL
)

logging;

CREATE TABLE artwork (
    artwork_id        INTEGER NOT NULL,
    auquisitor        VARCHAR2(254) NOT NULL,
    creation_date     VARCHAR2(16) NOT NULL,
    acquisition_date  DATE
)

logging;

ALTER TABLE artwork ADD CONSTRAINT artwork_pk PRIMARY KEY ( artwork_id );

CREATE TABLE creation_time (
    creation_date VARCHAR2(16) NOT NULL
)

logging;

ALTER TABLE creation_time ADD CONSTRAINT creation_time_pk PRIMARY KEY ( creation_date );

CREATE TABLE purchase (
    acquisitor VARCHAR2(254) NOT NULL
)

logging;

ALTER TABLE purchase ADD CONSTRAINT purchase_pk PRIMARY KEY ( acquisitor );

ALTER TABLE artist_artwork
    ADD CONSTRAINT artist_artwork_artist_fk FOREIGN KEY ( artist_id )
        REFERENCES artist ( artist_id )
    NOT DEFERRABLE;

ALTER TABLE artist_artwork
    ADD CONSTRAINT artist_artwork_artwork_fk FOREIGN KEY ( artwork_id )
        REFERENCES artwork ( artwork_id )
    NOT DEFERRABLE;

ALTER TABLE artwork
    ADD CONSTRAINT artwork_creation_time_fk FOREIGN KEY ( creation_date )
        REFERENCES creation_time ( creation_date )
    NOT DEFERRABLE;

ALTER TABLE artwork
    ADD CONSTRAINT artwork_purchase_fk FOREIGN KEY ( auquisitor )
        REFERENCES purchase ( acquisitor )
    NOT DEFERRABLE;

CREATE SEQUENCE artist_artist_id_seq START WITH 1 NOCACHE ORDER;

commit;
--CREATE OR REPLACE TRIGGER artist_artist_id_trg BEFORE
--    INSERT ON artist
--    FOR EACH ROW
--    WHEN ( new.artist_id IS NULL )
--BEGIN
--    :new.artist_id := artist_artist_id_seq.nextval;
--END;
