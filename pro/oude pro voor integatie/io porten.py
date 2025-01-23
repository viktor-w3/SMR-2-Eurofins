import socket
import time

# Functie om een URScript-commando naar de robot te sturen
def send_urscript_command(command, robot_ip="192.168.0.43", port=30002):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((robot_ip, port))
            # Voeg een newline toe om het commando correct te beëindigen
            s.sendall((command + "\n").encode())
            
            # Ontvang de raw byte response van de robot
            response = s.recv(1024)
            print(f"Raw response: {response.hex()}")  # Log in hexadecimale vorm
            
            # Probeer de response te decoderen als UTF-8
            try:
                decoded_response = response.decode('utf-8')
                return decoded_response.strip()
            except UnicodeDecodeError:
                return f"Raw response (niet decodeerbaar als UTF-8): {response.hex()}"
    except Exception as e:
        return f"Fout: {e}"

# Functie om digitale uitgang 4 in te schakelen via een secundair programma
def activate_io_port_4():
    command = """
    sec activateIO():
        set_digital_out(4, True)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

# Functie om digitale uitgang 4 uit te schakelen
def deactivate_io_port_4():
    command = """
    sec deactivateIO():
        set_digital_out(4, False)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

# Test de functies
if __name__ == "__main__":
    activate_io_port_4()
    time.sleep(20)
    deactivate_io_port_4()