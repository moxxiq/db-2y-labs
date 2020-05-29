import csv
import cx_Oracle
import cred

conn = cx_Oracle.connect(cred.name, cred.passw, "localhost/XE")
cur = conn.cursor()

tables = ["ARTIST","PROC_OFFICER","ARTWORK","RELATION_ARTWORK_ARTIST","RELATION_AO"]

for t in tables:
    with open(t + '.csv', 'w', newline='\n') as file:
        cur.execute(f"""
        SELECT *
        FROM {t}
        """)
        row = cur.fetchone()
        writer = csv.writer(file)
        writer.writerow(tuple(map(lambda i: i[0], cur.description)))

        while row:
            writer.writerow(row)
            row = cur.fetchone()


cur.close()
conn.close()