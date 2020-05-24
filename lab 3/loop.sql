DECLARE
    i_artist_id   ARTIST.ARTIST_ID%TYPE;
    i_artist_name ARTIST.ARTIST_NAME%TYPE;

BEGIN
    i_artist_id := 70000;
    i_artist_name := 'Olaf';
    FOR counter IN 1..10
        LOOP
            INSERT INTO ARTIST(ARTIST_ID, ARTIST_NAME)
            VALUES (counter + i_artist_id, i_artist_name || counter);
        END LOOP;
END;