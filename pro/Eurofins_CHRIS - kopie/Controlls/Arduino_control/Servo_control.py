# Controlls/Arduino_control/Servo_control.py

from .Command import ArduinoCommands

class ServoControl:
    def __init__(self, commands: ArduinoCommands):
        self.commands = commands

    def initialize_servo(self):
        """Initialize the servo."""
        self.commands.initialize_servo()

    def servo_on(self):
        """Turn the servo on and move to 90 degrees."""
        self.commands.servo_on()

    def servo_off(self):
        """Turn the servo off and return to 0 degrees."""
        self.commands.servo_off()
