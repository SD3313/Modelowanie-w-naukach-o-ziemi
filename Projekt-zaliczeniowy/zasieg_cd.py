import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

from math import sin  # do eval()


x_model =9000





img = Image.open("Antarctica_6400px_from_Blue_Marble.jpg")
img = np.asarray(img)


df = pd.read_csv('daily_ice_edge.csv')
df.columns = df.columns.str.strip()

given_date=df.iloc[x_model,0]
print(df)
print(given_date)


dzien_dane = df.iloc[x_model, 1:].values.astype(float)


df_f = pd.read_csv("lambda_funkcje_dla_wierzcholkow.csv")
wartosci_modelu = []

for idx, row in df_f.iterrows():
    func_str = row["lambda_funkcja"]
    try:
        f = eval(func_str)
        wartosc = f(x_model)
    except:
        wartosc = np.nan
    wartosci_modelu.append(wartosc)

# === NORMALIZACJA ===
def normalize_range(data, new_min, new_max):
    old_min = np.nanmin(data)
    old_max = np.nanmax(data)
    return [((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min for x in data]

#normalizacja
dzien_n = normalize_range(dzien_dane, 100, 160)
model_n = normalize_range(wartosci_modelu, 80, 160)

# === Konwersja na współrzędne biegunowe ===
angles = np.linspace(0, 360, len(dzien_n), endpoint=False)
angles = angles % 360

def to_xy(radii, angles):
    punkty = []
    for angle, radius in zip(angles, radii):
        x = math.sin(math.radians(angle)) * radius
        y = math.cos(math.radians(angle)) * radius
        punkty.append((x, y))
    return punkty

punkty_rzeczywiste = to_xy(dzien_n, angles)
punkty_model = to_xy(model_n, angles)


xs = [p[0] for p in punkty_rzeczywiste] + [punkty_rzeczywiste[0][0]]
ys = [p[1] for p in punkty_rzeczywiste] + [punkty_rzeczywiste[0][1]]

xs2 = [p[0] for p in punkty_model] + [punkty_model[0][0]]
ys2 = [p[1] for p in punkty_model] + [punkty_model[0][1]]





fig, ax = plt.subplots(figsize=(8, 8))
fig.suptitle(f"Zasięg lodu vs Model sinusoidalny", fontsize=15)
ax.plot(xs, ys, color='blue', label='Zasięg lodu (dane rzeczywiste)')
ax.plot(xs2, ys2, color='red', label='Model sinusoidalny')

# Ustawienia osi
ax.set_xlim(-160, 160)
ax.set_ylim(-160, 160)
ax.set_aspect('equal')
ax.set_title("dzień: "+given_date)


ax.imshow(img, extent=[-160, 160, -160, 160], alpha=0.2, zorder=0)

# Linie pomocnicze i okręgi
for r in np.linspace(50, 150, 5):
    circle = plt.Circle((0, 0), r, color='lightgray', fill=False, linestyle='--')
    ax.add_artist(circle)

for angle in np.arange(0, 360, 30):
    rad = math.radians(angle)
    x_line = [0, 100 * math.cos(rad)]
    y_line = [0, 100 * math.sin(rad)]
    ax.plot(x_line, y_line, color='lightgray', linestyle='--')


ax.legend()
plt.tight_layout()
plt.show()

