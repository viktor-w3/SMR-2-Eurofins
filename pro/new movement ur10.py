import tkinter as tk
from tkinter import ttk
import threading
import time

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
    mass = 2.0  # Gewicht in kg (controleer dat dit onder 5 kg blijft)
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
    speed = 0.8
    acceleration = 0.2
    command = (
        f"movel(p[-0.280, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(1)   #1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om de robot te bewegen voor weer in de grid
def move_robot_terug(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = -0.290
    z_terug = z + 0.02
    y_pickup = y - 0.037
    orientation = [-2.13, -2.12, 0.0759]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_terug}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3.7)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def orintatie_van_gripper(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.650
    y_pickup = y - 0.037
    z_pickup = z  + 0.004
    orientation = [-2.15, -2.13, 0.20]
    speed = 0.8
    acceleration = 0.05
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
def orintatie_van_gripper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.635
    z_pickup = z + 0.003
    y_pickup = y - 0.038
    orientation = [2.15, 2.17, 0.201]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(1.5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#gaat rustig naar de positie toe
def langzaam_naar_grid(coordinates, message=""):
    x,y,z = coordinates
    orientation = [-2.23, -2.16, 0.0079]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[-0.280, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# de grijper van de robot veranderen voor een goede beet 666 
def pick_up(coordinates,message=""):
    x, y, z = coordinates
    x_pickup = x - 0.650
    y_pickup = y - 0.042
    z_pickup = z -0.001*rij**2 + 0.0040*rij - 0.0025      # bovenste rij is  + 0.0027  in de midde + 0.0011 en onder -0.0025
    orientation = [2.126, 2.1012, 0.1872]
    speed = 0.8
    acceleration = 0.2
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3.5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def er_uit_halen_van_kast(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = -0.290
    y_pickup = y - 0.037
    z_pickup = z  + 0.004
    orientation = [-2.15, -2.13, 0.20]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3.5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# terug leggen van de sample 
def het_in_de_kast_leggen(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.630
    z_pickup = z + 0.01
    y_pickup = y - 0.046
    orientation = [-2.18, -2.14, 0.1234]
    speed = 0.08
    acceleration = 0.003
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3.5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#grijper er uit halen
def terug_de_grijper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = -0.290
    y_pickup = y - 0.037
    z_pickup = z + 0.005
    orientation = [2.13, 2.1, 0.318]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def move_robot_Photo1(photo_punt1, message=""):
    photo_punt1 = [-0.32, - 0.209, 0.157]
    orientation = [-2.16, -2.12, 0.17]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3)
def move_robot_Photo2(photo_punt2, message=""):
    photo_punt2 = [-0.315, - 0.219, 0.127]
    orientation = [-2.9, -0.02, 0.0]
    speed = 0.8
    acceleration = 0.2
    command = (
        f"movel(p[{photo_punt2[0]}, {photo_punt2[1]}, {photo_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2.5)
def move_robot_Photo3(photo_punt3, message=""):
    photo_punt3 = [-0.445, - 0.188, 0.127]
    orientation = [-2.89, 0.03, -0.002]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{photo_punt3[0]}, {photo_punt3[1]}, {photo_punt3[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2.5)
def move_robot_Photo4(photo_punt4, message=""):
    photo_punt4 = [-0.445, 0.273, 0.127]
    orientation = [-2.9, 0.01, 0.0039]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{photo_punt4[0]}, {photo_punt4[1]}, {photo_punt4[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2.8)
#verf movemebt ---------------------------------------------------------------------------------------------------------------------------
#move voor het verven 
def move_robot_verf1(verf_punt1, message=""):
    verf_punt1 = [-0.320, 0.185, 0.157]
    orientation = [-2.15, -2.09, 0.01]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{verf_punt1[0]}, {verf_punt1[1]}, {verf_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")

    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3)
def move_robot_verf2(verf_punt2, message=""):
    verf_punt2 = [-0.33948, 0.140, 0.134]
    orientation = [0.016, -3.13, 0.22]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{verf_punt2[0]}, {verf_punt2[1]}, {verf_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3)
def move_robot_verf3(verf_punt3, message=""):
    verf_punt3 = [-0.312, -0.282, 0.134]
    orientation = [0.016, -3.1, 0.22]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{verf_punt3[0]}, {verf_punt3[1]}, {verf_punt3[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(3.3)
def move_robot_verf4(verf_punt4, message=""):
    verf_punt4 = [-0.464, -0.281, 0.134]
    orientation = [0, 3.1, -0.18]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{verf_punt4[0]}, {verf_punt4[1]}, {verf_punt4[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
def move_robot_verf5(verf_punt5, message=""):
    verf_punt5 = [-0.464, -0.315, 0.134]
    orientation = [0, 3.1, -0.18]
    speed = 0.8
    acceleration = 0.2
    command = (
        f"movel(p[{verf_punt5[0]}, {verf_punt5[1]}, {verf_punt5[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(1)      #1
def move_robot_verf6(verf_punt6, message=""):
    verf_punt6 = [-0.464, -0.087, 0.137]
    orientation = [0, 3.1, -0.18]
    speed = 0.2
    acceleration = 0.03
    command = (
        f"movel(p[{verf_punt6[0]}, {verf_punt6[1]}, {verf_punt6[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)
def vervenklaar(vervenklaar, message=""):
    vervenklaar = [-0.464, 0.242, 0.138]
    orientation = [0, 3.1, -0.18]
    speed = 0.8
    acceleration = 0.3
    command = (
        f"movel(p[{vervenklaar[0]}, {vervenklaar[1]}, {vervenklaar[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(4)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
def activate_io_port_4():
    command = """
    sec activateIO():
        set_digital_out(4, True)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
def deactivate_io_port_4():
    command = """
    sec deactivateIO():
        set_digital_out(4, False)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

  # Verf en droog samples
def activate_io_port_5():
    command = """
    sec activateIO():
        set_digital_out(5, True)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
def deactivate_io_port_5():
    command = """
    sec deactivateIO():
        set_digital_out(5, False)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]


grid[2][2] = "sample1" 
grid[2][0] = "sample2" 
grid[1][0] = "sample3" 
grid[0][1] = "sample4" 

     # eerst hoogte 
if __name__ == "__main__":

 while True:  # Herhaal het proces continu
         drying_queue = []


         for rij in range(len(grid)):
            drying_queue = []
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
                    #lucht aan
                    activate_io_port_5()
                    move_robot_verf6(f"7.moven voor fotos")
                    #lucht uit 
                    deactivate_io_port_5()
                    vervenklaar(f"7.vervenklaar")
                    
                    move_robot_verf1(f"7.moven voor fotos")
                    
                    move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates,f"11. Beweging om grijper van {sample} weg te halen")
                    
                    grid[rij][kolom] = sample
                   
                   #  Voeg toe aan drooglijst
                    drying_queue.append((time.time(), rij, kolom, sample))
                    print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")


         while drying_queue:
            drying_queue.sort(key=lambda x: x[0])  # Sorteer op droogtijd

            current_time = time.time()
            for start_time, r, c, s in drying_queue[:]:
                elapsed = int(current_time - start_time)
                if elapsed < 30:  # Controleer droogtijd
                    print(f"{s} is aan het drogen. Tijd verstreken: {elapsed // 60}m {elapsed % 60}s.")
                else:
                    
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
                    activate_io_port_4()
                    #Fotografeer het sample in licht uv--------------------------------------------------------
                    
                    #rele schakelen voor licht uit te zetten  
                    deactivate_io_port_4()
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

                    grid[r][c] = f"{s} klaar"

        
        # Controleer of het grid volledig verwerkt is
            all_done = all(cell is None or "klaar" in str(cell) for row in grid for cell in row)
            if all_done:
             print("Alle samples zijn verwerkt. Start een nieuwe cyclus.")
            else:
             print("Nog niet alle samples zijn verwerkt.")
        
time.sleep(5)  # Pauzeer kort voordat je opnieuw begint
                   
                    # Voeg toe aan drooglijst
                    # Beweeg naar het sample
                    
                       
        