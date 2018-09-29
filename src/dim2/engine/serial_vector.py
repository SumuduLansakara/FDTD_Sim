from dim2.engine.base_engine import BaseEngine
from settings import delta_t


class SerialVectorEngine(BaseEngine):

    def update(self, n: int):
        """ Update single frame of the simulation """
        # vector operations for high single thread performance
        # update H fields

        f = (delta_t - 1) / (delta_t + 1)

        # update Hx field
        hx_y0 = self._Hx[:, 0]
        hx_y1 = self._Hx[:, 1]
        hx_y_0 = self._Hx[:, -1]
        hx_y_1 = self._Hx[:, -2]
        hx_x0 = self._Hx[0, :]
        hx_x1 = self._Hx[1, :]
        hx_x_0 = self._Hx[-1, :]
        hx_x_1 = self._Hx[-2, :]

        self._Hx[:-1, :-1] -= self._f_Hx * (self._Ez[:-1, 1:] - self._Ez[:-1, :-1])

        self._Hx[:, 0] = hx_y1 + f * (self._Hx[:, 1] - hx_y0)
        self._Hx[:, -1] = hx_y_1 + f * (self._Hx[:, -2] - hx_y_0)
        self._Hx[0, :] = hx_x1 + f * (self._Hx[1, :] - hx_x0)
        self._Hx[-1, :] = hx_x_1 + f * (self._Hx[-2, :] - hx_x_0)

        # update Hy field
        hy_x0 = self._Hy[0, :]
        hy_x1 = self._Hy[1, :]
        hy_x_0 = self._Hy[-1, :]
        hy_x_1 = self._Hy[-2, :]
        hy_y0 = self._Hy[:, 0]
        hy_y1 = self._Hy[:, 1]
        hy_y_0 = self._Hy[:, -1]
        hy_y_1 = self._Hy[:, -2]

        self._Hy[:-1, :-1] += self._f_Hy * (self._Ez[1:, :-1] - self._Ez[:-1, :-1])

        self._Hy[0, :] = hy_x1 + f * (self._Hy[1, :] - hy_x0)
        self._Hy[-1, :] = hy_x_1 + f * (self._Hy[-2, :] - hy_x_0)
        self._Hy[:, 0] = hy_y1 + f * (self._Hy[:, 1] - hy_y0)
        self._Hy[:, -1] = hy_y_1 + f * (self._Hy[:, -2] - hy_y_0)

        # update E fields
        self._Ez[1:, 1:] += self._f_Ez * (self._Hy[1:, 1:] - self._Hy[:-1, 1:] - self._Hx[1:, 1:] + self._Hx[1:, :-1])

        # input from source
        self._Ez[self._src_x, self._src_y] = 1
