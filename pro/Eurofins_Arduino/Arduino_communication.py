import serial
import time

# Connect to the Arduino (adjust COM port)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=0.1)  # Adjust COM4 to your port
time.sleep(2)  # Wait for the Arduino to reset


def clear_buffer():
    """Helper function to reset the input buffer and add a short delay."""
    arduino.reset_input_buffer()  # Clear serial buffer
    time.sleep(0.1)


def send_command(command, param=""):
    """Send a command to the Arduino and print the response."""
    full_command = f"{command} {param}\n"
    print(f"Sending: {full_command.strip()}")  # Print the command before sending
    arduino.write(full_command.encode())
    time.sleep(0.2)  # Increased delay to ensure Arduino can process the command

    while True:
        response = arduino.readline().decode().strip()
        if response == "done":
            print("Arduino: done")
            break
        elif response:
            print(f"Arduino: {response}")


# Servo and LED control functions
def initialize_servo():
    """Send command to initialize the servo."""
    send_command("initialize_servo")


def servo_on():
    """Send command to move the servo to 90 degrees."""
    send_command("servo_on")


def servo_off():
    """Send command to move the servo back to 0 degrees."""
    send_command("servo_off")


def initialize_leds():
    """Send command to initialize the LEDs."""
    send_command("initialize_leds")


def set_all_leds(color):
    """Send command to set all LEDs to a specific color."""
    send_command("set_all_leds", color)


def set_led_range(strip_index, start_index, end_index, color):
    """Send command to set a range of LEDs on a specific strip to a color."""
    send_command("set_led_range", f"{strip_index} {start_index} {end_index} {color}")


def load_bar_range(color, duration, strip_index, start_index, end_index):
    """Send command to display a loading bar on a specific range of LEDs."""
    send_command("load_bar_range", f"{color} {duration} {strip_index} {start_index} {end_index}")

class MuxStatusTracker:
    """A class to track and update the status of multiplexer channels."""

    def __init__(self):
        self.channel_status = {}

    def read_mux_channel_status(self, mux_number, channel_number):
        """Read the status of a specific channel in a multiplexer."""
        clear_buffer()
        command = f"read_mux_channel {mux_number} {channel_number}"
        arduino.write(f"{command}\n".encode())
        time.sleep(0.2)

        while True:
            response = arduino.readline().decode().strip()
            if response == "done":
                print("Arduino: done")
                break
            elif response:
                print(f"Arduino: {response}")
                return int(response)  # Convert and return response as integer
        return None  # Return None if no valid response


def monitor_mux_and_control_leds():
    """Monitor multiplexer channels and control corresponding LEDs."""
    mux_tracker = MuxStatusTracker()

    sensor_to_mux_channel = {
        0: (1, 0), 1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (1, 4),
        5: (0, 0), 6: (0, 1), 7: (0, 2), 8: (0, 3)
    }

    sensor_to_led_strip = {
        0: (0, 0, 9), 1: (0, 10, 19), 2: (0, 20, 29),
        3: (1, 0, 9), 4: (1, 10, 20), 5: (1, 21, 29),
        6: (2, 0, 9), 7: (2, 10, 19), 8: (2, 20, 29)
    }

    for sensor_id in range(9):
        print(f"Checking sensor {sensor_id}...")

        # Map sensor ID to multiplexer and channel
        mux_number, channel_number = sensor_to_mux_channel[sensor_id]

        # Read the status of the channel
        sensor_status = mux_tracker.read_mux_channel_status(mux_number, channel_number)

        if sensor_status is None:
            print(f"Sensor {sensor_id} failed to respond or invalid.")
            continue

        # Map the sensor to LED strip indices
        led_strip, start_led, end_led = sensor_to_led_strip[sensor_id]

        # Act based on sensor status
        if sensor_status == 0:
            print(f"Sensor {sensor_id} is LOW. Turning LEDs red.")
            set_led_range(led_strip, start_led, end_led, "Red")
        elif sensor_status == 1:
            print(f"Sensor {sensor_id} is HIGH. Turning LEDs off.")
            set_led_range(led_strip, start_led, end_led, "Green")


# Main program logic
if __name__ == "__main__":
    print("Starting the program...")

    # Initialize servo and LEDs
    clear_buffer()
    initialize_servo()
    servo_on()
    initialize_leds()
    time.sleep(0.3)
    """
    # LED control and effects
    set_all_leds("Red")
    time.sleep(0.3)
    set_all_leds("Black")
    time.sleep(0.3)

    # Display loading bars
    load_bar_range("Yellow", 1000, 0, 0, 29)
    time.sleep(0.3)
    set_led_range(0, 0, 29, "Yellow")
    time.sleep(0.3)

    load_bar_range("Yellow", 1000, 1, 0, 29)
    time.sleep(0.3)
    set_led_range(1, 0, 29, "Yellow")
    time.sleep(0.3)

    load_bar_range("Yellow", 1000, 2, 0, 29)
    time.sleep(0.3)
    set_led_range(2, 0, 29, "Yellow")
    time.sleep(0.3)

    set_led_range(2, 10, 20, "Green")
    time.sleep(0.3)
    set_all_leds("Black")"""
    clear_buffer()

    # Monitor MUX and control LEDs based on the status
    #mux_tracker = MuxStatusTracker()
    #mux_tracker.read_mux_channel_status(1, 2)
    time.sleep(0.3)

    # Monitor MUX status and control LEDs
    #while True:
     #monitor_mux_and_control_leds()
    # Turn off servo at the end
     #servo_on()
     #time.sleep(0.6)
     #set_all_leds("Black")
     #servo_off()
     #monitor_mux_and_control_leds()
    #print("Program finished.")
