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

# split multiple Artists into different lines
# ...it's too long to do it the right way


# finding rexexpr
# print(artworks_df['Date'].str.findall(r'\s*(\d{4})[-–](\d{2,4})\s*').head(940))

print(artworks_fixed_df.head(2380))
# print(pd.DataFrame(artworks_df.City.str.split('|').tolist(), index=artworks_df.EmployeeId).stack())
# print(artworks_df['Date'].str.replace(r'\s*(\d{4})-(\d{2})\s*', lambda s: s.group(1)[:2]+s.group(2)).head(500))
