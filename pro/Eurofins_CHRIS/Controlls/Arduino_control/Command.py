# Controlls/Arduino_control/Command.py

from .Connection import ArduinoConnection

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
