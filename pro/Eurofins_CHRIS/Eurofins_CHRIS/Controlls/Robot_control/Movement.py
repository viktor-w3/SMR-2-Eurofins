<<<<<<< HEAD
# Controlls/Robot_control/Movement.py

from .Connection import send_urscript_command
import time

# Functie om de robot te bewegen van de grid
def move_robot(coordinates, message=""):
    x, y, z = coordinates
    orientation = [2.13, 2.1, 0.318]           #=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    speed = 0.8
    acceleration = 0.6
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(0.5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functie om de robot te bewegen voor weer in de grid
def move_robot_terug(coordinates, message=""):
    x, y, z = coordinates
    z_terug = z + 0.02
    orientation = [-2.13, -2.12, 0.0759]
    speed = 0.8
    acceleration = 0.05
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
    x_pickup = x - 0.500
    z_pickup = z + 0.003
    orientation = [2.08, 2.25, 0.206]
    speed = 0.008
    acceleration = 0.005
    command = (
        f"movel(p[{x_pickup}, {y}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
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
    x_pickup = x - 0.501  #(-0.0025**kolom + 0.0025*kolom)
    y_pickup = y - 0.015
    z_pickup = z -0.001*rij**2 + 0.0040*rij - 0.0025      # bovenste rij is  + 0.0027  in de midde + 0.0011 en onder -0.0025
    orientation = [2.146, 2.1312, 0.1372]
    speed = 0.4
    acceleration = 0.1
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def er_uit_halen_van_kast(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x 
    y_pickup = y 
    z_pickup = z  + 0.005
    orientation = [-2.09, -2.14, 0.14]
    speed = 0.2
    acceleration = 0.09
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)
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
    x_pickup = x - 0.500
    z_pickup = z + 0.04
    y_pickup = y -.02
    orientation = [-2.13, -2.12, 0.0759]
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


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# grijper er uit halen
def terug_de_grijper_er_uit(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x
    y_pickup = y 
    z_pickup = z
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


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# voor het photo maken
def move_robot_Photo1(photo_punt1, message=""):
    photo_punt1 = [-0.15, - 0.209, 0.041]
    orientation = [-2.16, -2.12, 0.17]
    speed = 0.08
    acceleration = 0.05
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def move_robot_Photo2(photo_punt2, message=""):
    photo_punt2 = [-0.315, - 0.219, 0.041]
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
    time.sleep(20)
def move_robot_Photo3(photo_punt3, message=""):
    photo_punt3 = [-0.433, - 0.189, 0.047]
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
    photo_punt4 = [-0.433, 0.305, 0.047]
    orientation = [-2.9, 0.01, 0.0]
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
def move_robot_verf1(verf_punt1, message=""):
    verf_punt1 = [-0.159, 0.193, 0.112]
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
    time.sleep(20)
def move_robot_verf2(verf_punt2, message=""):
    verf_punt2 = [-0.315, 0.140, 0.041]
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
    time.sleep(20)
def move_robot_verf3(verf_punt3, message=""):
    verf_punt3 = [-0.314, - 0.285, 0.041]
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
    time.sleep(20)
def move_robot_verf4(verf_punt4, message=""):
    verf_punt4 = [-0.451, -0.284, 0.041]
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
    verf_punt5 = [-0.451, -0.317, 0.041]
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
    verf_punt6 = [-0.451, -0.090, 0.043]
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
    vervenklaar = [-0.451, 0.152, 0.045]
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
=======
# Controlls/Robot_control/Movement.py

from .Connection import send_urscript_command
import time

# Functie om de robot te bewegen van de grid
def move_robot(coordinates, message=""):
    x, y, z = coordinates
    orientation = [2.13, 2.1, 0.318]           #=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    speed = 0.8
    acceleration = 0.6
    command = (
        f"movel(p[{x}, {y}, {z}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(0.5)
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
    x_pickup = x - 0.501
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
    x_pickup = x - 0.501  #(-0.0025**kolom + 0.0025*kolom)
    y_pickup = y - 0.015
    z_pickup = z -0.001*rij**2 + 0.0040*rij - 0.0025      # bovenste rij is  + 0.0027  in de midde + 0.0011 en onder -0.0025
    orientation = [2.146, 2.1312, 0.1372]
    speed = 0.4
    acceleration = 0.1
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#omhoog met de sample voor het er uit halen
def er_uit_halen_van_kast(coordinates, message=""):
    x, y, z = coordinates
    x_pickup = x 
    y_pickup = y 
    z_pickup = z  + 0.005
    orientation = [-2.09, -2.14, 0.14]
    speed = 0.2
    acceleration = 0.09
    command = (
        f"movel(p[{x_pickup}, {y_pickup}, {z_pickup}, {orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(5)
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
    orientation = [-2.16, -2.12, 0.17]
    speed = 0.08
    acceleration = 0.05
    command = (
        f"movel(p[{photo_punt1[0]}, {photo_punt1[1]}, {photo_punt1[2]},{orientation[0]}, {orientation[1]}, {orientation[2]}], "
        f"a={acceleration}, v={speed})\n"
       
    )
    print(f"{message}: {command.strip()}")
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")
    time.sleep(20)
def move_robot_Photo2(photo_punt2, message=""):
    photo_punt2 = [-0.315, - 0.219, 0.041]
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
    time.sleep(20)
def move_robot_Photo3(photo_punt3, message=""):
    photo_punt3 = [-0.433, - 0.189, 0.047]
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
    photo_punt4 = [-0.433, 0.305, 0.047]
    orientation = [-2.9, 0.01, 0.0]
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
def move_robot_verf1(verf_punt1, message=""):
    verf_punt1 = [-0.159, 0.193, 0.112]
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
    time.sleep(20)
def move_robot_verf2(verf_punt2, message=""):
    verf_punt2 = [-0.315, 0.140, 0.041]
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
    time.sleep(20)
def move_robot_verf3(verf_punt3, message=""):
    verf_punt3 = [-0.314, - 0.285, 0.041]
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
    time.sleep(20)
def move_robot_verf4(verf_punt4, message=""):
    verf_punt4 = [-0.451, -0.284, 0.041]
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
    verf_punt5 = [-0.451, -0.317, 0.041]
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
    verf_punt6 = [-0.451, -0.090, 0.043]
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
    vervenklaar = [-0.451, 0.152, 0.045]
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
>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
