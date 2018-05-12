from dim2.engine.base_engine import BaseEngine


class SerialVectorEngine(BaseEngine):

    def update(self, n: int):
        """ Update single frame of the simulation """
        # vector operations for high single thread performance
        # update H fields

        self._Hx[:-1, :-1] -= self._f_Hx * (self._Ez[:-1, 1:] - self._Ez[:-1, :-1])
        self._Hy[:-1, :-1] += self._f_Hy * (self._Ez[1:, :-1] - self._Ez[:-1, :-1])

        # update E fields
        self._Ez[1:, 1:] += self._f_Ez * (self._Hy[1:, 1:] - self._Hy[:-1, 1:] - self._Hx[1:, 1:] + self._Hx[1:, :-1])

        # input from source
        self._Ez[self._src_x, self._src_y] = 1
