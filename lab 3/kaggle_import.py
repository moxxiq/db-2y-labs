import pandas as pd
import numpy as np
import os.path
import cx_Oracle
import chart_studio
import plotly.graph_objects as go
import plotly.io as pio
import chart_studio.plotly as py
import cred


chart_studio.tools.set_credentials_file(username=cred.username, api_key=cred.api_key)

# Check if File Exists
FILENAME = "dataset/artworks.csv"
if not os.path.isfile(FILENAME):
    print ("File does not exist")
    exit()
# raed file
artworks_df = pd.read_csv(FILENAME)
# remove limitations
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

artworks_df = artworks_df.head(500)
'''TODO:
make requirements.txt
'''
# print(artworks_df[["Artwork ID", "Title", "Artist ID", "Name", "Date", "Acquisition Date", "Credit"]].head(30).to_string(index=False))

# remove unnecessary columns 
# artworks_df.drop(["Name","Medium", "Dimensions", "Catalogue", "Department", "Classification", "Object Number", "Diameter (cm)", "Circumference (cm)", "Height (cm)", "Length (cm)", "Width (cm)", "Depth (cm)", "Weight (kg)", "Duration (s)"],
#                  axis=1,
#                  inplace=True)
artworks_df=artworks_df[["Artwork ID", "Title", "Artist ID", "Name", "Date", "Acquisition Date", "Credit"]]

# split artist into the new table
artists_df = artworks_df[['Artist ID', 'Name']]
artworks_df.drop(["Name"],
                 axis=1,
                 inplace=True)


# get only title of the artwork
artworks_df['Title'] = artworks_df['Title'].apply(
    lambda t: str(t).split(',')[0])

# fix year numbers '19(56)-57' -> '1957'
artworks_df['Date'] = artworks_df.Date.str.replace(r'.*(\(?\d{2}\)?\d{2})(s?[-–/]\d{2,4})?.*', 
    lambda s: str(s.group(1)[:2])+str(s.group(2)[-2:]) if s.group(2) else s.group(1), regex=True)


# arts with unknown year get 'Unknown' year
artworks_df['Date'] = artworks_df['Date'].fillna('Unknown')
artworks_df.loc[~artworks_df['Date'].str.contains(r'\d{4}', regex=True), 'Date'] = 'Unknown'

# replace NaN artist ids with unknown (31589 is id of unknown)
artworks_df['Artist ID'] = artworks_df['Artist ID'].fillna('31589')

# replace empty credit to unknown
artworks_df['Credit'] = artworks_df['Credit'].fillna('Unknown')

# replace NaN Acquisition Date with 'Unknown'
artworks_df['Acquisition Date'] = artworks_df['Acquisition Date'].fillna('Unknown')

# remove Acquisition Date with wrong format
artworks_df= artworks_df[artworks_df['Acquisition Date'].str.contains(r'\d{4}-\d{2}-\d{2}', regex=True)]

# split multiple Artists into different lines
artworks_df['Artist ID'] = artworks_df['Artist ID'].str.split(', ')
artworks_df = artworks_df.explode('Artist ID')

artists_df['Artist ID'] = artists_df['Artist ID'].astype(str)
artists_df = artists_df[~artists_df['Artist ID'].str.contains(',')]

artworks_df = pd.merge(artworks_df, artists_df, how='left', on='Artist ID')
del artists_df

# The whole thing in this dataset is that if an artwork were made by 2 or more artists,
# there will be another "artist" with unique ID and EVEN BIRTHDATE! What is more,
# it has a name such as $Artistname1 [and|+|,|etc.] $Artistname2 I don't know is that
# a strict rule, but suppose not, so better will be to remove those "shadow clones"
# artworks_df = artworks_df[~artworks_df.Name.str.contains(r'\,|\+')]

# if it prints error - try with na=False

# making life easier
# artworks_df = artworks_df[~artworks_df.Date.str.contains('Unknown', case=False,)]
# artworks_df = artworks_df[~artworks_df['Acquisition Date'].str.contains('Unknown', case=False,)]
# artworks_df = artworks_df[~artworks_df['Artist ID'].str.contains('Unknown', case=False,)]

# template for finding rexexpr
# print(artworks_df['Date'].str.findall(r'\s*(\d{4})[-–](\d{2,4})\s*').head(940))


def execute_query(query, args, cur):
    try:
        cur.execute (query,args)
    except cx_Oracle.Error as error:
        # print('Failed to insert row', error)
        pass


conn = cx_Oracle.connect(cred.name, cred.passw, "localhost/XE")
cur = conn.cursor()
into_artist_q = "INSERT INTO ARTIST (ARTIST_ID, ARTIST_NAME) VALUES (:artist_id, :artist_name)"
into_proc_officer_q = "INSERT INTO PROC_OFFICER (PROC_OFFICER_NAME) VALUES (:proc_officer_name)"
into_artwork_q = "INSERT INTO ARTWORK (ARTWORK_ID, ARTWORK_TITLE, ARTWORK_CREATION_YEAR, ACQUSITION_DATE, PROC_OFFICER_NAME) VALUES (:artwork_id, :artwork_title , :a_c_year, TO_DATE(:acquisition_date, 'YYYY-MM-DD'), :proc_officer_name)"
into_rel_artw_arti_q = "INSERT INTO RELATION_ARTWORK_ARTIST (ARTWORK_ARTWORK_ID, ARTIST_ARTIST_ID) VALUES (:artwork_id, :artist_id)"
into_rel_ao_q = "INSERT INTO RELATION_AO (PROC_OFFICER_NAME, ARTWORK_ARTWORK_ID) VALUES (:proc_officer_name, :artwork_id)"


# Test data
# execute_query(into_artist_q, [78787878, "cheburekor"], conn)
# execute_query(into_proc_officer_q, ["Gift of Luck"], conn)
# execute_query(into_artwork_q, [87878787, "Tvorenie",2020,"2020-05-29","Gift of Luck"], conn)
# execute_query(into_rel_artw_arti_q, [87878787, 78787878], conn)
# execute_query(into_rel_ao_q, ["Gift of Luck",87878787], conn)

print("Starting inserting into the rows")

for row in artworks_df.itertuples():
    # if 'unknown' in row.Date.lower():
    #     continue
    # if 'unknown' in row._5.lower():
    #     continue
    # if 'unknown' in row._3.lower():
    #     continue
    execute_query(into_artist_q, [row._3, row.Name], cur)
    execute_query(into_proc_officer_q, [row.Credit], cur)
    execute_query(into_artwork_q, [row._1, row.Title, row.Date,row._5,row.Credit], cur)
    execute_query(into_rel_artw_arti_q, [row._1, row._3], cur)
    execute_query(into_rel_ao_q, [row.Credit,row._1], cur)
    
    # print(row.Index, row.date, row.delay)

# print(artworks_df.head(30).to_string(index=False))
# cur.close()
conn.commit()
conn.close()