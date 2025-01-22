# Controlls/Arduino_control/Led_control.py

class LEDControl:
    def __init__(self, commands):
        """Initializes the LEDControl class with commands."""
        self.commands = commands  # Expecting ArduinoCommands as the commands parameter

    def initialize_leds(self):
        """Initialize the LEDs."""
        self.commands.initialize_leds()

    def set_all_leds(self, color):
        """Set all LEDs to a specific color."""
        self.commands.set_all_leds(color)

    def set_led_range(self, strip_index, start_index, end_index, color):
        """Set a range of LEDs on a strip to a color."""
        self.commands.set_led_range(strip_index, start_index, end_index, color)

    def load_bar_range(self, color, duration, strip_index, start_index, end_index):
        """Send command to display a loading bar on a specific range of LEDs."""
        self.commands.load_bar_range(color, duration, strip_index, start_index, end_index)
