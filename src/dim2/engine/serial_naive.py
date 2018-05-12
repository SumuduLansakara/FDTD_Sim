from dim2.engine.base_engine import BaseEngine
from settings import world_width, world_height


class SerialNaiveEngine(BaseEngine):

    def update(self, n: int):
        """ Update single frame of the simulation """
        # update H fields
        self._update_Hx()
        self._update_Hy()

        # update E fields
        for x in range(world_width - 1):
            for y in range(world_height - 1):
                self._Ez[x + 1, y + 1] += self._f_Ez * (
                        self._Hy[x + 1, y + 1] - self._Hy[x, y + 1] - self._Hx[x + 1, y + 1] +
                        self._Hx[x + 1, y])

        # input from source
        self._Ez[self._src_x, self._src_y] = 1
