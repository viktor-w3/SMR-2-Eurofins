# Controlls/Arduino_control/Monitor_mux.py
# Controlls/Arduino_control/Monitor_mux.py

from .Mux_control import MuxControl
from .Led_control import LEDControl
import time
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP, SENSOR_TO_GRID_POSITION
from Controlls.Robot_control.Robot_grid import grid  # Import grid from Robot_grid.py
class MuxStatusTracker:
    def __init__(self, mux_control, led_control, sensor_to_mux_channel, sensor_to_led_strip, grid_ref=None):
        self.mux_control = mux_control
        self.led_control = led_control
        self.sensor_to_mux_channel = sensor_to_mux_channel
        self.sensor_to_led_strip = sensor_to_led_strip
        self.grid_ref = grid_ref

    def sensor_to_grid_position(self, sensor_id):
        return SENSOR_TO_GRID_POSITION.get(sensor_id)

    def monitor_mux_and_control_leds(self, gui, sensors):
        """
        Monitor multiplexer channels and control LEDs based on sensor status.
        Also updates the sensor state and the grid.
        """
        previous_grid_state = [row[:] for row in grid]

        for sensor_id in SENSOR_TO_MUX_CHANNEL:
            mux_number, channel_number = SENSOR_TO_MUX_CHANNEL[sensor_id]

            # Check the sensor status multiple times to get a reliable reading
            status_votes = []
            for _ in range(1):
                status = self.mux_control.read_mux_channel(mux_number, channel_number)
                if status is not None:
                    status_votes.append(status == 1)

            high_count = sum(status_votes)
            is_active = high_count >= 1  # Sensor is considered active if HIGH appears at least 2 times

            # Update LED color based on sensor status
            strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
            if is_active:
                self.led_control.set_led_range(strip_index, start_index, end_index, "Green")
                sensors[sensor_id].update_state('New_sample')
            else:
                self.led_control.set_led_range(strip_index, start_index, end_index, "Red")
                sensors[sensor_id].update_state('No_sample')

            # Update grid based on sensor status
            grid_position = self.sensor_to_grid_position(sensor_id)
            if grid_position:
                rij, kolom = grid_position  # Using 'rij' for row and 'kolom' for column
                if not is_active:
                    # Only update the grid if the sensor is not active
                    grid[rij][kolom] = f"sample{sensor_id}"  # Set the sample name if inactive

                # Update the GUI grid color
                color = "Red" if is_active else "Green"
                # gui.update_sensor_status(sensor_id, color)

        # Compare the current grid with the previous state and log updates
        for rij, (prev_row, curr_row) in enumerate(zip(previous_grid_state, grid)):
            for kolom, (prev_cell, curr_cell) in enumerate(zip(prev_row, curr_row)):
                if prev_cell != curr_cell:
                    if curr_cell:
                        print(f"Grid updated: Added {curr_cell} at position ({rij}, {kolom}).")
                    else:
                        print(f"Grid updated: Cleared position ({rij}, {kolom}).")

