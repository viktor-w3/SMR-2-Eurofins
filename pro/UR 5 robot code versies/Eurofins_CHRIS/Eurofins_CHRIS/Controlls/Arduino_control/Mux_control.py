<<<<<<< HEAD
# Controlls/Arduino_control/Mux_control.py

from .Connection import ArduinoConnection
import time

class MuxControl:
    def __init__(self, connection: ArduinoConnection):
        self.connection = connection  # Using 'connection' instead of 'arduino_connection'

    def read_mux_channel(self, mux_number, channel_number):
        """Reads the status of a specific channel in a multiplexer."""
        # Clear the serial buffer to avoid stale data
        self.connection.clear_buffer()

        # Command format to read from the specific channel
        command = f"read_mux_channel {mux_number} {channel_number}"
        print(f"Sending: {command}")  # Log the command being sent
        response = self.connection.send_command(command)  # Send the command using the connection object

        if response:
            print(f"Arduino: {response}")

            # If the response is 'done', we just return None or handle success as needed.
            if response == "done":
                return None  # Return None or handle success as needed

            try:
                # If the response is a number, convert it to integer
                sensor_status = int(response)  # Convert response to integer if valid
                return sensor_status
            except ValueError:
                print(f"Unexpected response from Arduino: {response}")
                return None  # If the response is not a valid number, return None

        return None  # Return None if no valid response
=======
# Controlls/Arduino_control/Mux_control.py

from .Connection import ArduinoConnection
import time

class MuxControl:
    def __init__(self, connection: ArduinoConnection):
        self.connection = connection  # Using 'connection' instead of 'arduino_connection'

    def read_mux_channel(self, mux_number, channel_number):
        """Reads the status of a specific channel in a multiplexer."""
        # Clear the serial buffer to avoid stale data
        self.connection.clear_buffer()

        # Command format to read from the specific channel
        command = f"read_mux_channel {mux_number} {channel_number}"
        print(f"Sending: {command}")  # Log the command being sent
        response = self.connection.send_command(command)  # Send the command using the connection object

        if response:
            print(f"Arduino: {response}")

            # If the response is 'done', we just return None or handle success as needed.
            if response == "done":
                return None  # Return None or handle success as needed

            try:
                # If the response is a number, convert it to integer
                sensor_status = int(response)  # Convert response to integer if valid
                return sensor_status
            except ValueError:
                print(f"Unexpected response from Arduino: {response}")
                return None  # If the response is not a valid number, return None

        return None  # Return None if no valid response
>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
