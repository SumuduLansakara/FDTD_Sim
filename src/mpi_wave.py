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


def init_mpi():
    global _mpi_comm, _mpi_rank, _mpi_size
    _mpi_comm = MPI.COMM_WORLD
    _mpi_size = _mpi_comm.Get_size()
    _mpi_rank = _mpi_comm.Get_rank()


def init_engine():
    global _engine
    _engine = SerialVectorEngine()
    _engine.init()


def start_animation_loop():
    """ Start animation loop """
    global _im, _engine, _figure
    _figure = plt.figure()
    _im = plt.imshow(_engine.Ez, cmap='gist_gray_r', vmin=0, vmax=1)
    anim = animation.FuncAnimation(_figure, _update, interval=50)
    plt.show()


def _update(n: int):
    global _im
    _engine.update(n)
    _im.set_data(_engine.Ez)
    return _im


def start():
    """ Initialize parameters and start animation """
    init_mpi()
    init_engine()
    start_animation_loop()


if __name__ == '__main__':
    start()
