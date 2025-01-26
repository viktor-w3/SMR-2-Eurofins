# Process/States_samples.py

from Config import SENSOR_TO_GRID_POSITION, SENSOR_TO_MUX_CHANNEL

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
    return sensors

def update_sensor_state(mux_control, sensor_id, sensors):
    """Update the sensor state based on multiplexer channel value"""
    mux_channel = SENSOR_TO_MUX_CHANNEL.get(sensor_id)
    if mux_channel is None:
        return  # Skip if sensor doesn't exist in the channel mapping

    mux_number, channel_number = mux_channel
    sensor_status = mux_control.read_mux_channel(mux_number, channel_number)
    # Update the sensor state based on the channel status
    if sensor_status == 0:
        sensors[sensor_id].update_state('New_sample')
    elif sensor_status == 1:
        sensors[sensor_id].update_state('No_sample')
    else:
        print(f"Invalid sensor status for {sensor_id}")

