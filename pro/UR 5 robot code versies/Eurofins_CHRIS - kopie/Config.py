# Config.py

SENSOR_TO_MUX_CHANNEL = {
    0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (1, 4),
    5: (0, 0), 6: (0, 1), 7: (0, 2), 8: (0, 3)
}

SENSOR_TO_LED_STRIP = {
    0: (0, 0, 9), 1: (0, 10, 19), 2: (0, 20, 29),
    3: (1, 0, 9), 4: (1, 10, 20), 5: (1, 21, 29),
    6: (2, 0, 9), 7: (2, 10, 19), 8: (2, 20, 29)
}

# Mapping sensor IDs to grid positions
SENSOR_TO_GRID_POSITION = {
    8: (0, 0), 7: (0, 1), 6: (0, 2),
    5: (1, 0), 4: (1, 1), 3: (1, 2),
    2: (2, 0), 1: (2, 1), 0: (2, 2)
}
