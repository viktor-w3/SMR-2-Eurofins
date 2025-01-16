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
        """Send command to Arduino and print response."""
        full_command = f"{command} {param}\n"
        print(f"Sending: {full_command.strip()}")  # Print command before sending
        self.serial_connection.write(full_command.encode())
        time.sleep(0.2)  # Give Arduino time to process the command

        while True:
            response = self.serial_connection.readline().decode().strip()
            if response == "done":
                print("Arduino: done")
                break
            elif response:
                print(f"Arduino: {response}")

    def read_response(self):
        """Read the response from Arduino."""
        return self.serial_connection.readline().decode().strip()
