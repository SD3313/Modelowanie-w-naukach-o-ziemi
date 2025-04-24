from multiprocessing import Lock, Process, Queue, current_process
import random
import matplotlib; matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import matplotlib.animation as animation
import time









M=250 #rozmiar siatki Y
N=500 #rozmiar siatki X
x=3#ilosc rud zelaza
h=20#krok co ile liczymy pole

h=int(h)


L = np.zeros((M, N))
L += 3500

def rand_places(x): #losowanie indeksow w ktorych znajda sie te rudy
    ores= []
    for k in range(0,x):
        a = random.randint(0, 150)
        b = random.randint(0, 400)
        result = [a,b]
        ores.append(result)
    return ores

ore_positions = rand_places(x)

def body_create(x,L, positions):#generacja okraglych macierzy i dodanie ich do pola
    body_storage = []

    for k in range(0, x+1):

        body = np.full((100,100), np.nan)
        #body = body + 0.002
        center = [50, 50]
        for h in range(0,x):
            for i in range(body.shape[0]):
                for j in range(body.shape[1]):
                    point = [i, j]
                    euclidean = np.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)
                    if euclidean < 50:
                        a, b = positions[h]
                        L[a+i, b+j]=5500 ##wartosc rho dla rud
                        #body[i, j] = 0.006
        body_storage.append(body)
    return L

bodies = body_create(x, L, ore_positions)#wywolujemy funkcje

gamma = -6.67e-11

def gravity(L):
    epsilon = 1e-6
    z_data = []
    for k in range(100, 400):
        j = np.arange(1, M)
        i = np.arange(1, N)
        I, J = np.meshgrid(i, j, indexing='ij')

        d =np.abs(k-I)+epsilon#by nie bylo dzielenia przez 0
        r = np.sqrt(d**2+J**2)
        r_plus = np.sqrt((d+1)**2+(J+1)**2)

        theta = np.arctan(J/d)
        theta_plus = np.arctan((J+1)/(d+1))

        z = np.abs(gamma*np.sum(L[J, I]*(np.log(r_plus/r)-(theta_plus-theta))))
        z_data.append(z)

    return z_data



#podejscie bez multiprocessingu

start = time.time()
data_g=gravity(L)

end = time.time()
print(end-start)

fig, axs = plt.subplots(2, 1)
axs[0].matshow(L)
axs[1].plot(data_g)
plt.show()



