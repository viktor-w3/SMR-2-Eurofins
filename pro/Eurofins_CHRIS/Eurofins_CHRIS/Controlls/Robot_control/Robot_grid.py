<<<<<<< HEAD
# Controlls/Robot_control/Robot_grid.py

# Grid-instelling
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
grid[2][0] = "sample1"

# Functie om grid-positie naar coördinaten te converteren
def grid_to_coordinates(rij, kolom):
    x_base, y_base, z_base = -0.15, -0.203, 0.064  # Basispunt van het grid of -0.150 -0.637
    z_step, y_step = 0.172, 0.224  # Afstanden tussen gridpunten
    #van het midde kan die 85mm omhoog moet je onder blijven
    x = x_base
    y = y_base + (kolom * y_step)
    z = z_base + (rij * z_step)
=======
# Controlls/Robot_control/Robot_grid.py

# Grid-instelling
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
grid[2][0] = "sample1"

# Functie om grid-positie naar coördinaten te converteren
def grid_to_coordinates(rij, kolom):
    x_base, y_base, z_base = -0.15, -0.203, 0.064  # Basispunt van het grid of -0.150 -0.637
    z_step, y_step = 0.172, 0.224  # Afstanden tussen gridpunten
    #van het midde kan die 85mm omhoog moet je onder blijven
    x = x_base
    y = y_base + (kolom * y_step)
    z = z_base + (rij * z_step)
>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
    return [x, y, z]