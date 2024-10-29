from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)

class  Czastka:
    A:str
    B:str
    points = np.empty((0, 2), dtype=float)
    def __init__(self, A, B):
        self.A = A
        self.B = B
        
    def return_A(self):
        return self.A
    
    def return_B(self):
        return self.B
    
    def return_points(self):
        return self.points
    
    def append_points(self, x, y):
        self.points = np.append(self.points, [[x, y]], axis=0)
        
set_interval = int(input("Podaj co ile ma sie zmieniac klatka (ms):  "))    
czastki = []
rownania = int(input("Podaj ilość równań: "))
for i in range(rownania):
    A_part = input("Podaj wartość A: ")
    B_part = input("Podaj wartość B: ")
    czastki.append(Czastka(A_part, B_part))
    
points_limit = int(input("Podaj ostatna wartosc 't' do obliczenia: "))
step = float(input("Podaj co ile ma obliczac: "))
calc = 0
points = np.empty((0, 2), dtype=float)
maxcalc = 0
for czastka in czastki:
    calc = 0
    while calc < points_limit+1:
        x = eval(czastka.return_A()   , {'t': calc})
        y = eval(czastka.return_B(), {'t': calc})
        calc += step
        czastka.append_points(x, y)

fig, ax = plt.subplots()
scatters = [ax.plot([], [], 'o', label=f'Czastka {i+1}')[0] for i in range(len(czastki))]

def init():
    ax.set_xlim(0, step*max([eval(czastka.return_A(), {'t': points_limit}) for czastka in czastki]))
    ax.set_ylim(0, step*max([eval(czastka.return_B(), {'t': points_limit}) for czastka in czastki]))
    return scatters

def update(frame):
    for scatter, czastka in zip(scatters, czastki):
        points = czastka.return_points()
        scatter.set_data(points[frame, 0], points[frame, 1])
    return scatters

ani = FuncAnimation(fig, update, frames=range(points_limit+1), init_func=init, blit=True, interval=set_interval, repeat=True)
plt.xlabel('x[m]')
plt.ylabel('y[m]')
plt.legend()
plt.show()
