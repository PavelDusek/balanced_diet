# coding: utf-8
import pandas as pd
import numpy as np
import glob

ideal_nutrition = np.array([ 140, 263, 68.3 ])
ideal_vector = ideal_nutrition / np.linalg.norm( ideal_nutrition )

dfs  = []
csvs = glob.glob("data/calories*.csv")
for csv in csvs:
    df = pd.read_csv(csv)
    df = df[[ 'name', 'energy', 'protein', 'sugar', 'fats', 'fiber'] ]
    dfs.append(df)
df = pd.concat(dfs)
df = df.drop_duplicates()
df = df.loc[ df['name'] != '{{f.title}}']

df['energy']   = pd.to_numeric( df['energy'].str.replace(",", ".").str.replace("\xa0", "") )
df['protein'] = pd.to_numeric( df['protein'].str.replace(",", ".").str.replace("\xa0", "") )
df['sugar'] = pd.to_numeric( df['sugar'].str.replace(",", ".").str.replace("\xa0", "") )
df['fiber']  = pd.to_numeric( df['fiber'].str.replace(",", ".").str.replace("\xa0", "") )
df['fats']      = pd.to_numeric( df['fats'].str.replace(",", ".").str.replace("\xa0", "") )

def unit_vector( row ):
    vector = np.array( [ row['protein'], row['sugar'], row['fats'] ] )
    magnitude = np.linalg.norm( vector )
    return vector/magnitude
def distance( row ):
    return np.linalg.norm( row['unit_vector'] - ideal_vector )

df['unit_vector'] = df.apply( unit_vector, axis = 1)
df['distance']    = df.apply( distance, axis = 1)

df.sort_values(by='distance').to_csv('best.csv', index = False)
