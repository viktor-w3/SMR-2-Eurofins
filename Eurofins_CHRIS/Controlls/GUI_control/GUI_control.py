# Controlls/GUI_control/GUI_control.py

import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from Process import process_sensors  # Import the correct function from Robot_process
from Config import SENSOR_TO_GRID_POSITION
from Controlls.GUI_control.Gui_grid_color import get_color  # Import the color function
from Controlls.Arduino_control.Mux_control import MuxControl
from Controlls.Arduino_control.Led_control import LEDControl
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
from Controlls.Arduino_control.Command import ArduinoCommands
from Controlls.Robot_control import IO_commands
from Process.States_samples import Sensor


class EurofinsGUI:
    def __init__(self, root, arduino_connection, sensors):
        self.root = root
        self.root.title("Eurofins Process Control")
        self.arduino_connection = arduino_connection
        self.sample_timers = {}  # Track drying timers for samples
        self.grid_data = {}  # Track the state and timer for each grid cell
        self.process_thread = None
        self.running = False
        self.sensors = sensors

        # Start and Stop buttons
        self.start_button = tk.Button(self.root, text="Start Process", command=self.start_process)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_process)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        # Visual grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=1, column=0, columnspan=2)

        self.grid_cells = {}  # Dictionary to hold grid cells

        for rij in range(3):  # Assuming a 3x3 grid
            for kolom in range(3):
                cell_frame = tk.Frame(self.grid_frame, width=100, height=100, relief="solid", bg="white")
                cell_frame.grid(row=rij, column=kolom, padx=5, pady=5)

                # Adding a label for the sample status
                cell_label = tk.Label(cell_frame, text=f"({rij},{kolom})", width=10, height=4, relief="solid", bg="white")
                cell_label.grid(row=0, column=0)

                # Adding a label for the timer
                timer_label = tk.Label(cell_frame, text="Timer: 0s", width=10, height=2, relief="solid", bg="white")
                timer_label.grid(row=1, column=0)

                self.grid_cells[(rij, kolom)] = {"status": cell_label, "timer": timer_label}

        # Button to open photo directory
        self.open_directory_button = tk.Button(self.root, text="Open Photo Directory",
                                               command=self.open_photo_directory)
        self.open_directory_button.grid(row=2, column=0, columnspan=2, pady=10)

    def start_process(self):
        """Start the process in a separate thread"""
        if not self.running:
            self.running = True
            self.process_thread = Thread(target=self.run_process)
            self.process_thread.daemon = True  # Ensure the thread exits when the main program closes
            self.process_thread.start()

    def run_process(self):
        """Run the robot processing function."""
        try:
            # Assuming you have the necessary components like sensors, mux_control, gui, etc.
            sensors = self.sensors

            # Now you call process_sensors without needing to pass redundant parameters
            process_sensors(sensors, self)
        except Exception as e:
            print(f"Error during process: {e}")
        finally:
            self.running = False  # Reset the flag when the process finishes
            print("Process completed.")

    def stop_process(self):
        """Stop the process and ask for confirmation"""
        if self.running:
            response = messagebox.askquestion("Stop Process", "Do you want to stop the process?")
            if response == 'yes':
                self.terminate_process()

    def terminate_process(self):
        """Terminate the process and reset the grid"""
        if self.process_thread and self.process_thread.is_alive():
            print("Terminating process...")
            self.running = False  # Stop the process
            self.process_thread.join(timeout=10)  # Wait for up to 10 seconds to terminate
            if self.process_thread.is_alive():
                print("Process did not terminate in time!")
            self.process_thread = None  # Reset thread reference
        self.update_grid()  # Reset the grid to its initial state

    def update(self):
        """Update grid cells with colors and timer information."""
        for (rij, kolom), (state, timer) in self.grid_data.items():
            cell = self.grid_cells.get((rij, kolom))
            if cell:
                cell["status"].config(bg=get_color(state), text=state)  # Use get_color for background color
                cell["timer"].config(text=f"Timer: {timer}s")

    def update_grid(self, grid_data=None):
        """Update the grid UI based on sensor data (LED color)"""
        if grid_data:
            self.grid_data = grid_data  # Update the grid data if passed
        self.root.after(0, self.update)  # Schedule the update on the main thread

    def open_photo_directory(self):
        """Opens the base directory where the photos are saved."""
        base_path = "C:\\Users\\denri\\Desktop\\Smr 2"  # Define the base path
        if os.path.exists(base_path):
            try:
                os.startfile(base_path)  # Open the directory on Windows
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the directory: {e}")
        else:
            messagebox.showerror("Directory Not Found", f"The directory {base_path} does not exist.")
