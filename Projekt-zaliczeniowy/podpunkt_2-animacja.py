import pandas as pd
import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon

# Wczytaj dane
df = pd.read_csv('daily_ice_edge.csv')

minimum = [df[col].min() for col in df.columns[1:]]

# Funkcja normalizująca
def normalize_range(data, new_min, new_max):
    old_min = np.min(data)
    old_max = np.max(data)
    if old_max == old_min:
        return [new_min] * len(data)
    return [((x - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min for x in data]

minimum_normalized = normalize_range(minimum, 50, 110)

# Kąty
num_dirs = df.shape[1] - 1
angles = np.linspace(0, 360, num_dirs, endpoint=False)
angles = angles % 360
radii_min = 50
radii_max = 110

# Przygotuj figurę
fig, ax = plt.subplots(figsize=(8, 8))
line, = ax.plot([], [], color='blue')

# Dodaj siatkę kołową
for r in np.linspace(50, 150, 5):
    circle = plt.Circle((0, 0), r, color='lightgray', fill=False, linestyle='--')
    ax.add_artist(circle)

punkty = []
for angle, radius in zip(angles, minimum_normalized):
    x = math.sin(math.radians(angle)) * radius
    y = math.cos(math.radians(angle)) * radius
    punkty.append((x, y))

xm = [p[0] for p in punkty]
ym = [p[1] for p in punkty]

xm.append(xm[0])
ym.append(ym[0])

points = list(zip(xm, ym))
granica = Polygon(points, closed=True, facecolor='none', edgecolor='red', alpha=0.5)
ax.add_patch(granica)

for angle in np.arange(0, 360, 30):
    rad = np.radians(angle)
    x = [0, 100*np.cos(rad)]
    y = [0, 100*np.sin(rad)]
    ax.plot(x, y, color='lightgray', linestyle='--')

ax.set_xlim(-160, 160)
ax.set_ylim(-160, 160)
ax.set_aspect('equal')
title = ax.set_title('', fontsize=14)

# Funkcja aktualizująca klatkę
def update(frame):
    row = df.iloc[frame, 1:]
    normalized = normalize_range(row, radii_min, radii_max)
    xs = [math.sin(math.radians(a)) * r for a, r in zip(angles, normalized)]
    ys = [math.cos(math.radians(a)) * r for a, r in zip(angles, normalized)]
    xs.append(xs[0])
    ys.append(ys[0])
    line.set_data(xs, ys)
    title.set_text(f"Zasięg lodu – dzień {df.iloc[frame, 0]}")
    return line, title

# Stwórz animację
ani = animation.FuncAnimation(fig, update, frames=len(df), interval=100, blit=False)

plt.show()

#ani.save("zasieg-lodu.mp4", fps=45)