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

def set_robot_payload(message=""):
    """
    Stel de payload in op 2 kg en CoG op [0.0, 0.0, 0.0].
    Geschikt voor UR5.
    """
    mass = 0.0  # Gewicht in kg (controleer dat dit onder 5 kg blijft)
    cog = [0.0, 0.0, 0.0]  # Zwaartepunt in meters
    command = f"set_payload({mass}, [{cog[0]}, {cog[1]}, {cog[2]}])\n"
    if message:
        print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(1)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om grid-positie naar coördinaten te converteren
def grid_to_coordinates(rij, kolom):
    x_base, y_base, z_base = -0.15, -0.203, 0.157  # Basispunt van het grid of -0.150 -0.637
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
    speed = 0.08
    acceleration = 0.006
    command = (
        f"movel(p[-0.280, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om de robot te bewegen voor weer in de grid
def move_robot_terug(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = -0.290
    z_terug = z + 0.02
    y_pickup = y - 0.037
    orientation = [-2.13, -2.12, 0.0759]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_terug}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def orintatie_van_gripper(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.650
    y_pickup = y - 0.037
    z_pickup = z  + 0.004
    orientation = [-2.15, -2.13, 0.20]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def orintatie_van_gripper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.635
    z_pickup = z + 0.005
    y_pickup = y - 0.037
    orientation = [2.15, 2.17, 0.201]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#gaat rustig naar de positie toe
def langzaam_naar_grid(coordinates, message=""):
    x,y,z = coordinates
    orientation = [-2.23, -2.16, 0.0079]
    speed = 0.08
    acceleration = 0.05
    command = (
        f"movel(p[-0.280, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# de grijper van de robot veranderen voor een goede beet 666 
def pick_up(coordinates,message=""):
    x, y, z = coordinates
    x_pickup = x - 0.650
    y_pickup = y - 0.037
    z_pickup = z -0.001*rij**2 + 0.0042*rij - 0.0025      # bovenste rij is  + 0.0027  in de midde + 0.0011 en onder -0.0025
    orientation = [2.146, 2.1312, 0.1372]
    speed = 0.04
    acceleration = 0.02
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def er_uit_halen_van_kast(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = -0.290
    y_pickup = y - 0.037
    z_pickup = z  + 0.004
    orientation = [-2.15, -2.13, 0.20]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# terug leggen van de sample 
def het_in_de_kast_leggen(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.630
    z_pickup = z + 0.01
    y_pickup = y - 0.046
    orientation = [-2.23, -2.11, 0.1334]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#grijper er uit halen
def terug_de_grijper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = -0.290
    y_pickup = y - 0.037
    z_pickup = z + 0.005
    orientation = [2.13, 2.1, 0.318]
    speed = 0.08
    acceleration = 0.05
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def move_robot_Photo1(photo_punt1, message=""):
    photo_punt1 = [-0.32, - 0.209, 0.157]
    orientation = [-2.16, -2.12, 0.17]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def move_robot_Photo2(photo_punt2, message=""):
    photo_punt2 = [-0.315, - 0.219, 0.127]
    orientation = [-2.9, -0.02, 0.0]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{photo_punt2[0]}, {photo_punt2[1]}, {photo_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)
def move_robot_Photo3(photo_punt3, message=""):
    photo_punt3 = [-0.445, - 0.188, 0.127]
    orientation = [-2.89, 0.03, -0.002]
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
    photo_punt4 = [-0.445, 0.273, 0.127]
    orientation = [-2.9, 0.01, 0.0039]
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
#verf movemebt ---------------------------------------------------------------------------------------------------------------------------
#move voor het verven 
def move_robot_verf1(verf_punt1, message=""):
    verf_punt1 = [-0.320, 0.185, 0.157]
    orientation = [-2.15, -2.09, 0.01]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{verf_punt1[0]}, {verf_punt1[1]}, {verf_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")

    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(30)
def move_robot_verf2(verf_punt2, message=""):
    verf_punt2 = [-0.33948, 0.140, 0.134]
    orientation = [0.016, -3.13, 0.22]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{verf_punt2[0]}, {verf_punt2[1]}, {verf_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(30)
def move_robot_verf3(verf_punt3, message=""):
    verf_punt3 = [-0.312, -0.282, 0.134]
    orientation = [0.016, -3.1, 0.22]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{verf_punt3[0]}, {verf_punt3[1]}, {verf_punt3[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(30)
def move_robot_verf4(verf_punt4, message=""):
    verf_punt4 = [-0.464, -0.281, 0.134]
    orientation = [0, 3.1, -0.18]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{verf_punt4[0]}, {verf_punt4[1]}, {verf_punt4[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def move_robot_verf5(verf_punt5, message=""):
    verf_punt5 = [-0.464, -0.315, 0.134]
    orientation = [0, 3.1, -0.18]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{verf_punt5[0]}, {verf_punt5[1]}, {verf_punt5[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def move_robot_verf6(verf_punt6, message=""):
    verf_punt6 = [-0.464, -0.087, 0.134]
    orientation = [0, 3.1, -0.18]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{verf_punt6[0]}, {verf_punt6[1]}, {verf_punt6[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def vervenklaar(vervenklaar, message=""):
    vervenklaar = [-0.464, 0.242, 0.134]
    orientation = [0, 3.1, -0.18]
    speed = 0.08
    acceleration = 0.005
    command = (
        f"movel(p[{vervenklaar[0]}, {vervenklaar[1]}, {vervenklaar[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)

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
  # Verf en droog samples

grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]


grid[2][0] = "sample1"      # eerst hoogte 
if __name__ == "__main__":




 for rij in range(len(grid)):
            for kolom in range(len(grid[rij])):
                if grid[rij][kolom] is not None:
                    sample = grid[rij][kolom]
                    coordinates = grid_to_coordinates(rij, kolom)
                    set_robot_payload(message="Standaard payload instellen voor UR5")
                    #beweging uit grig helemaal prima

                    langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")
                    move_robot(coordinates, f"2. Beweging om {sample} op te pakken")
                    grid[rij][kolom] = None
                    pick_up(coordinates, f"3. Pakken van {sample} met aanpasingven van de grijper") 
                    orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")
                    er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sample}") 
                   
                    #photo maken voor verven------------------------------------------------------------------------------------------------------
                    move_robot_Photo1(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo2(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo3(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo4(coordinates, f"6.moven voor fotos")
                     
                    move_robot_Photo3(coordinates, f"6.moven voor fotos")                    
                    move_robot_Photo2(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo1(coordinates, f"6.moven voor fotos")
                                       
                    move_robot_verf1(f"7.moven voor fotos")
                    move_robot_verf2(f"7.moven voor fotos")
                    move_robot_verf3(f"7.moven voor fotos")
                    move_robot_verf4(f"7.moven voor fotos")
                    move_robot_verf5(f"7.moven voor fotos")
                    move_robot_verf6(f"7.moven voor fotos")
                    vervenklaar(f"7.vervenklaar")
                    
                    move_robot_verf1(f"7.moven voor fotos")
                    
                    move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates,f"11. Beweging om grijper van {sample} weg te halen")
                    grid[rij][kolom] = sample
                   
                   
                   
                    # Voeg toe aan drooglijst
                    # Beweeg naar het sample
                    
                    langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")                               #goed
                    move_robot(coordinates, f"2. Beweging om {sample} op te pakken")                                    #goed
                    pick_up(coordinates, f"3. Pakken van {sample} met aanpasingven van de grijper")                     #goed
                    orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")         #goed
                    er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sample}") 
                    
                    # Fotografeer het sample
                    move_robot_Photo1(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo2(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo3(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo4(coordinates, f"6.moven voor fotos")
                    #rele schakelen voor licht 

                    #take_photo(f"Photo met verf in normaal licht van {sample}")
                    
                    #rele schakelen voor licht uit te zetten  
                    
                    #Fotografeer het sample in uv----------------------------------------------------------------------- 
                    #io poort 4 aan voor uv  
                    #take_photo(f"Photo in uv licht van {sample}")
                    #io port 4 uit voor uv licht
                    
                    move_robot_Photo3(coordinates, f"6.moven voor fotos")
                    move_robot_Photo2(coordinates, f"6.moven voor fotos") 
                    move_robot_Photo1(coordinates, f"6.moven voor fotos")             
                    
                    #terug leggen 
                    move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates,f"11. Beweging om grijper van {sample} weg te halen")
                       
        