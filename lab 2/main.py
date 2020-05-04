import cx_Oracle
import cred

conn = cx_Oracle.connect(cred.name, cred.passw, "localhost/XE")

cur = conn.cursor()

cur.execute("""
SELECT *
FROM (SELECT ARTIST_ID, ARTIST_NAME, COUNT(RAA.ARTWORK_ARTWORK_ID) ARTWORKS_COUNT
      FROM ARTIST
               LEFT JOIN RELATION_ARTWORK_ARTIST RAA on ARTIST.ARTIST_ID = RAA.ARTIST_ARTIST_ID
      GROUP BY ARTIST_ID, ARTIST_NAME
      ORDER BY ARTWORKS_COUNT DESC)
WHERE ROWNUM <= 10
""")
query1 = cur.fetchmany(10)
print('\nЗапит 1')
print(*list(i[0] for i in cur.description))
for row in query1:
    print(*row)

cur.execute("""
SELECT PROC_OFFICER.PROC_OFFICER_NAME, round(COUNT(RELATION_AO.ARTWORK_ARTWORK_ID)*100/all_count,2) ARTWORKS_CREDITED_COUNT
FROM PROC_OFFICER
         JOIN RELATION_AO on PROC_OFFICER.PROC_OFFICER_NAME = RELATION_AO.PROC_OFFICER_NAME
        , (select count(ARTWORK_ID) as all_count from ARTWORK)
GROUP BY PROC_OFFICER.PROC_OFFICER_NAME, all_count
ORDER BY ARTWORKS_CREDITED_COUNT DESC
    """)
print('\nЗапит 2')
query2 = cur.fetchmany(10)
print(*list(i[0] for i in cur.description))
for row in query2:
    print(*row)

cur.execute("""
SELECT ARTWORK_CREATION_YEAR, COUNT(ARTWORK_ID) NUMBER_OF_ARTWORKS
FROM ARTWORK
GROUP BY ARTWORK_CREATION_YEAR
ORDER BY ARTWORK_CREATION_YEAR
    """)
print('\nЗапит 3')
query3 = cur.fetchmany(10)
print(*list(i[0] for i in cur.description))
for row in query3:
    print(*row)

cur.close()
conn.close()