# coding: utf-8
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

def get( n : int ) -> dict:
    url = f"https://www.kaloricketabulky.cz/tabulka-potravin?page={n}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    name, energy, protein, sugar, fats, fiber = [], [], [], [], [], []
    for tr in soup.find_all("tr", class_ = "p-table-bg-hover"):
        values = [ td.text.strip() for td in tr.find_all("td") ]
        n, e, b, s, t, v = values
        name.append(n)
        energy.append(e)
        protein.append(b)
        sugar.append(s)
        fats.append(t)
        fiber.append(v)
    return { 'name': name, 'energy': energy, 'protein': protein, 'sugar': sugar, 'fats': fats, 'fiber': fiber}

name, energy, protein, sugar, fats, fiber = [], [], [], [], [], []
#with open("errors") as f:
#    lines = f.readlines()
#ns = [int(line.strip()) for line in lines]
#for n in ns:
for n in range(1, 10000):
    try:
        print(n)
        data = get(n)
        data_df = pd.DataFrame( data )
        print( data_df )
        data_df.to_csv(f"data/calories{n}.csv")
        name.extend(     data['name']     )
        energy.extend(   data['energy']   )
        protein.extend( data['protein'] )
        sugar.extend( data['sugar'] )
        fats.extend(      data['fats']      )
        fiber.extend(  data['fiber']  )
        df = pd.DataFrame({ 'name': name, 'energy': energy, 'protein': protein, 'sugar': sugar, 'fats': fats, 'fiber': fiber})
        print()
        time.sleep(5)
    except requests.exceptions.ConnectionError as excp:
        print(excp)
        with open("errors", "a") as f:
            f.write(f"{n}\n")
        time.sleep(5*60)

