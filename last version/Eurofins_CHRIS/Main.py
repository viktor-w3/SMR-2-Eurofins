import time
from Controlls.Arduino_control.Connection import ArduinoConnection
from Controlls.Arduino_control.Mux_control import MuxControl
from Process.Robot_process import process_sensors
from Process.States_samples import Sensor, SensorState
from Controlls.Arduino_control.Led_control import LEDControl
from Controlls.Robot_control import IO_commands
from Controlls.Arduino_control.Command import ArduinoCommands
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
from Process.States_samples import Sensor, SensorState

def setup_arduino():
    """Set up the Arduino connection and return the connection object."""
    try:
        print("Setting up Arduino connection...")
        connection = ArduinoConnection('COM4')  # Replace with your actual port
        print("Arduino connected successfully!")
        return connection
    except Exception as e:
        print(f"Error while setting up Arduino connection: {e}")
        return None


from Process.States_samples import Sensor  # Import the Sensor class
from Config import SENSOR_TO_GRID_POSITION


def create_sensors():
    """
    Function to create all sensors dynamically based on the grid mapping
    and print their details.
    """
    sensors = []  # List to hold all sensor objects

    # Loop through each sensor ID in SENSOR_TO_GRID_POSITION
    for sensor_id in SENSOR_TO_GRID_POSITION:
        sensor = Sensor(sensor_id)  # Automatically assigns the position from the grid mapping
        sensors.append(sensor)  # Add the sensor to the list
        print(sensor)  # Print the sensor's information

    return sensors

def main():
    print("Initializing process...")

    # Initialize Arduino connection
    arduino_connection = setup_arduino()

    if not arduino_connection:
        print("Failed to establish Arduino connection. Exiting...")
        return

    # Create ArduinoCommands instance
    arduino_commands = ArduinoCommands(arduino_connection)
    io_commands = IO_commands

    # Initialize MuxControl, LEDControl
    mux_control = MuxControl(arduino_connection)
    led_control = LEDControl(arduino_commands)
    mux_status_tracker = MuxStatusTracker(mux_control, led_control, SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP)

    # Initialize IO ports
    io_commands.io_ports_init()
    print("Initializing all IO ports...")
    io_commands.io_activate_all()
    print("Turning all IO ports ON...")
    io_commands.deactivate_io_port(4)  # Example of turning off a port
    print("Turning IO port 4 OFF...")
    # Initialize LEDs and servo
    arduino_commands.initialize_leds()
    arduino_commands.initialize_servo()
    # Create sensors
    sensors = create_sensors()
    # Start the sensor processing loop
    process_sensors(
        sensors=sensors,
        mux_control=mux_control,
        gui=None,  # No GUI required
        led_control=led_control,
        mux_status_tracker=mux_status_tracker,
        arduino_commands=arduino_commands,
        io_commands=io_commands
    )

    # Cleanup after processing
    print("Shutting down...")
    arduino_connection.disconnect()

if __name__ == "__main__":
    main()
