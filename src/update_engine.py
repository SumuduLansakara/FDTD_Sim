import numpy as np
from mpi4py import MPI

from settings import world_height, world_width, epsilon0, mu0, delta_t, delta_xy


class SerialVectorEngine:
    def __init__(self, comm, size, rank):
        # keep mpi status
        self._mpi_comm: MPI.Intracomm = comm
        self._mpi_size: int = size
        self._mpi_rank: int = rank

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

    def init(self):
        self._init_material()
        self._init_fields()

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

    def update(self):
        """ Update single frame of the simulation """
        # vector operations for high single thread performance
        self._mpi_comm.barrier()
        # update H fields
        if self._mpi_rank == 0:
            self._update_Hx_vector()
            self._mpi_comm.Sendrecv(self._Hx, 1, recvbuf=self._Hy)
        elif self._mpi_rank == 1:
            self._update_Hy_vector()
            self._mpi_comm.Sendrecv(self._Hy, 0, recvbuf=self._Hx)

        # update E fields
        self._Ez[1:, 1:] += self._f_Ez * (self._Hy[1:, 1:] - self._Hy[:-1, 1:] - self._Hx[1:, 1:] + self._Hx[1:, :-1])

        # input from source
        self._Ez[self._src_x, self._src_y] = 1

    def update_loop(self):
        while True:
            self.update()

    def _update_Hx_vector(self):
        self._Hx[:-1, :-1] -= self._f_Hx * (self._Ez[:-1, 1:] - self._Ez[:-1, :-1])

    def _update_Hy_vector(self):
        self._Hy[:-1, :-1] += self._f_Hy * (self._Ez[1:, :-1] - self._Ez[:-1, :-1])

    def _update_Hx_naive(self):
        for y in range(world_height - 1):
            self._Hx[:-1, y] -= self._f_Hx * (self._Ez[:-1, y + 1] - self._Ez[:-1, y])

    def _update_Hy_naive(self):
        for x in range(world_width - 1):
            self._Hy[x, :-1] += self._f_Hy * (self._Ez[x + 1, :-1] - self._Ez[x, :-1])
