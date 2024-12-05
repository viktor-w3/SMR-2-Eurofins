import socket
import time

def send_urscript_command(command, robot_ip="192.168.0.43", port=30002):
    """Verbindt met de robot en stuurt een URScript-commando."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((robot_ip, port))
            s.sendall(command.encode())
            response = s.recv(1024)  # Ontvang de ruwe bytes
            print(f"Ruwe respons: {response}")  # Debugging van de respons
            return response.decode(errors="replace").strip()  # Decodeer met foutvervanging
    except Exception as e:
        return f"Fout: {e}"

# Configuratie
robot_ip = "192.168.0.43"

# Drie punten in (x, y, z) coördinaten (in meters)
point2 = [0.240, 0.290, 0.440]  # Omgezet naar meters
point3 = [0.300, 0.350, 0.500]

# Rotatiehoeken voor tool (in radians)
orientation = [0, 3.14, 0]  # Roll, Pitch, Yaw

# Snelheid en acceleratie
speed = 0.5  # Verlaagde snelheid (m/s)
acceleration = 0.2  # Verlaagde acceleratie (m/s²)

# URScript-commando's
commands = [
    f"movel(p[{point2[0]}, {point2[1]}, {point2[2]}, {orientation[0]}, {orientation[1]}, {orientation[2]}], a={acceleration}, v={speed})\n",
    f"movel(p[{point3[0]}, {point3[1]}, {point3[2]}, {orientation[0]}, {orientation[1]}, {orientation[2]}], a={acceleration}, v={speed})\n",
]

# Verstuur de commando's en laat de robot bewegen
for command in commands:
    print(f"Verstuur URScript: {command.strip()}")
    response = send_urscript_command(command, robot_ip)
    print(f"Antwoord: {response}")
    time.sleep(5)  # Wacht tussen bewegingen
