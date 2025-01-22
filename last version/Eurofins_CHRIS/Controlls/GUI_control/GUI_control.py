# Controlls/GUI_control/GUI_control.py

import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from Process import process_samples  # Import the process function from Robot_process
from Config import SENSOR_TO_GRID_POSITION


class EurofinsGUI:
    def __init__(self, root, arduino_connection):
        self.root = root
        self.root.title("Eurofins Process Control")
        self.arduino_connection = arduino_connection
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
                cell = tk.Label(self.grid_frame, text=f"({rij},{kolom})", width=10, height=4, relief="solid",
                                bg="white")
                cell.grid(row=rij, column=kolom, padx=5, pady=5)
                self.grid_cells[(rij, kolom)] = cell

        # Button to open photo directory
        self.open_directory_button = tk.Button(self.root, text="Open Photo Directory",
                                               command=self.open_photo_directory)
        self.open_directory_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.process_thread = None
        self.running = False

    def start_process(self):
        """Start the process in a separate thread"""
        if not self.running:
            self.running = True
            self.process_thread = Thread(target=self.run_process)
            self.process_thread.start()

    def run_process(self):
        """Run the robot processing function."""
        self.running = True  # Ensure the process flag is set
        try:
            # Pass the running flag to process_samples
            process_samples(self.arduino_connection, self, self.running)
        except Exception as e:
            print(f"Error during process: {e}")
        finally:
            self.running = False  # Reset the flag when the process finishes
            print("Process completed.")

    def stop_process(self):
        """Stop the process and ask for confirmation"""
        if self.running:
            self.running = False
            response = messagebox.askquestion("Stop Process", "Do you want to stop the process?")
            if response == 'yes':
                self.terminate_process()
            else:
                self.running = True

    def terminate_process(self):
        """Terminate the process and reset the grid"""
        if self.process_thread.is_alive():
            print("Terminating process...")
            self.running = False  # Stop the process
            self.process_thread.join(timeout=10)  # Wait for up to 10 seconds to terminate
            if self.process_thread.is_alive():
                print("Process did not terminate in time!")
                self.process_thread = None  # Optionally handle this situation
        self.update_grid()  # Reset the grid to its initial state

    def update_grid(self, grid_data=None):
        """Update the grid UI based on sensor data (LED color)"""

        def update():
            """Update grid cells with colors."""
            if grid_data:
                for (rij, kolom), color in grid_data.items():
                    cell = self.grid_cells.get((rij, kolom))  # Use 'rij' and 'kolom' as keys
                    if cell:
                        cell.config(bg=color)
            else:
                # Reset the grid to white
                for cell in self.grid_cells.values():
                    cell.config(bg="white")

        # Schedule the update to be done in the main thread
        self.root.after(0, update)  # 0 ms delay for immediate scheduling

    def update_sensor_status(self, sensor_id, status):
        """Update a single sensor's status"""
        grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
        if grid_position:
            rij, kolom = grid_position  # Using 'rij' and 'kolom'
            self.update_grid({(rij, kolom): status})

    def open_photo_directory(self):
        """
        Opens the base directory where the photos are saved.
        """
        # Define the base path to your directory
        base_path = "C:\\Users\\denri\\Desktop\\Smr 2"

        # Check if the directory exists
        if os.path.exists(base_path):
            try:
                # Open the directory using the default file explorer
                os.startfile(base_path)  # Works on Windows
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the directory: {e}")
        else:
            messagebox.showerror("Directory Not Found", f"The directory {base_path} does not exist.")
