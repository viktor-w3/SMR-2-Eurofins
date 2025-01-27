# Process/States_samples.py
from Config import SENSOR_TO_GRID_POSITION

class Sensor:
    def __init__(self, sensor_id, position):
        self.sensor_id = sensor_id
        self.position = position
        self.current_state = 'No_sample'  # Initial state is No_sample
        self.timer = None  # Timer is set later when state changes

    def update_state(self, new_state):
        """Update the sensor state"""
        self.current_state = new_state

def create_sensors():
    """Create and return a dictionary of Sensor objects based on grid positions"""
    sensors = {}
    for sensor_id, position in SENSOR_TO_GRID_POSITION.items():
        sensors[sensor_id] = Sensor(sensor_id, position)
        print("Initialized sensors:", sensors)
    return sensors

