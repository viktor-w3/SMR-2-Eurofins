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
        ("set_strip_leds", "0 Blue"),  # Set LEDs of strip 1 to Blue
        ("set_led", "0 5 Green"),  # Set LED 5 on strip 0 to Green
        ("load_bar", "Yellow 5000 0"),  # Run loading bar on strip 0 for 5 seconds
        ("servo_off", "")  # Move the servo back to 0 degrees
    ]

    # Send each command in sequence
    for command, param in commands:
        send_command(command, param)


if __name__ == "__main__":
    print("Starting the program...")
    execute_sequence()
    print("Program finished.")
