# Controlls/Arduino_control/Command.py

from .Connection import ArduinoConnection
from .Mux_control import MuxControl
from .Led_control import LEDControl

class ArduinoCommands:
    def __init__(self, connection):
        self.connection = connection

    def initialize_servo(self):
        """Send command to initialize the servo."""
        self.connection.send_command("initialize_servo")

    def servo_on(self):
        """Send command to move the servo to 90 degrees."""
        self.connection.send_command("servo_on")

    def servo_off(self):
        """Send command to move the servo back to 0 degrees."""
        self.connection.send_command("servo_off")

    def initialize_leds(self):
        """Send command to initialize the LEDs."""
        self.connection.send_command("initialize_leds")

    def set_all_leds(self, color):
        """Send command to set all LEDs to a specific color."""
        self.connection.send_command("set_all_leds", color)

    def set_led_range(self, strip_index, start_index, end_index, color):
        """Send command to set a range of LEDs on a specific strip to a color."""
        self.connection.send_command("set_led_range", f"{strip_index} {start_index} {end_index} {color}")

    def load_bar_range(self, color, duration, strip_index, start_index, end_index):
        """Send command to display a loading bar on a specific range of LEDs."""
        self.connection.send_command("load_bar_range", f"{color} {duration} {strip_index} {start_index} {end_index}")

    def read_mux_channel(self, mux_number, channel_number):
        """Read the status of a specific channel in the multiplexer."""
        command = f"read_mux_channel {mux_number} {channel_number}"
        return self.connection.send_command(command)

    def set_mux_channel(self, mux_number, channel_number):
        """Send command to select a multiplexer channel."""
        command = f"set_mux_channel {mux_number} {channel_number}"
        self.connection.send_command(command)

# MuxStatusTracker: Handles the monitoring of MUX and controlling LEDs
class MuxStatusTracker:
    def __init__(self, mux_control: MuxControl, led_control: LEDControl):
        self.mux_control = mux_control
        self.led_control = led_control

    def monitor_mux_and_control_leds(self):
        """Monitor multiplexer channels and control corresponding LEDs."""
        sensor_to_mux_channel = {
            0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (1, 4),
            5: (0, 0), 6: (0, 1), 7: (0, 2), 8: (0, 3)
        }

        sensor_to_led_strip = {
            0: (0, 0, 9), 1: (0, 10, 19), 2: (0, 20, 29),
            3: (1, 0, 9), 4: (1, 10, 20), 5: (1, 21, 29),
            6: (2, 0, 9), 7: (2, 10, 19), 8: (2, 20, 29)
        }

        # Loop through each sensor and monitor its status
        for sensor_id in range(9):
            mux_number, channel_number = sensor_to_mux_channel[sensor_id]
            # Read the status of the MUX channel
            status = self.mux_control.read_mux_channel(mux_number, channel_number)

            # Assuming the status of the sensor will be '1' for active and '0' for inactive
            if status == '1':  # Active sensor
                strip_index, start_index, end_index = sensor_to_led_strip[sensor_id]
                self.led_control.set_led_range(strip_index, start_index, end_index, "Green")  # Turn LEDs Green
            elif status == '0':  # Inactive sensor
                strip_index, start_index, end_index = sensor_to_led_strip[sensor_id]
                self.led_control.set_led_range(strip_index, start_index, end_index, "Black")  # Turn LEDs off
            else:
                print(f"Error: Unexpected sensor status for sensor {sensor_id}: {status}")
