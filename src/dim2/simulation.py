import matplotlib.image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from settings import *


class Simulation:
    def __init__(self):
        # material properties
        self._epsilon = None
        self._mu = None

        # fields
        self._Ez = None
        self._Hy = None
        self._Hx = None

        # plot
        self._im = None

    def _update(self, n: int) -> matplotlib.image.AxesImage:
        """ update single frame of the simulation """
        # print("frame: {}".format(n))

        x_l = 0
        x_r = world_width - 2
        y_d = 0
        y_u = world_height - 2

        # vector operations for high single thread performance
        fac1 = (deltat / (delta * self._mu[x_l:x_r, y_d:y_u]))
        self._Hy[x_l:x_r, y_d:y_u] += fac1 * (self._Ez[x_l + 1:x_r + 1, y_d:y_u] - self._Ez[x_l:x_r, y_d:y_u])
        self._Hx[x_l:x_r, y_d:y_u] -= fac1 * (self._Ez[x_l:x_r, y_d + 1:y_u + 1] - self._Ez[x_l:x_r, y_d:y_u])

        fac2 = deltat / (delta * self._epsilon[x_l + 1:x_r + 1, y_d + 1:y_u + 1])
        self._Ez[x_l + 1:x_r + 1, y_d + 1:y_u + 1] += fac2 * (
                self._Hy[x_l + 1:x_r + 1, y_d + 1:y_u + 1] - self._Hy[x_l:x_r, y_d + 1:y_u + 1] -
                self._Hx[x_l + 1:x_r + 1, y_d + 1:y_u + 1] + self._Hx[x_l + 1:x_r + 1, y_d:y_u]
        )

        self._Ez[src_x, src_y] = 1
        self._im.set_data(self._Ez)
        return self._im

    def _init_material(self):
        """ set uniform permittivity and permeability for homogeneous material """
        self._epsilon = epsilon0 * np.ones((world_width, world_height))
        self._mu = mu0 * np.ones((world_width, world_height))

    def _init_fields(self):
        """ set initial electric and magnetic field values """
        self._Ez = np.zeros((world_width, world_height))
        self._Ez[src_x, src_y] = 1
        self._Hy = np.zeros((world_width, world_height))
        self._Hx = np.zeros((world_width, world_height))

    def _visualize(self):
        """ start animation loop """
        fig = plt.figure()
        self._im = plt.imshow(self._Ez, cmap='gist_gray_r', vmin=0, vmax=1)
        anim = animation.FuncAnimation(fig, self._update, interval=50)
        plt.show()

    def start(self):
        self._init_material()
        self._init_fields()
        self._visualize()
