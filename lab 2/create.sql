CREATE TABLE artist (
    artist_id    INTEGER NOT NULL,
    artist_name  VARCHAR2(400)
);

ALTER TABLE artist ADD CONSTRAINT artist_pk PRIMARY KEY ( artist_id );

CREATE TABLE artwork (
    artwork_id             INTEGER NOT NULL,
    artwork_title          VARCHAR2(400) NOT NULL,
    artwork_creation_year  INTEGER,
    acqusition_date        DATE,
    proc_officer_name      VARCHAR2(700) NOT NULL
);

ALTER TABLE artwork ADD CONSTRAINT artwork_pk PRIMARY KEY ( artwork_id );

CREATE TABLE proc_officer (
    proc_officer_name VARCHAR2(700) NOT NULL
);

ALTER TABLE proc_officer ADD CONSTRAINT proc_officer_pk PRIMARY KEY ( proc_officer_name );

CREATE TABLE relation_ao (
    proc_officer_name   VARCHAR2(700) NOT NULL,
    artwork_artwork_id  INTEGER NOT NULL
);

ALTER TABLE relation_ao ADD CONSTRAINT relation_artwork_officer_pk PRIMARY KEY ( proc_officer_name,
                                                                                 artwork_artwork_id );

CREATE TABLE relation_artwork_artist (
    artwork_artwork_id  INTEGER NOT NULL,
    artist_artist_id    INTEGER NOT NULL
);

ALTER TABLE relation_artwork_artist ADD CONSTRAINT relation_1_pk PRIMARY KEY ( artwork_artwork_id,
                                                                               artist_artist_id );

ALTER TABLE relation_artwork_artist
    ADD CONSTRAINT relation_1_artist_fk FOREIGN KEY ( artist_artist_id )
        REFERENCES artist ( artist_id );

ALTER TABLE relation_artwork_artist
    ADD CONSTRAINT relation_1_artwork_fk FOREIGN KEY ( artwork_artwork_id )
        REFERENCES artwork ( artwork_id );

ALTER TABLE relation_ao
    ADD CONSTRAINT relation_ao_fk FOREIGN KEY ( artwork_artwork_id )
        REFERENCES artwork ( artwork_id );

ALTER TABLE relation_ao
    ADD CONSTRAINT relation_po_fk FOREIGN KEY ( proc_officer_name )
        REFERENCES proc_officer ( proc_officer_name );
commit;