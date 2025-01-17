# Main.py
import tkinter as tk
import time
from Controlls import (
    ArduinoCommands,
    ArduinoConnection,
    ServoControl,
    MuxControl,
    MuxStatusTracker,
    LEDControl,
    clear_buffer,
    send_urscript_command,
    activate_io_port,
    io_ports_init,
    io_activate_all,
    deactivate_io_port,
    move_robot,
    move_robot_terug,
    orintatie_van_gripper,
    orintatie_van_gripper_er_uit,
    langzaam_naar_grid,
    pick_up,
    er_uit_halen_van_kast,
    langzaam_uit_grid,
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
    vervenklaar,
    EurofinsGUI
)
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Process import process_samples

def setup_arduino():
    # Create a connection object (adjust based on how you're connecting)
    connection = ArduinoConnection('COM4')  # Example COM port, adjust as necessary
    arduino_commands = ArduinoCommands(connection)
    led_control = LEDControl(arduino_commands)  # LEDControl object
    servo_control = ServoControl(arduino_commands)  # Instantiate the ServoControl with ArduinoCommands
    mux_control = MuxControl(connection)

    # Initialize devices (servo, LEDs)
    clear_buffer(arduino_commands)

    # Initialize servo
    servo_control.initialize_servo()
    servo_control.servo_off()

    # Initialize LEDs
    led_control.initialize_leds()
    led_control.set_all_leds("Red")

    return arduino_commands, led_control, servo_control, mux_control  # Return control objects to use later

def setup_robot():
    # Initialize I/O ports using RobotControl (updated based on your clarification)
    io_ports_init()  # Initialize I/O ports
    io_activate_all()  # Activate all I/O ports


def run_for_next_minute(mux_tracker):
    start_time = time.time()  # Record the start time
    end_time = start_time + 10  # End time after 60 seconds

    while time.time() < end_time:  # Continue until 60 seconds have passed
        mux_tracker.monitor_mux_and_control_leds()  # Call your method here
        time.sleep(0.5)

def testmain():
    print("Starting the program...")

    # Set up Arduino commands and LED control
    led_control, arduino_commands, servo_control, mux_control  = setup_arduino()

    # Instantiate the MuxStatusTracker with mux_control and led_control
    mux_tracker = MuxStatusTracker(mux_control, led_control, SENSOR_TO_MUX_CHANNEL,SENSOR_TO_LED_STRIP)
    # Pause for initialization
    time.sleep(0.3)

    # Initialize servo and LEDs
    clear_buffer(arduino_commands)

    time.sleep(0.3)
    deactivate_io_port(4)
    """
    # LED control and effects
    led_control.set_all_leds("Red")
    time.sleep(0.3)
    led_control.set_all_leds("Black")
    time.sleep(0.3)

    # Display loading bars
    led_control.load_bar_range("Yellow", 1000, 0, 0, 29)
    time.sleep(0.3)
    led_control.set_led_range(0, 0, 29, "Yellow")
    time.sleep(0.3)

    led_control.load_bar_range("Yellow", 1000, 1, 0, 29)
    time.sleep(0.3)
    led_control.set_led_range(1, 0, 29, "Yellow")
    time.sleep(0.3)

    led_control.load_bar_range("Yellow", 1000, 2, 0, 29)
    time.sleep(0.3)
    led_control.set_led_range(2, 0, 29, "Yellow")
    time.sleep(0.3)

    led_control.set_led_range(2, 10, 20, "Green")
    time.sleep(0.3)
    led_control.set_all_leds("White")
    clear_buffer(arduino_commands)
    servo_control.servo_off()
    """
    # Monitor MUX and control LEDs based on the status
    run_for_next_minute(mux_tracker)

    time.sleep(0.3)
    led_control.set_led_range(3, 0, 29, "White")
    # Monitor MUX and control LEDs based on the status
    # mux_tracker = MuxStatusTracker()
    # mux_tracker.read_mux_channel_status(1, 2)

if __name__ == "__main__":
    setup_arduino()
    setup_robot()
    #testmain()
    root = tk.Tk()
    gui = EurofinsGUI(root)
    root.mainloop()
