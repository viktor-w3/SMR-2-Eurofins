# Main.py
import tkinter as tk
from Controlls.Arduino_control import ArduinoConnection  # Assuming you have a class for Arduino connection
from Process.Robot_process import process_samples
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


    # Set up Arduino connection (using setup_arduino function)
    arduino_connection = setup_arduino()

    if arduino_connection:
        # Create the root window for the Tkinter GUI
        root = tk.Tk()

        # Initialize the Eurofins GUI
        gui = EurofinsGUI(root, arduino_connection)

        root.mainloop()
        # Start the process with both Arduino connection and GUI instance
    else:
        print("Failed to establish Arduino connection. Exiting...")
        return  # Exit the program if the connection fails

    # Start the Tkinter main loop



if __name__ == "__main__":
    main()
