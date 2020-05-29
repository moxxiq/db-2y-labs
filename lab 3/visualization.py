import cx_Oracle
import numpy as np
import cred
from sys import argv

import chart_studio
import plotly.graph_objects as go
import plotly.io as pio
import chart_studio.plotly as py



chart_studio.tools.set_credentials_file(username=cred.username, api_key=cred.api_key)
conn = cx_Oracle.connect(cred.name, cred.passw, "localhost/XE")

cur = conn.cursor()


# Запит №1: Вивести 10 авторів з найбільшою кількістю робіт та кількість робіт кожного з цих авторів.
# Візуалізація: стовпчикова діаграма.

cur.execute("""
SELECT *
FROM (SELECT ARTIST_ID, ARTIST_NAME, COUNT(RAA.ARTWORK_ARTWORK_ID) ARTWORKS_COUNT
      FROM ARTIST
               LEFT JOIN RELATION_ARTWORK_ARTIST RAA on ARTIST.ARTIST_ID = RAA.ARTIST_ARTIST_ID
      GROUP BY ARTIST_ID, ARTIST_NAME
      ORDER BY ARTWORKS_COUNT DESC)
WHERE ROWNUM <= 10
""")
query1 = np.array(cur.fetchmany(10))
data1 = [go.Bar(
            x=query1[:,1],
            y=query1[:,2]
    )]
layout1 = go.Layout(
    title='10 авторів з найбільшою кількістю робіт',
    xaxis=dict(
        title='Автори'
    ),
    yaxis=dict(
        title='Кількість робіт',
        rangemode='nonnegative',
        autorange=True
    )
)
fig1 = go.Figure(data=data1, layout=layout1)
print('\nЗапит 1 - виконано')


# Запит №2: Вивести постачальників робіт музею у відсотковому співвідношенні відповідно до кількості робіт, які вони передали музею.
# Візуалізація: секторна діаграма

# ATTENTION: IT DIFFER FROM OTHER QUERIES CAUSE OF INFORMATIVE CHART
cur.execute("""
SELECT PROC_OFFICER.PROC_OFFICER_NAME, COUNT(RELATION_AO.ARTWORK_ARTWORK_ID) ARTWORKS_CREDITED_COUNT
FROM PROC_OFFICER
         JOIN RELATION_AO on PROC_OFFICER.PROC_OFFICER_NAME = RELATION_AO.PROC_OFFICER_NAME
GROUP BY PROC_OFFICER.PROC_OFFICER_NAME
ORDER BY ARTWORKS_CREDITED_COUNT DESC
    """)
query2 = np.array(cur.fetchall())
# create Others value
# others percent
others_pc = 25
query_accum = np.add.accumulate(np.asarray(query2[:,1], dtype=int))
#number from which it will be in Others
others_number = np.argmax(query_accum >(100-others_pc)/100.0*query_accum[-1])
pie = go.Pie(labels=np.append(query2[:others_number-1,0],'Others'), values=np.append(query2[:others_number-1,1], query_accum[-1]-query_accum[others_number-1]), direction='clockwise', sort=False)
fig2 = go.Figure(data=pie)
fig2.update_layout(title_text='Постачальники робіт музею')
print('Запит 2 - виконано')


# Запит №3: Вивести динаміку кількості робіт по роках.
# Візуалізація: графік залежності

cur.execute("""
SELECT ARTWORK_CREATION_YEAR, COUNT(ARTWORK_ID) NUMBER_OF_ARTWORKS
FROM ARTWORK
GROUP BY ARTWORK_CREATION_YEAR
ORDER BY ARTWORK_CREATION_YEAR
    """)

print('Запит 3 - виконано')
query3 = np.array(cur.fetchall())
scatter = go.Scatter(
    x=query3[:,0],
    y=query3[:,1],
    mode='lines+markers'
)
fig3 = go.Figure(data=scatter)
fig3.update_layout(title_text='Кількість завершених робіт по роках')


cur.close()
conn.close()


filename1 = 'workly-artists'
filename2 = 'artworks-aucqisitors'
filename3 = 'art_per_year'
if len(argv) > 1 and argv[1] == 'offline':
    pio.write_html(fig1, file=filename1+'.html', auto_open=False)
    pio.write_html(fig2, file=filename2+'.html', auto_open=False)
    pio.write_html(fig3, file=filename3+'.html', auto_open=False)
else:
    links = py.plot(fig1, filename = filename1), py.plot(fig2, filename = filename2), py.plot(fig3, filename = filename3)
    ###---###---###---###---###---###---###---###---###---###---###---
    ###---DEPRECATED DASHBOARD FROM AMIS, DO NOT TOUCH
    import chart_studio.dashboard_objs as dashboard
    import re
    def fileId_from_url(url):
        """Return fileId from a url."""
        raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1: ]
        return raw_fileId.replace('/', ':')

    ids = list(map(fileId_from_url,links))
    my_dboard = dashboard.Dashboard()

    box_1 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': ids[0],
        'title': '10 авторів з найбільшою кількістю робіт.L3'
    }
    box_2 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': ids[1],
        'title': 'Постачальники робіт музею.L3'
    }
    box_3 = {
        'type': 'box',
        'boxType': 'plot',
        'fileId': ids[2],
        'title': 'Кількість завершених робіт по роках.L3'
    }
     
    my_dboard.insert(box_1)
    my_dboard.insert(box_2, 'below', 1)
    my_dboard.insert(box_3, 'left', 2)

    py.dashboard_ops.upload(my_dboard, 'Lab 3 Dashboard')
    ###---###---###---###---###---###---###---###---###---###---###---
