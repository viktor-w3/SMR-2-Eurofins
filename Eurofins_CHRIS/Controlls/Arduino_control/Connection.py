# Controlls/Arduino_control/Connection.py
import serial
import time
import serial.tools.list_ports


class ArduinoConnection:
    def __init__(self, port='COM4', baudrate=9600, timeout=0.1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self._connect()

    def _connect(self):
        """Connect to the Arduino and establish serial communication."""
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Wait for Arduino to reset after connection
            print(f"Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino on {self.port}: {e}")
            self.serial_connection = None

    def send_command(self, command, param="", response_timeout=0.2):
        """Send command to Arduino and return the response."""
        if not self.serial_connection or not self.serial_connection.is_open:
            print("No active serial connection.")
            return None

        full_command = f"{command} {param}\n"
        self.clear_buffer()  # Clear any stale data
        print(f"Sending: {full_command.strip()}")
        self.serial_connection.write(full_command.encode())
        time.sleep(response_timeout)  # Wait for Arduino to process the command
        return self.read_response()

    def read_response(self):
        """Read the response from Arduino."""
        if not self.serial_connection or not self.serial_connection.is_open:
            return None
        response = self.serial_connection.readline().decode().strip()
        return response if response else None  # Return None if no valid response

    def clear_buffer(self):
        """Clear the serial buffer to ensure no stale data."""
        if self.serial_connection:
            while self.serial_connection.in_waiting > 0:
                self.serial_connection.readline()

    def disconnect(self):
        """Close the serial connection gracefully."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Disconnected from Arduino on {self.port}")

    @staticmethod
    def list_ports():
        """List all available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
