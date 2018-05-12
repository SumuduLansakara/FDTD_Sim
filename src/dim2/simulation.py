import matplotlib.figure
import matplotlib.image
import matplotlib.pyplot as plt
from matplotlib import animation

from dim2.engine.base_engine import BaseEngine
from dim2.engine.parallel_pthread import PthreadEngine
from dim2.engine.serial_naive import SerialNaiveEngine
from dim2.engine.serial_vector import SerialVectorEngine
from settings import *


class Simulation:
    def __init__(self):
        # plot
        self._figure: matplotlib.figure.Figure = None
        self._im: matplotlib.image.AxesImage = None

        self._engine: BaseEngine = None

    def _init_engine(self):
        """ Initialize field update method depending on the setting """
        self._figure = plt.figure()
        if update_mode == 0:
            print("update mode = serial_naive")
            self._figure.suptitle("serial_naive")
            self._engine = SerialNaiveEngine()
        elif update_mode == 1:
            print("update mode = serial_vectorized")
            self._figure.suptitle("serial_vector")
            self._engine = SerialVectorEngine()
        elif update_mode == 2:
            print("update mode = parallel")
            self._figure.suptitle("parallel_pthread")
            self._engine = PthreadEngine()
        else:
            raise NotImplementedError("Invalid update mode {}".format(update_mode))
        self._engine.init_material()
        self._engine.init_fields()

    def _update(self, n: int):
        self._engine.update(n)
        self._im.set_data(self._engine.Ez)
        return self._im

    def _start_animation_loop(self):
        """ Start animation loop """
        self._im = plt.imshow(self._engine.Ez, cmap='gist_gray_r', vmin=0, vmax=1)
        anim = animation.FuncAnimation(self._figure, self._update, interval=50)
        plt.show()

    def start(self):
        """ Initialize parameters and start animation """
        self._init_engine()
        self._engine.pre_update()
        self._start_animation_loop()
        self._engine.post_update()
