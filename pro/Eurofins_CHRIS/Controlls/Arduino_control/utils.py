# Controlls/Arduino_control/utils.py

import time

# utils.py

def clear_buffer(arduino_commands):
    # Ensure that arduino_commands has access to the serial instance
    if hasattr(arduino_commands, 'serial') and hasattr(arduino_commands.serial, 'reset_input_buffer'):
        arduino_commands.serial.reset_input_buffer()  # Clear serial buffer
    else:
        print("Error: The ArduinoCommands object does not have access to the serial buffer.")

