<<<<<<< HEAD
# Controlls/Arduino_control/Connection.py
import serial
import time

class ArduinoConnection:
    def __init__(self, port='COM4', baudrate=9600, timeout=0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self._connect()

    def _connect(self):
        """Connect to the Arduino and establish serial communication."""
        self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(2)  # Wait for Arduino to reset after connection
        print(f"Connected to Arduino on {self.port}")

    def send_command(self, command, param=""):
        """Send command to Arduino and return the response."""
        full_command = f"{command} {param}\n"
        print(f"Sending: {full_command.strip()}")  # Print command before sending
        self.serial_connection.write(full_command.encode())
        time.sleep(0.2)  # Give Arduino time to process the command

        # Read the response once, and handle it
        response = self.read_response()
        if response:
            print(f"Arduino: {response}")
            if response == "done":
                return response  # Return "done" if Arduino confirms completion
            return response  # Return the sensor status or other responses directly
        return None  # If no response, return None

    def read_response(self):
        """Read the response from Arduino."""
        response = self.serial_connection.readline().decode().strip()
        return response if response else None  # Return None if no valid response

    def clear_buffer(self):
        """Clear the serial buffer to ensure no stale data."""
        while self.serial_connection.in_waiting > 0:
            self.serial_connection.readline()
=======
# Controlls/Arduino_control/Connection.py
import serial
import time

class ArduinoConnection:
    def __init__(self, port='COM4', baudrate=9600, timeout=0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self._connect()

    def _connect(self):
        """Connect to the Arduino and establish serial communication."""
        self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(2)  # Wait for Arduino to reset after connection
        print(f"Connected to Arduino on {self.port}")

    def send_command(self, command, param=""):
        """Send command to Arduino and return the response."""
        full_command = f"{command} {param}\n"
        print(f"Sending: {full_command.strip()}")  # Print command before sending
        self.serial_connection.write(full_command.encode())
        time.sleep(0.2)  # Give Arduino time to process the command

        # Read the response once, and handle it
        response = self.read_response()
        if response:
            print(f"Arduino: {response}")
            if response == "done":
                return response  # Return "done" if Arduino confirms completion
            return response  # Return the sensor status or other responses directly
        return None  # If no response, return None

    def read_response(self):
        """Read the response from Arduino."""
        response = self.serial_connection.readline().decode().strip()
        return response if response else None  # Return None if no valid response

    def clear_buffer(self):
        """Clear the serial buffer to ensure no stale data."""
        while self.serial_connection.in_waiting > 0:
            self.serial_connection.readline()
>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
