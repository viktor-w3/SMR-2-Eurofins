# Controlls/__init__.py
# Importing Arduino-related classes and functions
from .Arduino_control import (
    ArduinoCommands,       # Ensure defined in Arduino_control.Command
    ArduinoConnection,     # Ensure defined in Arduino_control.Connection
    LEDControl,            # Ensure defined in Arduino_control.Led_control
    MuxControl,            # Ensure defined in Arduino_control.Mux_control
    MuxStatusTracker,      # Ensure defined in Arduino_control.Monitor_mux
    ServoControl,          # Ensure defined in Arduino_control.Servo_control
    clear_buffer           # Ensure defined in Arduino_control.utils
)

# Importing Camera-related classes and functions
from .Camera_control import (
    CameraHandler,         # Ensure defined in Camera_control
    take_clean_photo,
    take_white_photo,
    take_uv_photo

)

# Importing GUI-related classes
from .GUI_control import EurofinsGUI  # Ensure defined in GUI_control
from .GUI_control import get_color

# Importing Robot-related functions and variables
from .Robot_control import (
    send_urscript_command,       # Ensure defined in Robot_control
    activate_io_port,            # Ensure defined in Robot_control
    deactivate_io_port,          # Ensure defined in Robot_control
    io_ports_init,               # Ensure defined in Robot_control
    io_activate_all,             # Ensure defined in Robot_control
    set_robot_payload,
    move_robot,
    move_robot_terug,
    orintatie_van_gripper,
    orintatie_van_gripper_er_uit,
    langzaam_naar_grid,
    pick_up,
    er_uit_halen_van_kast,
    het_in_de_kast_leggen,
    terug_de_grijper_er_uit,
    move_robot_Photo1,
    move_robot_Photo2,
    move_robot_Photo3,
    move_robot_Photo4,
    move_robot_verf1,
    move_robot_verf2,
    move_robot_verf3,
    move_robot_verf4,
    move_robot_verf5,
    move_robot_verf6,
    vervenklaar
)
