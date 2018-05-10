import threading

import matplotlib.image

from settings import world_width, world_height

_update_hx_event: threading.Event = None
_update_hy_event: threading.Event = None
_thread_Hx: threading.Event = None
_thread_Hy: threading.Event = None


def prepare(simulation):
    global _update_hx_event, _update_hy_event, _thread_Hx, _thread_Hy
    _update_hx_event = threading.Event()
    _update_hy_event = threading.Event()
    _update_hx_event.set()
    _update_hy_event.set()
    _thread_Hx = threading.Thread(target=_start_update_Hx_loop, args=(simulation,))
    _thread_Hy = threading.Thread(target=_start_update_Hy_loop, args=(simulation,))
    _thread_Hx.start()
    _thread_Hy.start()


def finalize():
    global _thread_Hx, _thread_Hy
    _thread_Hx.join()
    _thread_Hy.join()


def update(simulation, n: int) -> matplotlib.image.AxesImage:
    """ update single frame of the simulation """
    global _update_hx_event, _update_hy_event, _thread_Hx, _thread_Hy
    # wait for H fields to be updated for the current iteration
    while _update_hx_event.is_set() and _update_hy_event.is_set():
        continue

    # update E fields
    for x in range(world_width - 1):
        for y in range(world_height - 1):
            simulation._Ez[x + 1, y + 1] += simulation._f_Ez * (
                    simulation._Hy[x + 1, y + 1] - simulation._Hy[x, y + 1] - simulation._Hx[x + 1, y + 1] +
                    simulation._Hx[x + 1, y])

    # input from source
    simulation._Ez[simulation._src_x, simulation._src_y] = 1
    _update_hx_event.set()
    _update_hy_event.set()

    simulation._im.set_data(simulation._Ez)
    return simulation._im


def _start_update_Hy_loop(simulation):
    while True:
        _update_hy_event.wait()
        simulation._update_Hy()
        _update_hy_event.clear()


def _start_update_Hx_loop(simulation):
    while True:
        _update_hx_event.wait()
        simulation._update_Hx()
        _update_hx_event.clear()
