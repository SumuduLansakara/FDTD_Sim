import matplotlib.image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from dim2.engine import parallel_pthread, serial_naive, serial_vector
from settings import *


class Simulation:
    def __init__(self):
        # material properties
        self._epsilon: np.ndarray = None
        self._mu: np.ndarray = None

        # fields
        self._Ez: np.ndarray = None
        self._Hy: np.ndarray = None
        self._Hx: np.ndarray = None

        # source
        self._src_x: int = None
        self._src_y: int = None

        # plot
        self._im: matplotlib.image.AxesImage = None

        # pre-calculated factors
        self._f_Hy: float = delta_t / (delta_xy * mu0)
        self._f_Hx: float = delta_t / (delta_xy * mu0)
        self._f_Ez: float = delta_t / (delta_xy * epsilon0)

        self._engine = None

    def _update_Hx(self):
        for y in range(world_height - 1):
            self._Hx[:-1, y] -= self._f_Hx * (self._Ez[:-1, y + 1] - self._Ez[:-1, y])

    def _update_Hy(self):
        for x in range(world_width - 1):
            self._Hy[x, :-1] += self._f_Hy * (self._Ez[x + 1, :-1] - self._Ez[x, :-1])

    def _init_material(self):
        """ Set uniform permittivity and permeability for homogeneous material """
        self._epsilon = epsilon0 * np.ones((world_width, world_height))
        self._mu = mu0 * np.ones((world_width, world_height))

    def _init_fields(self):
        """ Set initial electric and magnetic field values """
        self._Ez = np.zeros((world_width, world_height))
        self._src_x = world_width // 2
        self._src_y = world_height // 2
        self._Hy = np.zeros((world_width, world_height))
        self._Hx = np.zeros((world_width, world_height))

    def _init_engine(self):
        """ Initialize field update method depending on the setting """
        if update_mode == 0:
            print("update mode = serial_naive")
            self._engine = serial_naive
        elif update_mode == 1:
            print("update mode = serial_vectorized")
            self._engine = serial_vector
        elif update_mode == 2:
            print("update mode = parallel")
            self._engine = parallel_pthread
        else:
            raise NotImplementedError("Invalid update mode {}".format(update_mode))
        self._engine.prepare(self)

    def _start_animation_loop(self):
        """ Start animation loop """
        fig = plt.figure()
        self._im = plt.imshow(self._Ez, cmap='gist_gray_r', vmin=0, vmax=1)
        anim = animation.FuncAnimation(fig, lambda n: self._engine.update(self, n), interval=50)
        plt.show()

    def start(self):
        """ Initialize parameters and start animation """
        self._init_material()
        self._init_fields()
        self._init_engine()
        self._start_animation_loop()
        self._engine.finalize()
