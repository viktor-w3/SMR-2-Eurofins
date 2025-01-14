# Controlls/Arduino_control/utils.py

import time

def clear_buffer(arduino):
    """Helper function to reset the input buffer and add a short delay."""
    arduino.reset_input_buffer()  # Clear serial buffer
    time.sleep(0.1)
