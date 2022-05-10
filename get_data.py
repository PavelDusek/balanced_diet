# coding: utf-8
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

def get( n : int ) -> dict:
    url = f"https://www.kaloricketabulky.cz/tabulka-potravin?page={n}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    nazev, energie, bilkoviny, sacharidy, tuky, vlaknina = [], [], [], [], [], []
    for tr in soup.find_all("tr", class_ = "p-table-bg-hover"):
        values = [ td.text.strip() for td in tr.find_all("td") ]
        n, e, b, s, t, v = values
        nazev.append(n)
        energie.append(e)
        bilkoviny.append(b)
        sacharidy.append(s)
        tuky.append(t)
        vlaknina.append(v)
    return { 'nazev': nazev, 'energie': energie, 'bilkoviny': bilkoviny, 'sacharidy': sacharidy, 'tuky': tuky, 'vlaknina': vlaknina}

nazev, energie, bilkoviny, sacharidy, tuky, vlaknina = [], [], [], [], [], []
for n in range(1, 10000):
    try:
        print(n)
        data = get(n)
        data_df = pd.DataFrame( data )
        print( data_df )
        data_df.to_csv(f"data/calories{n}.csv")
        nazev.extend(     data['nazev']     )
        energie.extend(   data['energie']   )
        bilkoviny.extend( data['bilkoviny'] )
        sacharidy.extend( data['sacharidy'] )
        tuky.extend(      data['tuky']      )
        vlaknina.extend(  data['vlaknina']  )
        df = pd.DataFrame({ 'nazev': nazev, 'energie': energie, 'bilkoviny': bilkoviny, 'sacharidy': sacharidy, 'tuky': tuky, 'vlaknina': vlaknina})
        print()
        time.sleep(5)
    except requests.exceptions.ConnectionError as excp:
        print(excp)
        with open("errors", "a") as f:
            f.write(f"{n}\n")

