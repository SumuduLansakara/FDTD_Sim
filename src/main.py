import matplotlib.figure
import matplotlib.image
import matplotlib.pyplot as plt
from matplotlib import animation
from mpi4py import MPI

from update_engine import SerialVectorEngine

_figure: matplotlib.figure.Figure = None
_im: matplotlib.image.AxesImage = None
_engine: SerialVectorEngine = None

_mpi_comm: MPI.Intracomm = None
_mpi_size: int = None
_mpi_rank: int = None


def init():
    global _mpi_comm, _mpi_rank, _mpi_size, _engine
    # init mpi
    _mpi_comm = MPI.COMM_WORLD
    _mpi_size = _mpi_comm.Get_size()
    _mpi_rank = _mpi_comm.Get_rank()
    assert _mpi_size == 2
    # init update engine
    _engine = SerialVectorEngine(_mpi_comm, _mpi_size, _mpi_rank)
    _engine.init()


def start_animation_loop():
    """ Start animation loop """
    global _im, _engine, _figure
    _figure = plt.figure()
    _im = plt.imshow(_engine.Ez, cmap='gist_gray_r', vmin=0, vmax=1)
    anim = animation.FuncAnimation(_figure, _update, interval=50)
    plt.show()


def _update(_n: int):
    global _im
    _engine.update()
    _im.set_data(_engine.Ez)
    return _im


def start():
    """ Initialize parameters and start animation """
    global _mpi_rank, _engine
    init()
    if _mpi_rank == 0:
        start_animation_loop()
    else:
        _engine.update_loop()


if __name__ == '__main__':
    start()
