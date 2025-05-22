
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math


def model_sejsmiczny_video(zapisz_jako="sejsmogram_animacja.mp4"):
    # wymiar siatki x i y

    n = 600

    V = np.empty([n, n])
    V[:, :] = 1000
    V[200:300, 100:350] = 343
    V[300:400, 250:500] = 343
    # wspolrzedne srodka z ktorego rozchodzi sie fala
    xs = 100
    yx = 250
    # wspolrzedne punktu pomiarowego
    xp = 500
    yp = 350
    # krok
    dt = 0.002
    # czestotliwosc
    fpeak = 30
    et = 0.6
    ds = 1.0
    # kroki czasowe dla sejsmogramu
    nt = int(et / dt) + 1
    # macierze dla pol cisnien w czasie t+1, t, t-1
    pm, pp, p = [np.full((n, n), 0.0) for _ in range(3)]
    # warunek stabilnosci
    vmax = 2000
    # dtr- realny krok probkowania
    dtr = ds / (2.0 * vmax)
    w2 = 0
    while True:
        w2 += 1
        w1 = dt / w2
        if w1 <= dtr:
            dtr = w1
            break

    kk = 1
    kkk = 0
    k = 1
    dtr_ds = dtr / ds

    sejsmogram = []
    sejsmogram_xp_yp = []
    frames = []

    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(p, cmap="seismic", vmin=-0.01, vmax=0.01, animated=True)
    ax.set_title("Propagacja fali sejsmicznej")

    def update_frame(frame_num):
        nonlocal p, pp, pm, k, kk, kkk

        for _ in range(5):  # przeskocz 3 kroki symulacji na każdą klatkę
            k += 1
            kk += 1
            t = k * dtr

            pp[1:-1, 1:-1] = 2.0 * p[1:-1, 1:-1] - pm[1:-1, 1:-1] + ((dtr ** 2) / (ds ** 2)) * \
                             V[1:-1, 1:-1] ** 2 * (
                                         p[2:, 1:-1] + p[:-2, 1:-1] + p[1:-1, 2:] + p[1:-1, :-2] - 4 * p[1:-1, 1:-1])
            s = math.exp(-((math.pi * fpeak * (t - (1.0 / fpeak))) ** 2)) * \
                (1.0 - 2.0 * ((math.pi * fpeak * (t - (1.0 / fpeak))) ** 2))

            pp[yx, xs] += s

            pp[:, 0] = p[:, 0] + p[:, 1] - pm[:, 1] + V[:, 0] * dtr_ds * (p[:, 1] - p[:, 0] - (pm[:, 2] - pm[:, 1]))
            pp[:, -1] = p[:, -1] + p[:, -2] - pm[:, -2] + V[:, -1] * dtr_ds * (
                        p[:, -2] - p[:, -1] - (pm[:, -3] - pm[:, -2]))
            pp[0, :] = p[0, :] + p[1, :] - pm[1, :] + V[0, :] * dtr_ds * (p[1, :] - p[0, :] - (pm[2, :] - pm[1, :]))
            pp[-1, :] = p[-1, :] + p[-2, :] - pm[-2, :] + V[-1, :] * dtr_ds * (
                        p[-2, :] - p[-1, :] - (pm[-3, :] - pm[-2, :]))

            # pp[:, 0] = 0
            # pp[:, -1] = 0
            # pp[0, :] = 0
            # pp[-1, :] = 0

            pm[:] = p[:]
            p[:] = pp[:]

            sejsmogram.append(p[yx, xs])  # rejestrujemy punkt sejsmogramu
            sejsmogram_xp_yp.append(p[yp, xp])  # rejestrujemy punkt na koncu okopu

        im.set_data(p)
        return [im]

    total_frames = int(et / (3 * dtr))  # co 3 krok = 1 klatka
    ani = animation.FuncAnimation(fig, update_frame, frames=total_frames, blit=True)

    print(f"Zapisuję animację jako {zapisz_jako}...")

    ani.save(zapisz_jako, fps=30, dpi=150)

    plt.close(fig)

    max_cisnienie = max(abs(np.array(sejsmogram_xp_yp)))

    print(f"Maksymalna amplituda w punkcie ({xp}, {yp}): {max_cisnienie:.3f}")

    return sejsmogram, sejsmogram_xp_yp


sejsmo, max_cis = model_sejsmiczny_video()

from IPython.display import Video

Video("sejsmogram_animacja.mp4")