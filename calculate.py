# coding: utf-8
import pandas as pd
import numpy as np
import glob
import re

getNumber = re.compile("kalorie(\d+)\.csv")

ideal_nutrition = np.array([ 140, 263, 68.3 ])
ideal_vector = ideal_nutrition / np.linalg.norm( ideal_nutrition )

dfs  = []
csvs = glob.glob("kalorie*.csv")
for csv in csvs:
    df = pd.read_csv(csv)
    df = df[[ 'nazev', 'energie', 'bilkoviny', 'sacharidy', 'tuky', 'vlaknina'] ]
    dfs.append(df)
df = pd.concat(dfs)
df = df.drop_duplicates()
df = df.loc[ df['nazev'] != '{{f.title}}']

df['energie']   = pd.to_numeric( df['energie'].str.replace(",", ".") )
df['bilkoviny'] = pd.to_numeric( df['bilkoviny'].str.replace(",", ".") )
df['sacharidy'] = pd.to_numeric( df['sacharidy'].str.replace(",", ".") )
df['vlaknina']  = pd.to_numeric( df['vlaknina'].str.replace(",", ".") )
df['tuky']      = pd.to_numeric( df['tuky'].str.replace(",", ".") )

def unit_vector( row ):
    vector = np.array( [ row['bilkoviny'], row['sacharidy'], row['tuky'] ] )
    magnitude = np.linalg.norm( vector )
    return vector/magnitude
def distance( row ):
    return np.linalg.norm( row['unit_vector'] - ideal_vector )

df['unit_vector'] = df.apply( unit_vector, axis = 1)
df['distance']    = df.apply( distance, axis = 1)

df.sort_values(by='distance').to_csv('best.csv', index = False)
