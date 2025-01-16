# Controlls/Robot_control/Movement.py

from .Connection import send_urscript_command
import time

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


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# bewegen voot tijdens het verven

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
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


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# grijper er uit halen
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


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# voor het photo maken
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# bewegen in de foto box

