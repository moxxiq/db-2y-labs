-- Запит №1: Вивести 10 авторів з найбільшою кількістю робіт та кількість робіт кожного з цих авторів.
-- Візуалізація: стовпчикова діаграма.
SELECT *
FROM (SELECT ARTIST_ID, ARTIST_NAME, COUNT(RAA.ARTWORK_ARTWORK_ID) ARTWORKS_COUNT
      FROM ARTIST
               LEFT JOIN RELATION_ARTWORK_ARTIST RAA on ARTIST.ARTIST_ID = RAA.ARTIST_ARTIST_ID
      GROUP BY ARTIST_ID, ARTIST_NAME
      ORDER BY ARTWORKS_COUNT DESC)
WHERE ROWNUM <= 10;
-- Oracle 11g does not support 'FETCH FIRST 10 ROWS ONLY' syntax

-- Запит №2: Вивести постачальників робіт музею у відсотковому співвідношенні відповідно до кількості робіт, які вони передали музею.
-- Візуалізація: секторна діаграма
SELECT PROC_OFFICER.PROC_OFFICER_NAME, round(COUNT(RELATION_AO.ARTWORK_ARTWORK_ID)*100/all_count,2) || '%' ARTWORKS_CREDITED_COUNT
FROM PROC_OFFICER
         JOIN RELATION_AO on PROC_OFFICER.PROC_OFFICER_NAME = RELATION_AO.PROC_OFFICER_NAME
        , (select count(ARTWORK_ID) as all_count from ARTWORK)
GROUP BY PROC_OFFICER.PROC_OFFICER_NAME, all_count
ORDER BY ARTWORKS_CREDITED_COUNT DESC;


-- Запит №3: Вивести динаміку кількості робіт по роках.
-- Візуалізація: графік залежності
SELECT ARTWORK_CREATION_YEAR, COUNT(ARTWORK_ID) NUMBER_OF_ARTWORKS
FROM ARTWORK
GROUP BY ARTWORK_CREATION_YEAR
ORDER BY ARTWORK_CREATION_YEAR;