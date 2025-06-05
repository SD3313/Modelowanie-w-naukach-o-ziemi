import pandas as pd
import math

# Wczytaj dane z pliku CSV
df = pd.read_csv('daily_ice_edge.csv')

# Wyświetl kilka pierwszych wierszy, aby sprawdzić poprawność importu

print(df.iloc[0])

srodek = [0,0]

def wspolrzedne(kat,r):
    x = srodek[0] + r * math.cos(kat)
    y = srodek[1] + r * math.sin(kat)
    return [x,y]

for x in range(1,len(df.columns)):
    kat = x-1
    r = df.iloc[0][x]
    map(wspolrzedne(),(kat,r))