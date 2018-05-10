import matplotlib.image

from settings import world_width, world_height


def prepare(simulation):
    pass


def finalize():
    pass


def update(simulation, n: int) -> matplotlib.image.AxesImage:
    """ Update single frame of the simulation """
    # vector operations for high single thread performance
    # update H fields
    simulation._update_Hx()
    simulation._update_Hy()

    # update E fields
    for x in range(world_width - 1):
        for y in range(world_height - 1):
            simulation._Ez[x + 1, y + 1] += simulation._f_Ez * (
                    simulation._Hy[x + 1, y + 1] - simulation._Hy[x, y + 1] - simulation._Hx[x + 1, y + 1] +
                    simulation._Hx[x + 1, y])

    # input from source
    simulation._Ez[simulation._src_x, simulation._src_y] = 1

    simulation._im.set_data(simulation._Ez)
    return simulation._im
