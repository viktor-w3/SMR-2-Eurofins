import tkinter as tk
from tkinter import ttk
import threading
import time
from camera_module import CameraHandler
import socket
import os
import subprocess

global photo_counter
photo_counter = 0
# Voeg de benodigde functies toe (zoals grid_to_coordinates, langzaam_naar_grid, etc.) hier, of neem ze over vanuit je oorspronkelijke code.
# Grid-instelling
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
grid[2][0] = "sample1"
# Functie om URScript-commando's naar de robot te sturen
def send_urscript_command(command, robot_ip="192.168.0.43", port=30002):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((robot_ip, port))
            s.sendall(command.encode())
            response = s.recv(1024).decode()
            return response.strip()
    except Exception as e:
        return f"Fout: {e}"
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om grid-positie naar coördinaten te converteren
def grid_to_coordinates(rij, kolom):
    x_base, y_base, z_base = -0.15, -0.203, 0.064  # Basispunt van het grid of -0.150 -0.637
    z_step, y_step = 0.172, 0.224  # Afstanden tussen gridpunten
    #van het midde kan die 85mm omhoog moet je onder blijven 
    x = x_base
    y = y_base + (kolom * y_step)
    z = z_base + (rij * z_step)
    return [x, y, z]
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om de robot te bewegen van de grid
def move_robot(coordinates, message=""):
    x, y, z = coordinates
    orientation = [2.13, 2.1, 0.318]           #=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(4)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om de robot te bewegen voor weer in de grid
def move_robot_terug(coordinates, message=""):
    x, y, z = coordinates
    z_terug = z + 0.02
    orientation = [-2.23, -2.16, 0.0079]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x}, {y}, {z_terug}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def orintatie_van_gripper(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.504
    z_pickup = z  + 0.004
    orientation = [-2.14, -2.204, 0.01759]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x_pickup}, {y}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def orintatie_van_gripper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.504
    z_pickup = z + 0.002
    orientation = [2.08, 2.25, 0.206]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x_pickup}, {y}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#gaat rustig naar de positie toe
def langzaam_naar_grid(coordinates, message=""):
    x, y,z = coordinates
    orientation = [-2.23, -2.16, 0.0079]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[-0.1639, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# de grijper van de robot veranderen voor een goede beet 666 
def pick_up(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.504
    y_pickup = y -0.004
    z_pickup = z + 0.007
    orientation = [2.05, 2.21, 0.159]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def er_uit_halen_van_kast(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x 
    z_pickup = z  + 0.004
    orientation = [-2.14, -2.204, 0.01759]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x_pickup}, {y}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def langzaam_uit_grid(coordinates, message=""):
    x,y,z = coordinates
    orientation = [-2.205, -2.13, 0.0071]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[0.260,{y} , {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)

    verf_punt = [0.300, 0.550, 0.500]
    orientation = [2.19, -2.2, -0.04]
    speed = 0.4
    acceleration = 0.2
    command = (
        f"movel(p[{verf_punt[0]}, {verf_punt[1]}, {verf_punt[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#bewegen voot tijdens het verven

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# terug leggen van de sample 
def het_in_de_kast_leggen(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.504
    z_pickup = z + 0.04
    y_pickup = y - 0.01
    orientation = [-2.14, -2.204, 0.01759]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#grijper er uit halen
def terug_de_grijper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x
    y_pickup = y 
    z_pickup = z
    orientation = [2.13, 2.1, 0.318]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#voor het photo maken
def move_robot_Photo1(photo_punt1, message=""):
    photo_punt1 = [-0.15, - 0.209, 0.041]
    orientation = [-2.23, -2.18, 0.0]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
def move_robot_Photo2(photo_punt2, message=""):
    photo_punt2 = [-0.315, - 0.219, 0.041]
    orientation = [-3.1, -0.02, 0.0]
    speed = 0.8
    acceleration = 0.5
    command = (
        f"movel(p[{photo_punt2[0]}, {photo_punt2[1]}, {photo_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
def move_robot_Photo3(photo_punt3, message=""):
    photo_punt3 = [-0.401, - 0.156, 0.081]
    orientation = [-3.06, 0.0, 0.0]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{photo_punt3[0]}, {photo_punt3[1]}, {photo_punt3[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def move_robot_Photo4(photo_punt4, message=""):
    photo_punt4 = [-0.401, 0.3122, 0.081]
    orientation = [-3.1, 0.0, 0.0]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{photo_punt4[0]}, {photo_punt4[1]}, {photo_punt4[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#bewegen in de foto box 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#een foto maken code
def take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\vikto\\Desktop\\Smr 2"):
    global photo_counter
    photo_counter += 1  # Verhoog de teller

    # Bereken de sample map (elke 3 foto's verandert de sample naam)
    sample_number = (photo_counter - 1) // 3 + 1
    sample_name = f"{sample_base_name}{sample_number}"
    output_dir = os.path.join(output_dir_base, sample_name)

    # Zorg ervoor dat de output-directory bestaat
    os.makedirs(output_dir, exist_ok=True)

    # Stel de bestandsnaam voor de foto in
    photo_name = f"{sample_name}_photo{photo_counter}.jpg"
    photo_path = os.path.join(output_dir, photo_name)

    # Maak de foto (camera-module)
    try:
        camera_handler = CameraHandler(output_dir=output_dir)
        camera_handler.capture_photo(photo_path)  # Specificeer de volledige bestandsnaam
        camera_handler.release_camera()
        print(f"Foto opgeslagen: {photo_path}")
    except Exception as e:
        print(f"Fout bij het maken van de foto: {e}")

    return photo_path
class EurofinsGUI:
    def __init__(self, root):
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
        title_label.grid(row=0, column=0 ,columnspan=5, pady=10, sticky="nsew")

        # Status Lampjes (3x3 grid)
        status_label = tk.Label(root, text="Status lampjes van de data set",font=("Arial", 10), bg="gray", fg="black")
        status_label.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.lampjes = []  # Store lamp widgets
        for i in range(3):
            row_lampjes = []
            for j in range(3):
                frame = tk.Frame(root, bg="gray")
                frame.grid(row=i + 2, column=j, padx=5, pady=5, sticky="nsew")

                lamp = tk.Canvas(frame, width=80, height=80, bg="red", highlightthickness=1, highlightbackground="black")
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

        self.stop_knop = tk.Button(button_frame, text="Stop Knop", bg="red", command=self.stop_knop_action, height=button_height, width=button_width)
        self.stop_knop.pack(fill="x", pady=5)

        self.start_knop = tk.Button(button_frame, text="Start Knop", bg="green", command=self.start_knop_action, height=button_height, width=button_width)
        self.start_knop.pack(fill="x", pady=5)

        data_knop = tk.Button(button_frame, text="Folder voor Data", command=self.open_folder, height=button_height, width=button_width)
        data_knop.pack(fill="x", pady=5)

        # Status update label
        self.status_label = tk.Label(root, text="Huidige stap van het proces wordt live geupdate", anchor="w", bg="gray", fg="white")
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
        folder_path = r"C:\Users\vikto\Desktop\Smr 2"
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
        else:
            print(f"De map {folder_path} bestaat niet.")

    # Update lampjes status
    def update_lamp(self, row, col, status):
        colors = {"red": "red", "green": "green", "orange": "orange"}
        if status in colors:
            self.lampjes[row][col].config(bg=colors[status])

    def process_samples(self):
     while True:  # Herhaal het proces continu
         drying_queue = []  # Houdt bij welke samples drogen
        
        # Verf en droog samples
         for rij in range(len(grid)):
            for kolom in range(len(grid[rij])):
                if grid[rij][kolom] is not None:
                    sample = grid[rij][kolom]
                    coordinates = grid_to_coordinates(rij, kolom)

                    # Pak en verf het sample
                    langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")
                    move_robot(coordinates, f"2. Beweging om {sample} op te pakken")
                    grid[rij][kolom] = None
                    pick_up(coordinates, f"3. Pakken van {sample} met aanpasingven van de grijper") 
                    orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")
                    er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sample}") 
                    #photo maken van sample zonder verf
                    move_robot_Photo1(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo2(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo3(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo4(coordinates, f"6.moven voor fotos")
                    #move_robot_Verf(f"6. Beweging om {sample} te verven") 
                    #rele schakelen voor licth  
                    take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\vikto\\Desktop\\Smr 2"f"Photo zonder verf van {sample}")
                    #rele uitschakelen voor licth
                    move_robot_Photo3(coordinates, f"6.moven voor fotos")                    
                    move_robot_Photo2(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo1(coordinates, f"6.moven voor fotos")
                    #bewegingen voor het verven 

                    move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates,f"11. Beweging om grijper van {sample} weg te halen")
                    grid[rij][kolom] = sample
                    

                    # Voeg toe aan drooglijst
                    drying_queue.append((time.time(), rij, kolom, sample))
                    print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")
        
        # Wachten tot alles droog is en foto's maken
         while drying_queue:
            drying_queue.sort(key=lambda x: x[0])  # Sorteer op droogtijd

            current_time = time.time()
            for start_time, r, c, s in drying_queue[:]:
                elapsed = int(current_time - start_time)
                if elapsed < 120:  # Controleer droogtijd
                    print(f"{s} is aan het drogen. Tijd verstreken: {elapsed // 60}m {elapsed % 60}s.")
                else:
                    # Sample is droog, verwerk het
                    drying_queue.remove((start_time, r, c, s))
                    print(f"{s} is nu droog en klaar voor foto.")

                    # Beweeg naar het sample
                    coordinates = grid_to_coordinates(r, c)
                    langzaam_naar_grid(coordinates, f"Langzaam naar {s} in grid")
                    move_robot(coordinates, f"Beweging om {s} op te pakken")
                    
                    # Fotografeer het sample
                    move_robot_Photo1(f"Beweging om {s} te fotograferen")
                    move_robot_Photo2(f"Beweging om {s} te fotograferen")
                    #rele schakelen voor licht 
                    take_photo(f"Photo met verf in normaal licht van {sample}")
                    #rele schakelen voor licht uit te zetten  
                    # Fotografeer het sample in uv----------------------------------------------------------------------- 
                    #rele schakelen voor licht van uv  
                    take_photo(f"Photo in uv licht van {sample}")
                    #rele uitschakelen voor licht van uv  
                    # Breng het sample terug
                    langzaam_naar_grid(coordinates, f"Langzaam naar {s} in grid")
                    move_robot(coordinates, f"Beweging om {s} terug te leggen")
                    langzaam_uit_grid(coordinates, f"Langzaam uit {s} in grid")
                   
                    # Markeer sample als klaar
                    grid[r][c] = f"{s} klaar"

        
        # Controleer of het grid volledig verwerkt is
         all_done = all(cell is None or "klaar" in str(cell) for row in grid for cell in row)
         if all_done:
            print("Alle samples zijn verwerkt. Start een nieuwe cyclus.")
         else:
            print("Nog niet alle samples zijn verwerkt.")
        
         time.sleep(5)  # Pauzeer kort voordat je opnieuw begint

            
        
        
  # Pauzeer kort voordat je opnieuw begint



if __name__ == "__main__":
    root = tk.Tk()
    gui = EurofinsGUI(root)
    root.mainloop()
