# main.py

# Import necessary classes and functions from other files
from Controlls.Arduino_control.Connection import ArduinoConnection
from Controlls.Arduino_control.Mux_control import MuxControl
from Process.Robot_process import process_sensors
from Process.States_samples import create_sensors
from Controlls.GUI_control import EurofinsGUI  # Assuming this is the correct path
from Controlls.Arduino_control.Led_control import LEDControl  # Assuming this is the correct path
import tkinter as tk

from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
from Controlls.Arduino_control.Mux_control import MuxControl
from Controlls.Robot_control.Robot_grid import grid, grid_to_coordinates
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Command import ArduinoCommands
from Controlls.Robot_control import IO_commands
from Controlls.Arduino_control.Led_control import LEDControl
from Config import SENSOR_TO_GRID_POSITION
from Controlls.Arduino_control import ArduinoConnection  # Assuming you have a class for Arduino connection
#from Process.Robot_process import process_samples
from Controlls.GUI_control import EurofinsGUI  # Assuming your GUI class is in EurofinsGUI.py


def setup_arduino():
    """Set up the Arduino connection and return the connection object."""
    try:
        # Establish connection to Arduino once
        print("Setting up Arduino connection...")
        connection = ArduinoConnection('COM4')  # Adjust port if needed
        print("Arduino connected successfully!")
        return connection
    except Exception as e:
        print(f"Error while setting up Arduino connection: {e}")
        return None

def main():
    print("Process started.")
    arduino_connection = setup_arduino()

    # Create ArduinoCommands instance
    arduino_commands = ArduinoCommands(arduino_connection)
    io_commands = IO_commands

    # Create MuxControl and LEDControl
    mux_control = MuxControl(arduino_connection)
    led_control = LEDControl(arduino_commands)

    # Create MuxStatusTracker with proper dependencies
    mux_status_tracker = MuxStatusTracker(mux_control, led_control, SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP)

    # Create sensors and initialize the GUI
    sensors = create_sensors()

    # Initialize the GUI in the Tkinter mainloop
    root = tk.Tk()  # Create the main Tkinter root window
    gui = EurofinsGUI(root, arduino_connection)  # Pass the Arduino connection to the GUI

    # Start the sensor processing in a background thread
    def run_sensor_processing():
        process_sensors(sensors, mux_control, gui, led_control, mux_status_tracker)

    # Run the sensor processing in a background thread
    import threading
    sensor_thread = threading.Thread(target=run_sensor_processing, daemon=True)
    sensor_thread.start()

    # Start the Tkinter event loop
    root.mainloop()

    # Cleanup after the GUI is closed
    arduino_connection.disconnect()






if __name__ == "__main__":
    main()
