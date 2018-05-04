# world dimensions
world_width = 500
world_height = 500
duration = 200

# source coordinates
src_x = 250
src_y = 250

epsilon0 = 1  # permittivity
mu0 = 1  # permeability
c = 1  # speed of light

# Courant stability factor
S = 1 / (2 ** 0.5)

# Spatial and temporal grid step lengths
delta = 1
deltat = S * delta / c
