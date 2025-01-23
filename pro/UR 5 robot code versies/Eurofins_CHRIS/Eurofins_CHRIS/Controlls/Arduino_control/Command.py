<<<<<<< HEAD
# Controlls/Arduino_control/Command.py

from .Connection import ArduinoConnection

class ArduinoCommands:
    def __init__(self, connection: ArduinoConnection):
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

    def set_all_leds(self, color: str):
        """Send command to set all LEDs to a specific color."""
        self.connection.send_command("set_all_leds", color)

    def set_led_range(self, strip_index: int, start_index: int, end_index: int, color: str):
        """Send command to set a range of LEDs on a specific strip to a color."""
        command = f"set_led_range {strip_index} {start_index} {end_index} {color}"
        self.connection.send_command(command)

    def load_bar_range(self, color, duration, strip_index, start_index, end_index):
        """Send command to display a loading bar on a specific range of LEDs."""
        self.connection.send_command("load_bar_range", f"{color} {duration} {strip_index} {start_index} {end_index}")


    def read_mux_channel(self, mux_number: int, channel_number: int) -> str:
        """Read the status of a specific MUX channel."""
        command = f"read_mux_channel {mux_number} {channel_number}"
        return self.connection.send_command(command)

    def set_mux_channel(self, mux_number: int, channel_number: int):
        """Send command to select a MUX channel."""
        command = f"set_mux_channel {mux_number} {channel_number}"
        self.connection.send_command(command)

=======
# Controlls/Arduino_control/Command.py

from .Connection import ArduinoConnection

class ArduinoCommands:
    def __init__(self, connection: ArduinoConnection):
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

    def set_all_leds(self, color: str):
        """Send command to set all LEDs to a specific color."""
        self.connection.send_command("set_all_leds", color)

    def set_led_range(self, strip_index: int, start_index: int, end_index: int, color: str):
        """Send command to set a range of LEDs on a specific strip to a color."""
        command = f"set_led_range {strip_index} {start_index} {end_index} {color}"
        self.connection.send_command(command)

    def load_bar_range(self, color, duration, strip_index, start_index, end_index):
        """Send command to display a loading bar on a specific range of LEDs."""
        self.connection.send_command("load_bar_range", f"{color} {duration} {strip_index} {start_index} {end_index}")


    def read_mux_channel(self, mux_number: int, channel_number: int) -> str:
        """Read the status of a specific MUX channel."""
        command = f"read_mux_channel {mux_number} {channel_number}"
        return self.connection.send_command(command)

    def set_mux_channel(self, mux_number: int, channel_number: int):
        """Send command to select a MUX channel."""
        command = f"set_mux_channel {mux_number} {channel_number}"
        self.connection.send_command(command)

>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
