import serial
import time

# Connect to the Arduino (adjust COM port)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)  # Adjust COM4 to your port
time.sleep(2)  # Wait for the Arduino to reset
arduino.reset_input_buffer() # Clear serial buffer

def send_command(command, param=""):
    full_command = f"{command} {param}\n"
    print(f"Sending: {full_command.strip()}")  # Print the command before sending
    arduino.write(full_command.encode())
    #print(f"Sent: {full_command.strip()}")
    time.sleep(0.1)  # Add delay before waiting for a response

    while True:
        response = arduino.readline().decode().strip()
        if response == "done":
            print("Arduino: done")
            break
        elif response:
            print(f"Arduino: {response}")

def initialize_servo():
    """Send command to initialize the servo."""
    send_command("initialize_servo")

def servo_on():
    """Send command to move the servo to 90 degrees."""
    send_command("servo_on")


def servo_off():
    """Send command to move the servo back to 0 degrees."""
    send_command("servo_off")


# LED control functions
def initialize_leds():
    """Send command to initialize the LEDs."""
    send_command("initialize_leds")


def set_all_leds(color):
    """Send command to set all LEDs to a specific color."""
    send_command("set_all_leds", color)


def set_strip_leds(strip_index, color):
    """Send command to set all LEDs on a specific strip to a color."""
    send_command("set_strip_leds", f"{strip_index} {color}")


def set_led_range(strip_index, start_index, end_index, color):
    """Send command to set a range of LEDs on a specific strip to a color."""
    send_command("set_led_range", f"{strip_index} {start_index} {end_index} {color}")


def load_bar_range(color, duration, strip_index, start_index, end_index):
    """Send command to display a loading bar on a specific range of LEDs."""
    send_command("load_bar_range", f"{color} {duration} {strip_index} {start_index} {end_index}")


class MuxStatusTracker:
    """
    A class to track and update the status of multiplexer channels.
    """

    def __init__(self):
        # Dictionary to hold the status of each mux channel
        self.channel_status = {}

    def read_mux_channel_status(self, mux_number, channel_number):
        """
        Send a command to read the status of a specific channel in a multiplexer,
        and update the stored status.
        """
        arduino.reset_input_buffer()  # Clear serial buffer
        time.sleep(0.1)
        send_command(f"read_mux_channel {mux_number} {channel_number}")

        while True:
            response = arduino.readline().decode().strip()
            if response.startswith(f"MUX{mux_number} Channel {channel_number}"):
                # Parse the value from the response
                value = response.split(": ")[1]
                print(f"Received response from MUX{mux_number} Channel {channel_number}: {value}")
                key = f"MUX{mux_number}_CH{channel_number}"
                self.channel_status[key] = value
                return value
            elif response == "done":
                break

    def get_channel_status(self, mux_number, channel_number):
        """
        Retrieve the stored status of a specific channel.

        Args:
            mux_number (int): The multiplexer number.
            channel_number (int): The channel number.

        Returns:
            str: The stored status ('HIGH', 'LOW', or 'UNKNOWN' if not read yet).
        """
        key = f"MUX{mux_number}_CH{channel_number}"
        return self.channel_status.get(key, "UNKNOWN")

def read_mux_status(mux_number):
    """Send command to read the status of the multiplexer."""
    if mux_number == 0:
        arduino.reset_input_buffer()  # Clear serial buffer
        time.sleep(0.1)
        send_command("read_mux0")
    elif mux_number == 1:
        arduino.reset_input_buffer()  # Clear serial buffer
        time.sleep(0.1)
        send_command("read_mux1")
    elif mux_number == 2:
        arduino.reset_input_buffer()  # Clear serial buffer
        time.sleep(0.1)
        send_command("read_mux2")
    else:
        print("Invalid multiplexer number!")

#Command breakdown in command chain
"""
"initialize_servo", "" : Initializes the servo motor.
"servo_on", "": Moves the servo to 90 degrees.
"servo_off", "": Moves the servo back to 0 degrees.

"initialize_leds", "": Initializes the LEDs on the Arduino side.
"set_all_leds", "color": Sets all LEDs on all strips to the given color (Red, Blue, etc.).
"set_strip_leds","stripIndex color": Sets all LEDs on the given strip index to the specified color.
"set_led_range", "stripIndex startIndex endIndex color": Sets a range of LEDs on a specific strip to a color.
"load_bar_range", "color duration stripIndex startIndex endIndex": Creates a loading bar effect by lighting LEDs from start index to end index on a specific strip with a duration.

"""
#Command breakdown as def
"""
initialize_servo() #Initializes servo motor.
servo_on() #Moves servo to 90 degrees.
servo_off() #Moves servo back to 0 degrees.
initialize_leds() #Initializes all LEDs on the Arduino side.
set_all_leds(color) #Sets all LEDs on all strips to the given color.
# currently broken set_strip_leds(strip_index, color) #Sets all LEDs on the given strip index to the specified color.
set_led_range(strip_index, start_index, end_index, color) #Sets a range of LEDs on a specific strip to a color.
load_bar_range(color, duration, strip_index, start_index, end_index) #Creates a loading bar effect by lighting LEDs from start index to end index on a specific strip with a duration.
read_mux_status(muxIndex) #Reads all channels on specified MUX
read_mux_channel_status(1, 3) #Read specific channel on specified MUX (MUX1 channel 3)
"""

if __name__ == "__main__":
    #"""
    print("Starting the program 1...")
    initialize_servo()
    servo_on()
    initialize_leds()
    time.sleep(0.3)
    set_all_leds("Red")
    time.sleep(0.3)
    set_all_leds("Black")
    time.sleep(0.3)
    load_bar_range("Yellow", 1000, 0, 0, 30)
    set_led_range(0, 0, 30, "Yellow")
    time.sleep(0.3)

    load_bar_range("Yellow", 1000, 1, 0, 30)
    set_led_range(1, 0, 30, "Yellow")
    time.sleep(0.3)

    load_bar_range("Yellow", 1000, 2, 0, 30)
    set_led_range(2, 0, 30, "Yellow")
    time.sleep(0.3)

    set_led_range(2, 10, 20, "Green")
    time.sleep(0.3)
    set_all_leds("Black")
    arduino.reset_input_buffer()  # Clear serial buffer
    time.sleep(0.3)

    mux_tracker = MuxStatusTracker()
    mux_tracker.read_mux_channel_status(1, 2)
    time.sleep(0.3)
    read_mux_status(0)
    time.sleep(0.3)
    read_mux_status(1)
    servo_off()
    print("Starting the program 2 ...") # """
    #execute_sequence1()

    print("Program finished.")
