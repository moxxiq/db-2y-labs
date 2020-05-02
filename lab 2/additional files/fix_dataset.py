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

# set right names to the artists via additional artists.csv
# easy way by additional file
artists_df = pd.read_csv("dataset/artists.csv")
artists_df['Artist ID'] = artists_df['Artist ID'].astype(str)
artists_df = artists_df[['Artist ID', 'Name']]
artworks_df = pd.merge(artworks_df, artists_df, how='left', on='Artist ID')
del artists_df

'''
The whole thing in this dataset is that if an artwork were made by 2 or more artists,
there will be another "artist" with unique ID and EVEN BIRTHDATE! What is more,
it has a name such as $Artistname1 [and|+|,|etc.] $Artistname2 I don't know is that
a strict rule, but suppose not, so better will be to remove those "shadow clones"
'''
artworks_df = artworks_df[~artworks_df.Name.str.contains(r'\,|\+')]
# if it prints error - try with na=False

# making life easier
artworks_df = artworks_df[~artworks_df.Date.str.contains('Unknown', case=False,)]
artworks_df = artworks_df[~artworks_df['Acquisition Date'].str.contains('Unknown', case=False,)]
artworks_df = artworks_df[~artworks_df['Artist ID'].str.contains('Unknown', case=False,)]

# template for finding rexexpr
# print(artworks_df['Date'].str.findall(r'\s*(\d{4})[-–](\d{2,4})\s*').head(940))

# QUOTE_NONNUMERIC - compatibility issues need it
from csv import QUOTE_NONNUMERIC
artworks_df.to_csv('dataset/artworks_fixed.csv', index=False, quoting=QUOTE_NONNUMERIC)