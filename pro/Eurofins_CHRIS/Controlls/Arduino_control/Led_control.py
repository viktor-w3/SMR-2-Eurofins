# Controlls/Arduino_control/Led_control.py

from .Command import ArduinoCommands

class LEDControl:
    def __init__(self, commands: ArduinoCommands):
        self.commands = commands

    def initialize_leds(self):
        """Initialize the LEDs."""
        self.commands.initialize_leds()

    def set_all_leds(self, color):
        """Set all LEDs to a specific color."""
        self.commands.set_all_leds(color)

    def set_led_range(self, strip_index, start_index, end_index, color):
        """Set a range of LEDs on a strip to a color."""
        self.commands.set_led_range(strip_index, start_index, end_index, color)
