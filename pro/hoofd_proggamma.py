# feature moet Base view zijn om de goed cordinate te zien
#----------------------------------------------------------------

import time
import socket

# Grid-instelling dus hier moet ook ergens de sensor data binennen komen
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
#----------------------------------------------------------------

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
#---------------------------------------------------------------- 

# Functie om grid-positie naar coördinaten te converteren
def grid_to_coordinates(rij, kolom):
    """Converteer een gridpositie naar fysieke (x, y, z) coördinaten."""
    x_base, y_base, z_base = 0.75, 0.079, 0.394                 # Basispunt van het grid
    z_step, y_step = 0.02, 0.02                                 # Afstanden tussen gridpunten
    x = x_base                                                  # Hoogte blijft constant
    y = y_base + (kolom * y_step)
    z = z_base + (rij * z_step)
    return [x, y, z]
#---------------------------------------------------------------

# Functie om de robot te bewegen van de opslag ruimte
def move_robot(coordinates, message=""):
    """Stuur een beweging naar de robot."""
    x, y, z = coordinates
    orientation = [0, 1.3, 0.4]                                 # Roll, Pitch, Yaw
    speed = 0.1
    acceleration = 0.2
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)                                              # Wacht om beweging te simuleren
#----------------------------------------------------------------

# Deel van de code voor de beweging van het verven
def move_robot_Verf(message=""):
    """Beweeg de robot naar de verfpositie."""
    verf_punt1 = [0.03, 0.569, 0.841]
    verf_punt2 = [0.03, 0.469, 0.750]
    orientation = [0, 1.3, 0.4]                                 # Roll, Pitch, Yaw
    speed = 0.05
    acceleration = 0.1
    command = (
        f"movel(p[{verf_punt1[0]}, {verf_punt1[1]}, {verf_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"movel(p[{verf_punt2[0]}, {verf_punt2[1]}, {verf_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)                                              # Wacht om beweging te simuleren
#----------------------------------------------------------------

# Hier is de deel van de code dat zorgt voor de beweging naar de cammera
def move_robot_Photo(message=""):
    """Beweeg de robot naar de fotopositie."""
    photo_punt1 = [0.03, 0.57, 0.800]
    photo_punt2 = [0.03, 0.550, 0.850]
    orientation = [0, 1.3, 0.4]                                 # Roll, Pitch, Yaw
    speed = 0.1
    acceleration = 0.2
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"movel(p[{photo_punt2[0]}, {photo_punt2[1]}, {photo_punt2[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)                                              # Wacht om beweging te simuleren
#----------------------------------------------------------------

# Automatisch verwerkingssysteem
def process_samples_continuous():
    drying_queue = []                                           # Houdt bij welke samples drogen

    while True:
        # Verwerk te verven samples
        for rij in range(len(grid)):
            for kolom in range(len(grid[rij])):
                if grid[rij][kolom] is not None and not grid[rij][kolom].endswith("klaar"):
                    # 1. Pak het sample op
                    sample = grid[rij][kolom]
                    coordinates = grid_to_coordinates(rij, kolom)
                    move_robot(coordinates, f"Beweging om {sample} op te pakken")
                    grid[rij][kolom] = None                 # Maak de plek leeg
                    
                    # 2. Breng het naar de verfplek
                    move_robot_Verf(f"Beweging om {sample} te verven")
                    
                    # 3. Breng het terug naar zijn originele plek
                    move_robot(coordinates, f"Beweging om {sample} terug te leggen")
                    grid[rij][kolom] = sample               # Plaats het sample terug
                    
                    # 4. Voeg toe aan drooglijst
                    drying_queue.append((time.time(), rij, kolom, sample))
                    print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")

        # Verwerk drogende samples
        current_time = time.time()
        for start_time, r, c, s in drying_queue[:]:         # Maak een kopie voor iteratie
            elapsed = int(current_time - start_time)
            if elapsed < 60:                                # Minder dan 15 minuten nu even op 1 min 
                print(f"{s} is aan het drogen. Tijd verstreken: {elapsed // 60}m {elapsed % 60}s.")
            else:
                # Sample is klaar met drogen
                drying_queue.remove((start_time, r, c, s))
                print(f"{s} is nu droog en klaar voor foto.")
                
                # 5. Beweeg naar fotoplek
                move_robot_Photo(f"Beweging om {s} te fotograferen")
                
                # 6. Breng het sample terug naar zijn plek
                coordinates = grid_to_coordinates(r, c)
                move_robot(coordinates, f"Beweging om {s} terug te leggen")
                grid[r][c] = f"{s} klaar"                   # Markeer als volledig verwerkt

        # Laat huidige gridstatus zien
        print("Huidige grid-status:")
        for rij in grid:
            print(rij)
        
        # Wacht even voordat je de loop opnieuw doorloopt
        print("Wachten op nieuwe samples...")
        time.sleep(5)                                      # Wacht 5 seconden voordat de loop opnieuw begint
#----------------------------------------------------------------

# Voorbeeldsamples toevoegen aan grid voor het testen zonder asvalt
grid[0][0] = "sample1"
grid[0][1] = "sample2"
grid[2][2] = "sample3"
#---------------------------------------------------------------


# Start verwerking
process_samples_continuous()
