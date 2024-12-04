import time
import socket

# Grid-instelling
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

history = []  # Geschiedenis van opgepakte samples

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
    """Converteer een gridpositie naar fysieke (x, y, z) coördinaten."""
    x_base, y_base, z_base = 0.75, 0.079, 0.194  # Basispunt van het grid
    z_step, y_step = 0.02, 0.02  # Afstanden tussen gridpunten
    x = x_base # Hoogte blijft constant
    y = y_base + (kolom * y_step)
    z = z_base + (rij * z_step) 
    return [x, y, z]

# Functie om de robot te bewegen
def move_robot(coordinates, message=""):
    """Stuur een beweging naar de robot."""
    x, y, z = coordinates
    orientation = [0, 1.3, 0.4]  # Roll, Pitch, Yaw
    speed = 0.4
    acceleration = 0.01
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)  # Wacht om beweging te simuleren

def move_robot_Verf(message=""):
    """Beweeg de robot naar de verfpositie."""
    verf_punt = [0.300, 0.350, 0.500]
    orientation = [0, 1.3, 0.4]  # Roll, Pitch, Yaw
    speed = 0.4
    acceleration = 0.01
    command = (
        f"movel(p[{verf_punt[0]}, {verf_punt[1]}, {verf_punt[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(10)  # Wacht om beweging te simuleren

# Automatisch verwerkingssysteem
def process_samples():
    drying_queue = []  # Houdt bij welke samples drogen
    for rij in range(len(grid)):
        for kolom in range(len(grid[rij])):
            if grid[rij][kolom] is not None:
                # 1. Pak het sample op
                sample = grid[rij][kolom]
                coordinates = grid_to_coordinates(rij, kolom)
                move_robot(coordinates, f"Beweging om {sample} op te pakken")
                grid[rij][kolom] = None  # Maak de plek leeg
                
                # 2. Breng het naar de verfplek
                move_robot_Verf(f"Beweging om {sample} te verven")
                
                # 3. Breng het terug naar zijn originele plek
                move_robot(coordinates, f"Beweging om {sample} terug te leggen")
                grid[rij][kolom] = sample  # Plaats het sample terug
                
                # 4. Voeg toe aan drooglijst
                drying_queue.append((time.time(), rij, kolom, sample))
                print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")

            # Controleer drogende samples
            current_time = time.time()
            drying_queue = [
                (start_time, r, c, s)
                for start_time, r, c, s in drying_queue
                if current_time - start_time < 900  # Droogtijd 15 minuten
            ]

            # Geef status van drogende samples
            for start_time, r, c, s in drying_queue:
                elapsed = int(current_time - start_time)
                print(f"{s} is aan het drogen. Tijd verstreken: {elapsed // 60}m {elapsed % 60}s.")

            # Als droogtijd is verstreken, markeer als klaar
            completed_samples = [
                (start_time, r, c, s) for start_time, r, c, s in drying_queue
                if current_time - start_time >= 900
            ]
            for _, r, c, s in completed_samples:
                grid[r][c] = f"{s} klaar"
                print(f"{s} is nu droog en klaar.")

# Samples toevoegen aan grid
grid[0][0] = "sample1"
grid[0][1] = "sample2"
grid[2][2] = "sample3"

# Start verwerking
process_samples()

# Laat verwerkte grid-status zien
print("Eindstatus van het grid:")
for rij in grid:
    print(rij)
