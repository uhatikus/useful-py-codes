import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter

import random
random.seed(1)

Satellite_mass = 1  # Satellite math: 10 000 kg = 10^4 kg
Earth_mass = 6 * (10 ** 4) # 6 *10 ^ 24 kg
Radius = 1

def get_satellites():
    Satellites = []
    # number_of_satellites = 2
    # for i in range(number_of_satellites):
    #
    #     x_i, y_i, z_i = (np.sqrt(Radius) * random.uniform(-1, 1),
    #                      np.sqrt(Radius) * random.uniform(-1, 1),
    #                      np.sqrt(Radius) * random.uniform(-1, 1))
    #     root_sum_coors = (x_i**2 + y_i**2 + z_i**2)**(0.5)
    #     x_i, y_i, z_i = x_i / root_sum_coors, \
    #                     y_i  / root_sum_coors, \
    #                     z_i  / root_sum_coors
    #
    #     vx_i, vy_i, vz_i = (np.sqrt(Earth_mass) * random.uniform(-1, 1),
    #                         np.sqrt(Earth_mass) * random.uniform(-1, 1),
    #                         np.sqrt(Earth_mass) * random.uniform(-1, 1))
    #     root_sum_vs = (vx_i**2 + vy_i**2 + vz_i**2)**(0.5)
    #     vx_i, vy_i, vz_i = vx_i / root_sum_vs, \
    #                        vy_i / root_sum_vs, \
    #                        vz_i / root_sum_vs
    #
    #     try:
    #         assert x_i**2 + y_i**2 + z_i**2 < Radius * 1.0001 and \
    #            x_i**2 + y_i**2 + z_i**2 > Radius *  0.9999
    #     except Exception:
    #         print(x_i, y_i, z_i)
    #
    #     try:
    #         assert vx_i**2 + vy_i**2 + vz_i**2 < Earth_mass * 1.0001 and \
    #                vx_i**2 + vy_i**2 + vz_i**2 > Earth_mass *  0.9999
    #     except Exception:
    #         print(vx_i, vy_i, vz_i, vx_i**2 + vy_i**2 + vz_i**2)
    #
    #     Satellites.append(Satellite([x_i, y_i, z_i], [vx_i, vy_i, vz_i]))

    all_satellites_data = [
        [[Radius, 0, 0], [0, np.sqrt(Earth_mass), 0]],
        [[Radius, 0, 0], [0, 0, np.sqrt(Earth_mass)]],
        [[Radius, 0, 0], [0, -np.sqrt(Earth_mass), 0]],
        [[Radius, 0, 0], [0, 0, -np.sqrt(Earth_mass)]],
        [[Radius, 0, 0], [0, np.sqrt(Earth_mass / 2),
                  np.sqrt(Earth_mass / 2)]],
        [[Radius, 0, 0], [0, -np.sqrt(Earth_mass / 2),
                  -np.sqrt(Earth_mass / 2)]],
        [[Radius, 0, 0], [0, np.sqrt(Earth_mass / 2),
                  -np.sqrt(Earth_mass / 2)]],
        [[Radius, 0, 0], [0, -np.sqrt(Earth_mass / 2),
                  np.sqrt(Earth_mass / 2)]],

        [[0, Radius, 0], [np.sqrt(Earth_mass), 0, 0]],
        [[0, Radius, 0], [0, 0, np.sqrt(Earth_mass)]],
        [[0, Radius, 0], [-np.sqrt(Earth_mass), 0, 0]],
        [[0, Radius, 0], [0, 0, -np.sqrt(Earth_mass)]],
        [[0, Radius, 0], [np.sqrt(Earth_mass / 2), 0,
                          np.sqrt(Earth_mass / 2)]],
        [[0, Radius, 0], [-np.sqrt(Earth_mass / 2), 0,
                          -np.sqrt(Earth_mass / 2)]],
        [[0, Radius, 0], [np.sqrt(Earth_mass / 2), 0,
                          -np.sqrt(Earth_mass / 2)]],
        [[0, Radius, 0], [-np.sqrt(Earth_mass / 2), 0,
                          np.sqrt(Earth_mass / 2)]],

        [[0, 0, Radius], [np.sqrt(Earth_mass), 0, 0]],
        [[0, 0, Radius], [0, np.sqrt(Earth_mass), 0]],
        [[0, 0, Radius], [-np.sqrt(Earth_mass), 0, 0]],
        [[0, 0, Radius], [0, -np.sqrt(Earth_mass), 0]],
        [[0, 0, Radius], [np.sqrt(Earth_mass / 2),
                          np.sqrt(Earth_mass / 2), 0]],
        [[0, 0, Radius], [-np.sqrt(Earth_mass / 2),
                          -np.sqrt(Earth_mass / 2), 0]],
        [[0, 0, Radius], [np.sqrt(Earth_mass / 2),
                          -np.sqrt(Earth_mass / 2), 0]],
        [[0, 0, Radius], [-np.sqrt(Earth_mass / 2),
                          np.sqrt(Earth_mass / 2), 0]],

        [[-Radius, 0, 0], [0, np.sqrt(Earth_mass), 0]],
        [[-Radius, 0, 0], [0, 0, np.sqrt(Earth_mass)]],
        [[-Radius, 0, 0], [0, -np.sqrt(Earth_mass), 0]],
        [[-Radius, 0, 0], [0, 0, -np.sqrt(Earth_mass)]],
        [[-Radius, 0, 0], [0, np.sqrt(Earth_mass / 2),
                          np.sqrt(Earth_mass / 2)]],
        [[-Radius, 0, 0], [0, -np.sqrt(Earth_mass / 2),
                          -np.sqrt(Earth_mass / 2)]],
        [[-Radius, 0, 0], [0, np.sqrt(Earth_mass / 2),
                          -np.sqrt(Earth_mass / 2)]],
        [[-Radius, 0, 0], [0, -np.sqrt(Earth_mass / 2),
                          np.sqrt(Earth_mass / 2)]],

        [[0, -Radius, 0], [np.sqrt(Earth_mass), 0, 0]],
        [[0, -Radius, 0], [0, 0, np.sqrt(Earth_mass)]],
        [[0, -Radius, 0], [-np.sqrt(Earth_mass), 0, 0]],
        [[0, -Radius, 0], [0, 0, -np.sqrt(Earth_mass)]],
        [[0, -Radius, 0], [np.sqrt(Earth_mass / 2), 0,
                          np.sqrt(Earth_mass / 2)]],
        [[0, -Radius, 0], [-np.sqrt(Earth_mass / 2), 0,
                          -np.sqrt(Earth_mass / 2)]],
        [[0, -Radius, 0], [np.sqrt(Earth_mass / 2), 0,
                          -np.sqrt(Earth_mass / 2)]],
        [[0, -Radius, 0], [-np.sqrt(Earth_mass / 2), 0,
                          np.sqrt(Earth_mass / 2)]],

        [[0, 0, -Radius], [np.sqrt(Earth_mass), 0, 0]],
        [[0, 0, -Radius], [0, np.sqrt(Earth_mass), 0]],
        [[0, 0, -Radius], [-np.sqrt(Earth_mass), 0, 0]],
        [[0, 0, -Radius], [0, -np.sqrt(Earth_mass), 0]],
        [[0, 0, -Radius], [np.sqrt(Earth_mass / 2),
                          np.sqrt(Earth_mass / 2), 0]],
        [[0, 0, -Radius], [-np.sqrt(Earth_mass / 2),
                          -np.sqrt(Earth_mass / 2), 0]],
        [[0, 0, -Radius], [np.sqrt(Earth_mass / 2),
                          -np.sqrt(Earth_mass / 2), 0]],
        [[0, 0, -Radius], [-np.sqrt(Earth_mass / 2),
                          np.sqrt(Earth_mass / 2), 0]],
        ]

    for Satellite_data_unit in all_satellites_data:
        Satellites.append(Satellite(Satellite_data_unit[0], Satellite_data_unit[1]))


    return Satellites


class Satellite:

    def __init__(self, coordinates, velocity):

        assert len(coordinates) == len(velocity)

        self.dim = len(coordinates)

        self.mass = Satellite_mass
        self.init_coordinates = coordinates
        self.init_velocity = velocity

        self.trajectory = None


class SatelliteNetwork:

    def __init__(self, Satellites):

        self.Earth_mass = Earth_mass
        self.Radius = Radius
        self.mass_to_radiusin3 = self.Earth_mass / (self.Radius ** 3)

        self.Satellites = Satellites
        self.n_Satellites = len(Satellites)

        self.number_of_values_per_satellite = 2 * self.Satellites[0].dim

    def simulate(self):
        t = np.linspace(0, 1, 10000)
        y0 = []
        for Satellite_i in self.Satellites:
            y0 = y0 + Satellite_i.init_coordinates + Satellite_i.init_velocity

        sol = odeint(self.calculate_dSdt, y0=y0, t=t)

        for i, Satellite_i in enumerate(self.Satellites):
            Satellite_i.trajectory = [sol.T[i * self.number_of_values_per_satellite],
                                     sol.T[i * self.number_of_values_per_satellite + 1],
                                     sol.T[i * self.number_of_values_per_satellite + 2]]

            trajectories_df = pd.DataFrame(Satellite_i.trajectory)
            trajectories_df = trajectories_df.transpose()
            trajectories_df.columns = ["x", "y", "z"]
            # ax = trajectories_df.plot()
            # ax.set_xlim(0, 200)
            # plt.show()

        def animate(i):
            ax.view_init(elev=10., azim=i/4)
            xs = []
            ys = []
            zs = []
            for Satellite_i in self.Satellites:
                xs.append(Satellite_i.trajectory[0][i])
                ys.append(Satellite_i.trajectory[1][i])
                zs.append(Satellite_i.trajectory[2][i])

            scatter._offsets3d = (xs, ys, zs)
            # text.set_text('Time = {:.2f} Years'.format(i * tt))

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection='3d')
        ax.grid()
        scatter = ax.scatter3D([], [], [])
        text = ax.text(0.7, 0.7, 0.7, s="")
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlim(-1.5, 1.5)
        ax.set_zlim(-1.5, 1.5)
        ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)
        ani.save('plan_3D_yz_new_6.gif', writer='pillow', fps=30)

    def calculate_dSdt(self, S, t):
        dSdt = []

        for i in range(self.n_Satellites):
            dCoordinates = list(S[i * self.number_of_values_per_satellite + self.Satellites[0].dim:
                             i * self.number_of_values_per_satellite + 2 * self.Satellites[0].dim])

            dVelocity = [- self.mass_to_radiusin3 * S[i * self.number_of_values_per_satellite],
                         - self.mass_to_radiusin3 * S[i * self.number_of_values_per_satellite+1] ,
                         - self.mass_to_radiusin3 * S[i * self.number_of_values_per_satellite+2]]

            dSdt = dSdt + dCoordinates + dVelocity

        return dSdt


if __name__ == "__main__":
    Satellites = get_satellites()
    SN = SatelliteNetwork(Satellites)
    SN.simulate()
