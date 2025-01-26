from .States_samples import create_sensors, update_sensor_state
from Process.Timer import Timer
from Config import SENSOR_TO_GRID_POSITION, SENSOR_TO_LED_STRIP
import time
from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
from Controlls.Arduino_control.Mux_control import MuxControl
from Controlls.Robot_control.Robot_grid import grid, grid_to_coordinates
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Command import ArduinoCommands
from Controlls.Robot_control import IO_commands
from Controlls.Arduino_control.Led_control import LEDControl
from Config import SENSOR_TO_GRID_POSITION

# Initialize the timer system
timer_system = Timer()


def sample_timer(sensor_id, gui, led_control, duration=120):
    """Manage the drying timer for a sample"""
    remaining_time = timer_system.get_remaining_time(sensor_id, duration)

    # Update the GUI with the remaining time
    grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
    if grid_position:
        rij, kolom = grid_position
        gui.update_grid({(rij, kolom): ('Drying_sample', remaining_time)})

    # Update LED loading bar
    strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
    if remaining_time > 0:
        progress_percentage = int(((duration - remaining_time) / duration) * 100)
        led_control.load_bar_range("Orange", progress_percentage, strip_index, start_index, end_index)
    else:
        # Once the timer ends, update the state and set LEDs to the "done" color
        update_sample_state(sensor_id, "Dried_Sample", gui)
        led_control.set_led_range(strip_index, start_index, end_index, "Blue")


def update_sample_state(sensor_id, state, gui):
    """Update the sample state in the GUI"""
    print(f"Sensor {sensor_id} state updated to: {state}")
    grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
    if grid_position:
        rij, kolom = grid_position
        gui.update_grid({(rij, kolom): (state, 0)})


def process_sensors(sensors, mux_control, gui, led_control, mux_status_tracker):
    """Process all sensors and update their states"""
    all_done = False

    while not all_done:
        # Monitor multiplexers and update LED statuses
        mux_status_tracker.monitor_mux_and_control_leds(gui)

        for sensor_id, sensor in sensors.items():
            print(f"Processing Sensor {sensor_id} at position {sensor.position}")
            print(f"Sesnor status: {sensor.current_state}")

            if sensor.current_state == 'New_sample':
                # Start process 1 and set to Drying_sample
                print(f"Starting process 1 for sensor {sensor_id}.")
                sensor.update_state('Drying_sample')
                timer_system.start_timer(sensor_id)  # Start the timer for drying
                update_sample_state(sensor_id, "Drying_sample", gui)  # Update state in GUI

            elif sensor.current_state == 'Drying_sample':
                # Use sample_timer to check the drying state and transition
                sample_timer(sensor_id, gui, led_control)
                # Check if the state should change to Dried_sample
                if timer_system.is_timer_done(sensor_id):
                    print(f"Sensor {sensor_id} is done drying.")
                    sensor.update_state('Dried_sample')
                    update_sample_state(sensor_id, "Dried_sample", gui)

            elif sensor.current_state == 'Dried_sample':
                # Run process 2 and change state to Done_sample
                print(f"Running process 2 for sensor {sensor_id}.")
                sensor.update_state('Done_sample')
                update_sample_state(sensor_id, "Done_sample", gui)

            # If any sensor is not Done_sample or No_sample, we need to process again
            if sensor.current_state not in ['Done_sample', 'No_sample']:
                all_done = False

        # Sleep for a short period before rechecking
        time.sleep(1)
