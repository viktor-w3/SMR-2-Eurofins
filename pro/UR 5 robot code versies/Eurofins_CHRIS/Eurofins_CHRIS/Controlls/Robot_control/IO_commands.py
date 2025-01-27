<<<<<<< HEAD
# Controlls/Robot_control/IO_commands.py

from Controlls.Robot_control.Connection import send_urscript_command
import socket
import time

def activate_io_port(port_number):
    """
    Activates the specified IO port.

    Args:
        port_number (int): The IO port number to activate (e.g., 0 to 4).
    """
    if not (0 <= port_number <= 4):
        raise ValueError("Port number must be between 0 and 4.")

    command = f"""
    sec activateIO():
        set_digital_out({port_number}, True)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

def deactivate_io_port(port_number):
    """
    Deactivates the specified IO port.

    Args:
        port_number (int): The IO port number to deactivate (e.g., 0 to 4).
    """
    if not (0 <= port_number <= 4):
        raise ValueError("Port number must be between 0 and 4.")

    command = f"""
    sec deactivateIO():
        set_digital_out({port_number}, False)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

def io_ports_init():
    deactivate_io_port(0)
    deactivate_io_port(1)
    deactivate_io_port(2)
    deactivate_io_port(3)
    deactivate_io_port(4)
    time.sleep(0.1)

def io_activate_all():
    activate_io_port(0)
    activate_io_port(1)
    activate_io_port(2)
    activate_io_port(3)
    activate_io_port(4)
=======
# Controlls/Robot_control/IO_commands.py

from Controlls.Robot_control.Connection import send_urscript_command
import socket
import time

def activate_io_port(port_number):
    """
    Activates the specified IO port.

    Args:
        port_number (int): The IO port number to activate (e.g., 0 to 4).
    """
    if not (0 <= port_number <= 4):
        raise ValueError("Port number must be between 0 and 4.")

    command = f"""
    sec activateIO():
        set_digital_out({port_number}, True)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

def deactivate_io_port(port_number):
    """
    Deactivates the specified IO port.

    Args:
        port_number (int): The IO port number to deactivate (e.g., 0 to 4).
    """
    if not (0 <= port_number <= 4):
        raise ValueError("Port number must be between 0 and 4.")

    command = f"""
    sec deactivateIO():
        set_digital_out({port_number}, False)
    end
    """
    response = send_urscript_command(command)
    print(f"Robot antwoord: {response}")

def io_ports_init():
    deactivate_io_port(0)
    deactivate_io_port(1)
    deactivate_io_port(2)
    deactivate_io_port(3)
    deactivate_io_port(4)
    time.sleep(0.1)

def io_activate_all():
    activate_io_port(0)
    activate_io_port(1)
    activate_io_port(2)
    activate_io_port(3)
    activate_io_port(4)
>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
    time.sleep(0.1)