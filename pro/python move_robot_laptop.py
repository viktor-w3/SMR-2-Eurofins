from camera_module import CameraHandler
import time
import socket

# Grid-instelling
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

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
    speed = 0.4
    acceleration = 0.2
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om de robot te bewegen voor weer in de grid
def move_robot_terug(coordinates, message=""):
    x, y, z = coordinates
    z_terug = z + 0.02
    orientation = [-2.23, -2.16, 0.0079]
    speed = 0.4
    acceleration = 0.2
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
    x_pickup = x - 0.512
    z_pickup = z  + 0.004
    orientation = [-2.14, -2.204, 0.01759]
    speed = 0.4
    acceleration = 0.2
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
    x_pickup = x - 0.512
    z_pickup = z + 0.002
    orientation = [2.08, 2.25, 0.206]
    speed = 0.4
    acceleration = 0.2
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
    speed = 0.4
    acceleration = 0.2
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
    x_pickup = x - 0.512
    y_pickup = y -0.004
    z_pickup = z 
    orientation = [2.05, 2.21, 0.159]
    speed = 0.4
    acceleration = 0.2
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
    speed = 0.08
    acceleration = 0.004
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
    speed = 0.2
    acceleration = 0.1
    command = (
        f"movel(p[0.260,{y} , {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#gaat voor het verven
def move_robot_Verf(message=""):
    verf_punt = [0.300, 0.550, 0.500]
    orientation = [2.19, -2.2, -0.04]
    speed = 0.02
    acceleration = 0.001
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
    x_pickup = x - 0.512
    z_pickup = z + 0.04
    y_pickup = y - 0.01
    orientation = [-2.14, -2.204, 0.01759]
    speed = 0.2
    acceleration = 0.1
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(40)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#grijper er uit halen
def terug_de_grijper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x
    y_pickup = y 
    z_pickup = z
    orientation = [2.13, 2.1, 0.318]
    speed = 0.4
    acceleration = 0.2
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
def move_robot_Photo(message=""):
    photo_punt1 = [0.300, 0.450, 0.700]
    photo_punt2 = [0.400, 0.633, 0.350]
    orientation = [2.19, -2.2, -0.04]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
        f"movel(p[{photo_punt2[0]}, {photo_punt2[1]}, {photo_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#bewegen in de foto box 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Automatisch verwerkingssysteem
def process_samples():
    while True:  # Herhaal het proces continu
        drying_queue = []  # Houdt bij welke samples drogen
        
        # Verf en droog samples
        for rij in range(len(grid)):
            for kolom in range(len(grid[rij])):
                if grid[rij][kolom] is not None:
                    sample = grid[rij][kolom]
                    coordinates = grid_to_coordinates(rij, kolom)
                    
                    camera_handler = CameraHandler(output_dir="C:\\Users\\vikto\\Desktop\\Smr 2")
                    photo_path = camera_handler.capture_photo()
                    camera_handler.release_camera()

                    # Pak en verf het sample
                    langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")
                    move_robot(coordinates, f"2. Beweging om {sample} op te pakken")
                    grid[rij][kolom] = None
                    pick_up(coordinates, f"3. Pakken van {sample} met aanpasingven van de grijper") 
                    orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")
                    er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sample}") 
                    langzaam_uit_grid(coordinates, f"6. Langzaam uit {sample} in grid")
                    #photo maken van sample zonder verf
                                                #move_robot_Verf(f"6. Beweging om {sample} te verven")
                    #bewegingen voor het verven 
                    langzaam_uit_grid(coordinates, f"7. Langzaam uit {sample} in grid")
                    move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates,f"11. Beweging om grijper van {sample} weg te halen")
                    langzaam_uit_grid(coordinates, f"12. Langzaam uit {sample} in grid")
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
                if elapsed < 30:  # Controleer droogtijd
                    print(f"{s} is aan het drogen. Tijd verstreken: {elapsed // 60}m {elapsed % 60}s.")
                else:
                    # Sample is droog, verwerk het
                    drying_queue.remove((start_time, r, c, s))
                    print(f"{s} is nu droog en klaar voor foto.")

                    # Beweeg naar het sample
                    coordinates = grid_to_coordinates(r, c)
                    langzaam_naar_grid(coordinates, f"Langzaam naar {s} in grid")
                    move_robot(coordinates, f"Beweging om {s} op te pakken")
                    langzaam_uit_grid(coordinates, f"Langzaam uit {s} in grid")

                    # Fotografeer het sample
                    move_robot_Photo(f"Beweging om {s} te fotograferen")

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

# Samples toevoegen aan grid
grid[0][0] = "sample1"
grid[0][1] = "sample2"
grid[2][2] = "sample3"


# Start verwerking
process_samples()
