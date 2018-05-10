# world dimensions
world_width = 100
world_height = 100
duration = 200

epsilon0 = 1  # permittivity
mu0 = 1  # permeability
c = 1  # speed of light

# Courant stability factor
S = 1 / (2 ** 0.5)

# Spatial and temporal grid step lengths
delta = 1
deltat = S * delta / c
