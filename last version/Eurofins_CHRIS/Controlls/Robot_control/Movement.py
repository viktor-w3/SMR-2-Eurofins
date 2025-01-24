# Controlls/Robot_control/Movement.py

from .Connection import send_urscript_command
from .Robot_grid import grid_to_coordinates
import time

# Functie om de robot te bewegen van de grid
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

def move_robot(coordinates, message=""):
    x, y, z = coordinates
    orientation = [2.13, 2.1, 0.318]           
    speed = 0.8
    acceleration = 0.2
    command = (
        f"movel(p[-0.280, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(1)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def orintatie_van_gripper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.635
    z_pickup = z + 0.005
    y_pickup = y - 0.037
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# gaat rustig naar de positie toe
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# de grijper van de robot veranderen voor een goede beet 666
def pick_up(coordinates, rij, message=""):
    # Ensure rij is valid
    if not isinstance(rij, (int, float)):
        try:
            rij = float(rij)
        except (ValueError, TypeError):
            print(f"Error: Invalid rij value '{rij}' provided to pick_up().")
            return

    print(f"rij (validated) = {rij}")

    x, y, z = coordinates
    x_pickup = x - 0.650
    y_pickup = y - 0.037
    z_pickup = z -0.001*rij**2 + 0.0042*rij - 0.0025      # bovenste rij is  + 0.0027  in de midde + 0.0011 en onder -0.0025
    orientation = [2.146, 2.1312, 0.1372]
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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# omhoog met de sample voor het er uit halen
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
# terug leggen van de sample
def het_in_de_kast_leggen(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x - 0.630
    z_pickup = z + 0.01
    y_pickup = y - 0.046
    orientation = [-2.23, -2.11, 0.1334]
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# grijper er uit halen
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# voor het foto maken
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# bewegen in de foto box
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
    time.sleep(1)
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
