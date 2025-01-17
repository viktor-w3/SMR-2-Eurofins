<<<<<<< HEAD
# Controlls/Arduino_control/utils.py

import time

# utils.py

def clear_buffer(arduino_commands):
    # Ensure that arduino_commands has access to the serial instance
    if hasattr(arduino_commands, 'serial') and hasattr(arduino_commands.serial, 'reset_input_buffer'):
        arduino_commands.serial.reset_input_buffer()  # Clear serial buffer
    else:
        print("Error: The ArduinoCommands object does not have access to the serial buffer.")

=======
# Controlls/Arduino_control/utils.py

import time

# utils.py

def clear_buffer(arduino_commands):
    # Ensure that arduino_commands has access to the serial instance
    if hasattr(arduino_commands, 'serial') and hasattr(arduino_commands.serial, 'reset_input_buffer'):
        arduino_commands.serial.reset_input_buffer()  # Clear serial buffer
    else:
        print("Error: The ArduinoCommands object does not have access to the serial buffer.")

>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
