import threading

from dim2.engine.base_engine import BaseEngine
from settings import world_width, world_height


class PthreadEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        self._update_hx_event: threading.Event = None
        self._update_hy_event: threading.Event = None
        self._thread_Hx: threading.Thread = None
        self._thread_Hy: threading.Thread = None

    def pre_update(self):
        self._update_hx_event = threading.Event()
        self._update_hy_event = threading.Event()
        self._update_hx_event.set()
        self._update_hy_event.set()
        self._thread_Hx = threading.Thread(target=self._start_update_Hx_loop)
        self._thread_Hy = threading.Thread(target=self._start_update_Hy_loop)
        self._thread_Hx.start()
        self._thread_Hy.start()

    def post_update(self):
        self._thread_Hx.join()
        self._thread_Hy.join()

    def update(self, n: int):
        """ update single frame of the simulation """
        # wait for H fields to be updated for the current iteration
        while self._update_hx_event.is_set() and self._update_hy_event.is_set():
            continue

        # update E fields
        for x in range(world_width - 1):
            for y in range(world_height - 1):
                self._Ez[x + 1, y + 1] += self._f_Ez * (
                        self._Hy[x + 1, y + 1] - self._Hy[x, y + 1] - self._Hx[x + 1, y + 1] +
                        self._Hx[x + 1, y])

        # input from source
        self._Ez[self._src_x, self._src_y] = 1
        self._update_hx_event.set()
        self._update_hy_event.set()

    def _start_update_Hy_loop(self):
        while True:
            self._update_hy_event.wait()
            self._update_Hy()
            self._update_hy_event.clear()

    def _start_update_Hx_loop(self):
        while True:
            self._update_hx_event.wait()
            self._update_Hx()
            self._update_hx_event.clear()
