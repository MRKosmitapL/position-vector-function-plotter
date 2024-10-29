from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)

class Czastka:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.points = np.empty((0, 2), dtype=float)
        
    def append_points(self, x, y):
        self.points = np.append(self.points, [[x, y]], axis=0)

def get_user_input():
    set_interval = int(input("Podaj co ile ma sie zmieniac klatka (ms): "))
    rownania = int(input("Podaj ilość równań: "))
    czastki = [Czastka(input("Podaj wartość A: "), input("Podaj wartość B: ")) for _ in range(rownania)]
    points_limit = int(input("Podaj ostatna wartosc 't' do obliczenia: "))
    step = float(input("Podaj co ile ma obliczac: "))
    return set_interval, czastki, points_limit, step

def calculate_points(czastki, points_limit, step):
    for czastka in czastki:
        calc = 0
        while calc <= points_limit:
            x = eval(czastka.A, {'t': calc})
            y = eval(czastka.B, {'t': calc})
            czastka.append_points(x, y)
            calc += step

def init_plot(czastki, points_limit, step):
    fig, ax = plt.subplots()
    scatters = [ax.plot([], [], 'o', label=f'Czastka {i+1}')[0] for i in range(len(czastki))]
    ax.set_xlim(0, step * max(eval(czastka.A, {'t': points_limit}) for czastka in czastki))
    ax.set_ylim(0, step * max(eval(czastka.B, {'t': points_limit}) for czastka in czastki))
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    plt.legend()
    return fig, ax, scatters

def update(frame, scatters, czastki):
    for scatter, czastka in zip(scatters, czastki):
        points = czastka.points
        scatter.set_data(points[frame, 0], points[frame, 1])
    return scatters

def main():
    set_interval, czastki, points_limit, step = get_user_input()
    calculate_points(czastki, points_limit, step)
    fig, ax, scatters = init_plot(czastki, points_limit, step)
    ani = FuncAnimation(fig, update, frames=range(points_limit + 1), fargs=(scatters, czastki), init_func=lambda: scatters, blit=True, interval=set_interval, repeat=True)
    plt.show()

if __name__ == "__main__":
    main()
