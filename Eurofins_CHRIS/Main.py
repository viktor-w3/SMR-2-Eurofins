import os
import tkinter as tk
from Controlls.Arduino_control.Connection import ArduinoConnection
from Controlls.Arduino_control.Mux_control import MuxControl
from Process.Robot_process import process_sensors
from Process.States_samples import create_sensors
from Controlls.GUI_control import EurofinsGUI
from Controlls.Arduino_control.Led_control import LEDControl
from Controlls.Robot_control import IO_commands
from Controlls.Arduino_control.Command import ArduinoCommands
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
import threading


def setup_arduino():
    """Set up the Arduino connection and return the connection object."""
    try:
        print("Setting up Arduino connection...")
        connection = ArduinoConnection('COM4')  # Replace with your actual port
        print("Arduino connected successfully!")
        return connection
    except Exception as e:
        print(f"Error while setting up Arduino connection: {e}")
        return None




def main():
    print("Initializing process...")

    # Initialize Arduino connection
    arduino_connection = setup_arduino()

    if not arduino_connection:
        print("Failed to establish Arduino connection. Exiting...")
        return

    # Create ArduinoCommands instance
    arduino_commands = ArduinoCommands(arduino_connection)
    io_commands = IO_commands

    # Initialize MuxControl, LEDControl
    mux_control = MuxControl(arduino_connection)
    led_control = LEDControl(arduino_commands)

    # Initialize MuxStatusTracker
    mux_status_tracker = MuxStatusTracker(mux_control, led_control, SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP)

    # Create sensors
    sensors = create_sensors()

    # Initialize IO ports
    io_commands.io_ports_init()
    print("Initializing all IO ports...")
    io_commands.io_activate_all()
    print("Turning all IO ports ON...")
    io_commands.deactivate_io_port(4)  # Example of turning off a port
    print("Turning IO port 4 OFF...")

    # Initialize LEDs and servo
    arduino_commands.initialize_leds()
    arduino_commands.initialize_servo()

    # Initialize the GUI
    root = tk.Tk()
    gui = EurofinsGUI(root, arduino_connection, sensors)  # Pass the Arduino connection to the GUI

    # Create a function to start sensor processing in a separate thread when the start button is clicked
    def start_sensor_processing():
        """Start the sensor processing in a separate thread."""
        try:
            # Pass all required arguments to process_sensors
            process_sensors(
                sensors,  # sensors
                mux_control,  # mux_control
                gui,  # gui (EurofinsGUI instance)
                led_control,  # led_control
                mux_status_tracker,  # mux_status_tracker
                arduino_commands,  # arduino_commands
                io_commands  # io_commands
            )
        except Exception as e:
            print(f"Error during sensor processing: {e}")
        finally:
            gui.running = False  # Stop the process flag when finished
            print("Sensor process completed.")

    # Modify the start button in the GUI to call `start_sensor_processing` on click
    gui.start_button.config(command=start_sensor_processing)

    # Start Tkinter event loop
    root.mainloop()

    # Cleanup after the GUI is closed
    print("Shutting down...")
    arduino_connection.disconnect()


if __name__ == "__main__":
    main()
