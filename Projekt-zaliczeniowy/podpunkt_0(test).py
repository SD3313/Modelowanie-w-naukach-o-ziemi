import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# Wczytaj dane z pliku CSV
df = pd.read_csv('daily_ice_edge.csv')

# Wyświetl kilka pierwszych wierszy, aby sprawdzić poprawność importu

print(df.iloc[0])

srodek = [0,0]


def normalize_range(data, new_min, new_max):
    old_min = min(data)
    old_max = max(data)
    return [((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min for x in data]


def wspolrzedne(kat, r):
    x = srodek[0] + r * math.cos(kat)
    y = srodek[1] + r * math.sin(kat)
    return [x, y]


minimum = [df[col].min() for col in df.columns[1:]]
minimum_normalized = normalize_range(minimum, 50, 110)

wsp_row = []
for x in range(1, len(df.columns)):
    kat = (x - 1) * 2 * np.pi / 360
    r = minimum_normalized[x - 1]
    wsp_row.append(wspolrzedne(kat,r))

x_coords = [point[0] for point in wsp_row]
y_coords = [point[1] for point in wsp_row]

#

plt.figure(figsize=(10, 10))
plt.plot(x_coords, y_coords, alpha=0.5)
plt.grid(True)
plt.axis('equal')
plt.title('Visualization of Normalized Ice Edge Coordinates')
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.xlim(-160, 160)
plt.ylim(-160, 160)
plt.show()
