import pandas as pd

artworks_df = pd.read_csv("dataset/artworks_fixed.csv")

# populate_sql
with open('populate.sql', 'w') as sql_file:
    # setting off the limitations
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)

    # cover ' with ''
    artworks_df['Name'] = artworks_df['Name'].str.replace("\'", "\'\'", regex=True)
    artworks_df['Credit'] = artworks_df['Credit'].str.replace("\'", "\'\'", regex=True)
    artworks_df['Title'] = artworks_df['Title'].str.replace("\'", "\'\'", regex=True)

    sql_file.write("-- Escape ampersand\n")
    sql_file.write("set define off\n\n")

    sql_file.write("-- Artist Table\n")
    sql_file.write(pd.Series(artworks_df.apply(lambda row: 
        "INSERT INTO ARTIST (ARTIST_ID, ARTIST_NAME) VALUES (" + 
        str(row['Artist ID']) +
        ", '" +
        str(row['Name'])+
        "');", 
        axis = 1).unique()).to_string(index=False))
    sql_file.write("\n\n")

    sql_file.write("-- PROC_OFFICER Table\n")
    sql_file.write(pd.Series(artworks_df.apply(lambda row: 
        "INSERT INTO PROC_OFFICER (PROC_OFFICER_NAME) VALUES (" + 
        "'" +
        str(row['Credit']) +
        "');", 
        axis = 1).unique()).to_string(index=False).replace(r'\n','').replace(r'\t',''))
    sql_file.write("\n\n")

    sql_file.write("-- ARTWORK Table\n")
    sql_file.write(pd.Series(artworks_df.apply(lambda row: 
        "INSERT INTO ARTWORK (ARTWORK_ID, ARTWORK_TITLE, ARTWORK_CREATION_YEAR, ACQUSITION_DATE, PROC_OFFICER_NAME) VALUES (" + 
        str(row['Artwork ID']) +
        ", '" +
        str(row['Title']) +
        "' , " +
        str(row['Date']) +
        ", TO_DATE('" +
        str(row['Acquisition Date']) +
        "', 'YYYY-MM-DD'), '" +
        str(row['Credit']) +
        "');", 
        axis = 1).unique()).to_string(index=False).replace(r'\n','').replace(r'\t',''))
    sql_file.write("\n\n")

    sql_file.write("-- RELATION_ARTWORK_ARTIST Table\n")
    sql_file.write(pd.Series(artworks_df.apply(lambda row: 
        "INSERT INTO RELATION_ARTWORK_ARTIST (ARTWORK_ARTWORK_ID, ARTIST_ARTIST_ID) VALUES (" + 
        str(row['Artwork ID']) +
        ", " +
        str(row['Artist ID'])+
        ");", 
        axis = 1).unique()).to_string(index=False))
    sql_file.write("\n\n")

    sql_file.write("-- RELATION_AO Table\n")
    sql_file.write(pd.Series(artworks_df.apply(lambda row: 
        "INSERT INTO RELATION_AO (PROC_OFFICER_NAME, ARTWORK_ARTWORK_ID) VALUES (" + 
        "'" +
        str(row['Credit']) +
        "', " +
        str(row['Artwork ID']) +
        ");", 
        axis = 1).unique()).to_string(index=False).replace(r'\n','').replace(r'\t',''))



# print(artworks_df.apply(lambda row: str(row['Artist ID']) + " " + str(row['Name']), axis = 1))