import serial
import time

# Connect to the Arduino (adjust COM port)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1)  # Adjust COM4 to your port
time.sleep(2)  # Wait for the Arduino to reset
arduino.reset_input_buffer() # Clear serial buffer

def send_command(command, param=""):
    full_command = f"{command} {param}\n"
    arduino.write(full_command.encode())
    print(f"Sent: {full_command.strip()}")
    time.sleep(0.1)  # Add delay before waiting for a response

    while True:
        response = arduino.readline().decode().strip()
        if response == "done":
            print("Arduino: done")
            break
        elif response:
            print(f"Arduino: {response}")


def execute_sequence():
    """Execute a sequence of commands."""

    # Define the sequence of commands to send
    commands = [
        ("initialize_servo", ""),  # Initialize the servo
        ("servo_on", ""),  # Move servo to 90 degrees
        ("initialize_leds", ""),  # Initialize LEDs
        ("set_all_leds", "Red"),  # Set all LEDs to Red
        ("set_strip_leds", "0 Blue"),  # Set LEDs of strip 0 to Blue
        ("set_led_range", "0 0 9 Red"),  # Set LEDs 0-9 on strip 0 to Red
        ("load_bar_range", "Yellow 5000 0 10 20"),  # 5 second Yellow load bar on LEDs 10-20 on strip 0
        ("servo_off", ""),  # Move the servo back to 0 degrees
    ]

    # Send each command in sequence
    for command, param in commands:
        send_command(command, param)

def execute_sequence2():
    """Execute a sequence of commands."""

    # Define the sequence of commands to send
    commands = [
        ("servo_on", ""),  # Move servo to 90 degrees
        ("servo_off", ""),  # Move the servo back to 0 degrees
        ("initialize_leds", ""),  # Initialize LEDs
        ("load_bar_range", "Green 5000 0 0 30"),  # 5 second Green load bar on LEDs 10-20 on strip 0
        ("set_all_leds", "Black")
]
    for command, param in commands:
        send_command(command, param)
#Command breakdown
"""
initialize_servo: Initializes the servo motor.

servo_on: Moves the servo to 90 degrees.

servo_off: Moves the servo back to 0 degrees.

initialize_leds: Initializes the LEDs on the Arduino side.

set_all_leds {color}: Sets all LEDs on all strips to the given color (Red, Blue, etc.).

set_strip_leds {stripIndex} {color}: Sets all LEDs on the given strip index to the specified color.

set_led_range {stripIndex} {startIndex} {endIndex} {color}: Sets a range of LEDs on a specific strip to a color.

load_bar_range {color} {duration} {stripIndex} {startIndex} {endIndex}: Creates a loading bar effect by lighting LEDs from start index to end index on a specific strip with a duration.

# broken blink single {stripIndex} {ledIndex} {color} {speed}: Blinks a single LED on a strip with a specific color and speed.

# broken blink all {stripIndex} {color} {speed}: Blinks all LEDs on a strip with a specified color and speed.

# broken blink range {stripIndex} {startLed} {endLed} {color} {speed}: Blinks a range of LEDs on a strip with a specified color and speed.
"""
if __name__ == "__main__":
    print("Starting the program 1...")
    execute_sequence()
    time.sleep(5)
    print("Starting the program 2 ...")
    execute_sequence2()

    print("Program finished.")
