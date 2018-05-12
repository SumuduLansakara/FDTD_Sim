# world dimensions
world_width = 300
world_height = 300
duration = 200

epsilon0 = 1  # permittivity
mu0 = 1  # permeability
c = 1  # speed of light

# Courant stability factor
S = 1 / (2 ** 0.5)

# Spatial and temporal grid step lengths
delta_xy = 1
delta_t = S * delta_xy / c

# #Update mode
# serial_naive = 0
# serial_vectorized = 1
# parallel_pthread = 2
update_mode = 1
