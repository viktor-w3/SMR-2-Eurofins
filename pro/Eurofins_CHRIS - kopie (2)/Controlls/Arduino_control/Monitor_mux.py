# Controlls/Arduino_control/Monitor_mux.py

from .Mux_control import MuxControl
from .Led_control import LEDControl
import time
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP, SENSOR_TO_GRID_POSITION
from Controlls.Robot_control.Robot_grid import grid  # Import grid from Robot_grid.py

class MuxStatusTracker:
    def __init__(self, mux_control, led_control, sensor_to_mux_channel, sensor_to_led_strip, grid_ref=None):
        self.mux_control = mux_control
        self.led_control = led_control  # This should be an instance of LEDControl
        self.sensor_to_mux_channel = sensor_to_mux_channel
        self.sensor_to_led_strip = sensor_to_led_strip
        self.grid_ref = grid_ref


    def sensor_to_grid_position(self, sensor_id):
        return SENSOR_TO_GRID_POSITION.get(sensor_id)

    def run_for_next_minute(self):
        start_time = time.time()  # Record the start time
        end_time = start_time + 10  # End time after 60 seconds

        while time.time() < end_time:  # Continue until 60 seconds have passed
            self.monitor_mux_and_control_leds()  # Call your method here
            time.sleep(0.5)

    def monitor_mux_and_control_leds(self):
        """
        Monitor multiplexer channels and control LEDs based on sensor status.
        """
        for sensor_id in SENSOR_TO_MUX_CHANNEL:
            mux_number, channel_number = SENSOR_TO_MUX_CHANNEL[sensor_id]

            # Check the sensor status multiple times to get a reliable reading
            status_votes = []
            for _ in range(3):
                status = self.mux_control.read_mux_channel(mux_number, channel_number)
                if status is not None:
                    status_votes.append(status == 1)

            high_count = sum(status_votes)
            is_active = high_count >= 2  # Sensor is considered active if HIGH appears at least 2 times

            # Get LED strip indices
            strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]

            # Update LED color based on sensor status
            if is_active:
                self.led_control.set_led_range(strip_index, start_index, end_index, "Green")
            else:
                self.led_control.set_led_range(strip_index, start_index, end_index, "Red")

            # Update grid based on sensor status
            grid_position = self.sensor_to_grid_position(sensor_id)
            if grid_position:
                rij, kolom = grid_position
                if is_active:
                    grid[rij][kolom] = f"sample{sensor_id}"  # Set the sample name if active
                else:
                    grid[rij][kolom] = None  # Clear the grid if sensor is inactive


