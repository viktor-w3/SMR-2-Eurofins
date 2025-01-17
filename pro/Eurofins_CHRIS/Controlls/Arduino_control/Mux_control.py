# Controlls/Arduino_control/Mux_control.py

from .Connection import ArduinoConnection

class MuxControl:
    def __init__(self, connection: ArduinoConnection):
        self.connection = connection

    def read_mux_channel(self, mux_number, channel_number):
        """Read the status of a specific channel in the multiplexer."""
        command = f"read_mux_channel {mux_number} {channel_number}"
        response = self.connection.send_command(command)  # This now returns the response
        return response  # Return the response (e.g., '1' or '0')

    def set_mux_channel(self, mux_number, channel_number):
        """Send command to select a multiplexer channel."""
        command = f"set_mux_channel {mux_number} {channel_number}"
        self.connection.send_command(command)
