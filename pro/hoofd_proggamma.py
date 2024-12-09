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

# Functie om grid-positie naar coördinaten te converteren
def grid_to_coordinates(rij, kolom):
    x_base, y_base, z_base = 0.427, 0.123, -0.039  # Basispunt van het grid
    z_step, y_step = 0.175, 0.224  # Afstanden tussen gridpunten
    #van het midde kan die 85mm omhoog moet je onder blijven 
    x = x_base
    y = y_base - (kolom * y_step)
    z = z_base + (rij * z_step)
    return [x, y, z]

# Functie om de robot te bewegen
def move_robot(coordinates, message=""):
    x, y, z = coordinates
    orientation = [-2.2, 2.2, 0.027]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)

def langzaam_naar_grid(coordinates, message=""):
    x, y,z = coordinates
    orientation = [2.19, -2.2, -0.04]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[0.320, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)

def langzaam_uit_grid(coordinates, message=""):
    x,y,z = coordinates
    orientation = [2.19, -2.2, -0.04]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[0.270,{y} , {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)

def move_robot_Verf(message=""):
    verf_punt = [0.300, 0.550, 0.500]
    orientation = [2.19, -2.2, -0.04]
    speed = 0.8
    acceleration = 0.4
    command = (
        f"movel(p[{verf_punt[0]}, {verf_punt[1]}, {verf_punt[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)

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
                    
                    # Pak en verf het sample
                    langzaam_naar_grid(coordinates, f"Langzaam naar {sample} in grid")
                    move_robot(coordinates, f"Beweging om {sample} op te pakken")
                    grid[rij][kolom] = None
                    langzaam_uit_grid(coordinates, f"Langzaam uit {sample} in grid")
                    move_robot_Verf(f"Beweging om {sample} te verven")
                    langzaam_uit_grid(coordinates, f"Langzaam uit {sample} in grid")
                    langzaam_naar_grid(coordinates, f"Langzaam naar {sample} in grid")
                    move_robot(coordinates, f"Beweging om {sample} terug te leggen")
                    langzaam_uit_grid(coordinates, f"Langzaam uit {sample} in grid")
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
