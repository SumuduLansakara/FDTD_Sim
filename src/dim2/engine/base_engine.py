import numpy as np

from settings import world_height, world_width, delta_t, delta_xy, mu0, epsilon0


class BaseEngine:
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

        # pre-calculated factors
        self._f_Hy: float = delta_t / (delta_xy * mu0)
        self._f_Hx: float = delta_t / (delta_xy * mu0)
        self._f_Ez: float = delta_t / (delta_xy * epsilon0)

    @property
    def Ez(self):
        return self._Ez

    def init_material(self):
        """ Set uniform permittivity and permeability for homogeneous material """
        self._epsilon = epsilon0 * np.ones((world_width, world_height))
        self._mu = mu0 * np.ones((world_width, world_height))

    def init_fields(self):
        """ Set initial electric and magnetic field values """
        self._Ez = np.zeros((world_width, world_height))
        self._src_x = world_width // 2
        self._src_y = world_height // 2
        self._Hy = np.zeros((world_width, world_height))
        self._Hx = np.zeros((world_width, world_height))

    def pre_update(self):
        pass

    def update(self, n: int):
        raise NotImplementedError

    def post_update(self):
        pass

    def _update_Hx(self):
        for y in range(world_height - 1):
            self._Hx[:-1, y] -= self._f_Hx * (self._Ez[:-1, y + 1] - self._Ez[:-1, y])

    def _update_Hy(self):
        for x in range(world_width - 1):
            self._Hy[x, :-1] += self._f_Hy * (self._Ez[x + 1, :-1] - self._Ez[x, :-1])
