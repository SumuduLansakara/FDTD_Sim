import matplotlib.figure
import matplotlib.image
import matplotlib.pyplot as plt
from matplotlib import animation

from update_engine import SerialVectorEngine

_figure: matplotlib.figure.Figure = None
_im: matplotlib.image.AxesImage = None
_engine: SerialVectorEngine = None


def _init_engine():
    global _figure, _engine
    _figure = plt.figure()
    _engine = SerialVectorEngine()
    _engine.init_material()
    _engine.init_fields()


def _update(n: int):
    global _figure, _im
    _engine.update(n)
    _im.set_data(_engine.Ez)
    return _im


def _start_animation_loop():
    """ Start animation loop """
    global _im, _engine, _figure
    _im = plt.imshow(_engine.Ez, cmap='gist_gray_r', vmin=0, vmax=1)
    anim = animation.FuncAnimation(_figure, _update, interval=50)
    plt.show()


def start():
    """ Initialize parameters and start animation """
    _init_engine()
    _engine.pre_update()
    _start_animation_loop()
    _engine.post_update()


if __name__ == '__main__':
    start()
