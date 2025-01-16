# Controlls/GUI_control/GUI_control.py

import tkinter as tk
from tkinter import ttk
import threading
import os
import subprocess

class EurofinsGUI:
    def __init__(self, root):
        print(f"EurofinsGUI opgeroepen.")
        self.root = root
        self.root.title("Eurofins GUI SMR2")
        self.running = False
        # Set background color
        self.root.configure(bg="gray")

        # Configure grid weights for responsive layout
        for i in range(5):
            self.root.columnconfigure(i, weight=1)
        for i in range(9):
            self.root.rowconfigure(i, weight=1)

        # Title
        title_label = tk.Label(root, text="Eurofins GUI SMR2", font=("Arial", 16), bg="light gray", fg="black")
        title_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")

        # Status Lampjes (3x3 grid)
        status_label = tk.Label(root, text="Status lampjes van de data set", font=("Arial", 10), bg="gray", fg="black")
        status_label.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.lampjes = []  # Store lamp widgets
        for i in range(3):
            row_lampjes = []
            for j in range(3):
                frame = tk.Frame(root, bg="gray")
                frame.grid(row=i + 2, column=j, padx=5, pady=5, sticky="nsew")

                lamp = tk.Canvas(frame, width=80, height=80, bg="red", highlightthickness=1,
                                 highlightbackground="black")
                lamp.pack()

                number_label = tk.Label(frame, text=str(i * 3 + j + 1), bg="gray", fg="white", font=("Arial", 10))
                number_label.pack()

                row_lampjes.append(lamp)
            self.lampjes.append(row_lampjes)

        # Knoppen
        button_frame = tk.Frame(root, bg="gray")
        button_frame.grid(row=2, column=4, rowspan=4, padx=10, pady=5, sticky="nsew")

        button_height = 4
        button_width = 15

        self.stop_knop = tk.Button(button_frame, text="Stop Knop", bg="red", command=self.stop_knop_action,
                                   height=button_height, width=button_width)
        self.stop_knop.pack(fill="x", pady=5)

        self.start_knop = tk.Button(button_frame, text="Start Knop", bg="green", command=self.start_knop_action,
                                    height=button_height, width=button_width)
        self.start_knop.pack(fill="x", pady=5)

        data_knop = tk.Button(button_frame, text="Folder voor Data", command=self.open_folder, height=button_height,
                              width=button_width)
        data_knop.pack(fill="x", pady=5)

        # Status update label
        self.status_label = tk.Label(root, text="Huidige stap van het proces wordt live geupdate", anchor="w",
                                     bg="gray", fg="white")
        self.status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Timer en aantal stukken klaar naast elkaar
        info_frame = tk.Frame(root, bg="gray")
        info_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        timer_label = tk.Label(info_frame, text="Timer", bg="gray", fg="black")
        timer_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.timer_label = tk.Label(info_frame, text="00:00:00", bg="white", anchor="e")
        self.timer_label.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        klaar_label = tk.Label(info_frame, text="Aantal stukken die klaar zijn", bg="gray", fg="black")
        klaar_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.klaar_label = tk.Label(info_frame, text="0", bg="white", anchor="e")
        self.klaar_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        afgekuurde_label = tk.Label(info_frame, text="Aantal stukken die afgekuurde klaar zijn", bg="gray", fg="black")
        afgekuurde_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.afgekuurde = tk.Label(info_frame, text="0", bg="white", anchor="e")
        self.afgekuurde.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # Droogtijd tabel naast timer en aantal stukken klaar
        droogtijd_frame = tk.Frame(root, bg="gray")
        droogtijd_frame.grid(row=5, column=4, columnspan=3, rowspan=3, padx=5, pady=5, sticky="nsew")

        droogtijd_label = tk.Label(droogtijd_frame, text="Droog tijd per sample", bg="gray", fg="black")
        droogtijd_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Create table with two columns: Sample and Timer
        self.droogtijd_table = ttk.Treeview(droogtijd_frame, columns=("Sample", "Timer"), show="headings", height=9)
        self.droogtijd_table.heading("Sample", text="Sample")
        self.droogtijd_table.heading("Timer", text="Timer")
        self.droogtijd_table.column("Sample", width=200, anchor="center")
        self.droogtijd_table.column("Timer", width=200, anchor="center")
        self.droogtijd_table.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Populate table with samples and placeholder timers
        for i in range(1, 10):
            self.droogtijd_table.insert("", "end", values=(f"Sample {i}", "00:00"))

    # Actions for buttons (placeholders)
    def stop_knop_action(self):
        self.status_label.config(text="Proces gestopt", fg="red")
        self.running = False  # Set the flag to False to stop the thread

    def start_knop_action(self):
        self.status_label.config(text="Proces gestart", fg="green")
        self.running = True  # Set the flag to True to start the thread
        # Start process in a new thread using a lambda to avoid the need for self argument
        threading.Thread(target=self.process_samples, daemon=True).start()

    def open_folder(self):
        folder_path = r"C:\Users\...\Desktop\Smr 2"
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
        else:
            print(f"De map {folder_path} bestaat niet.")

    # Update lampjes status
    def update_lamp(self, row, col, status):
        colors = {"red": "red", "green": "green", "orange": "orange"}
        if status in colors:
            self.lampjes[row][col].config(bg=colors[status])