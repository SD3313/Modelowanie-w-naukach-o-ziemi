import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from tqdm import tqdm
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

from math import sin  # do eval()


x_model = 200



# Wczytaj dane
df = pd.read_csv("daily_ice_edge.csv")


df_numeric = df.drop(columns=["Date"])

t = np.arange(df_numeric.shape[0])  # np. 0..9528
print(t)
def sinusoid(t, A, omega, phi, C):
    return A * np.sin(omega * t + phi) + C

wyniki_funkcji = []

print("Dopasowywanie i generowanie funkcji eval-friendly...")

for col in tqdm(df_numeric.columns):
    y = df_numeric[col].values

    try:
        guess = [np.std(y), 2 * np.pi / len(y), 0, np.mean(y)]
        popt, _ = curve_fit(sinusoid, t, y, p0=guess, maxfev=10000)
        A, omega, phi, C = popt

        A_ = round(A, 8)
        omega_ = round(omega, 8)
        phi_ = round(phi, 8)
        C_ = round(C, 8)

        funkcja_str = f"lambda x: {A_} * sin({omega_} * x + {phi_}) + {C_}"
    except Exception:
        funkcja_str = "None"

    wyniki_funkcji.append({
        "wierzcholek": col,
        "lambda_funkcja": funkcja_str
    })




df_funkcje = pd.DataFrame(wyniki_funkcji)
df_funkcje.to_csv("lambda_funkcje_dla_wierzcholkow2.csv", index=False)

print(df_funkcje)