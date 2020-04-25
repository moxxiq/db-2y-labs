import pandas as pd
import numpy as np

artworks_df = pd.read_csv("dataset/artworks.csv")

# remove unnecessary columns 
artworks_df.drop(["Name","Medium", "Dimensions", "Catalogue", "Department", "Classification", "Object Number", "Diameter (cm)", "Circumference (cm)", "Height (cm)", "Length (cm)", "Width (cm)", "Depth (cm)", "Weight (kg)", "Duration (s)"],
                 axis=1,
                 inplace=True)

# get only title of the artwork
artworks_df['Title'] = artworks_df['Title'].apply(
    lambda t: str(t).split(',')[0])

# fix year '1956-57' -> '1957'
artworks_df['Date'] = artworks_df['Date'].str.replace(r'.*(\d{4})([-–]\d{2,4})*[^\d]*', 
    lambda s: s.group(1)[:2]+s.group(2)[-2:] if s.group(2) else s.group(1))

#TODO: remove arts with unknown year

# split multiple Artists into different lines
artworks_df['Artist ID'] = artworks_df['Artist ID'].str.split(', ')
artworks_df = artworks_df.explode('Artist ID')

# set right names to the artists via additional artists.csv
artists_df = pd.read_csv("dataset/artists.csv")
artists_df['Artist ID'] = artists_df['Artist ID'].astype(str)
artists_df = artists_df[['Artist ID', 'Name']]
artworks_df = pd.merge(artworks_df, artists_df, how='left', on='Artist ID')
del artists_df

#TODO: Change 'NULL' Artist_ID to some 'Unknown'

# finding rexexpr
# print(artworks_df['Date'].str.findall(r'\s*(\d{4})[-–](\d{2,4})\s*').head(940))

print(artworks_df)
