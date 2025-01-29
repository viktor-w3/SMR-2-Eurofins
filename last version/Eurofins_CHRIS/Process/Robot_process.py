# Process/Robot_process.py


from Process.Timer import Timer
import time
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Config import SENSOR_TO_GRID_POSITION
from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control.Monitor_mux import *
from Controlls.Arduino_control.Mux_control import MuxControl
from Controlls.Robot_control.Robot_grid import grid
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Command import ArduinoCommands
from Controlls.Robot_control import IO_commands
from Controlls.Arduino_control.Led_control import LEDControl
from Process.States_samples import Sensor, SensorState

# Initialize the timer system
timer_system = Timer()

def process_sensors(sensors, mux_control, gui, led_control, mux_status_tracker, arduino_commands, io_commands):
    """Process all sensors and update their states."""
    all_done = False

    while not all_done:
        # Monitoring MUX channels and controlling LEDs
        mux_status_tracker.monitor_mux_and_control_leds(sensors = sensors)

        for sensor in sensors: #Loop through all Samples with state NEW_SAMPLE and process them. NO_SAMPLE is skipped
            mux_status_tracker.monitor_mux_and_control_leds(sensors=sensors)
            check_dry_time(sensors, mux_control, gui, led_control, mux_status_tracker, arduino_commands, io_commands)
            sensor_id= sensor.sensor_id
            print(f"Processing Sensor {sensor_id} at position {sensor.position}")
            print(f"Sensor status: {sensor.current_state}")
           # gui.update_sensor_status(sensor_id, "orange")
            strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]


            # Ensure proper position is retrieved
            grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
            if grid_position:
                rij, kolom = grid_position
                coordinates = grid_to_coordinates(rij, kolom)  # Retrieve the correct coordinates
            else:
                print(f"Error: Sensor {sensor_id} not found in grid mapping.")
                continue  # Skip this iteration or handle the error accordingly

            if sensor.current_state == SensorState.NO_SAMPLE:
                print(f"No_sample at {sensor_id}, skipping")
                continue

            elif sensor.current_state == SensorState.NEW_SAMPLE:
                print(f"Starting process 1 for sensor {sensor_id}.")
                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.set_led_range(strip_index, start_index, end_index, "Blue")  # Set LEDs to Blue for the range
                # Start process 1 and set to Drying_sample
                coordinates = grid_to_coordinates(rij, kolom)
                set_robot_payload(message="Standaard payload instellen voor UR10")
                #time.sleep(3)

                langzaam_naar_grid(coordinates, f"1. Langzaam naar {sensor_id} in grid")
                move_robot(coordinates, f"2. Beweging om {sensor_id} op te pakken")
                #grid[rij][kolom] = None
                pick_up(coordinates, rij, f"3. Pakken van {sensor_id} met aanpasingven van de grijper")
                orintatie_van_gripper(coordinates, f"4. Orintatie van {sensor_id} gripper aanpassing in grid")
                er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sensor_id}")

                # photo maken voor verven------------------------------------------------------------------------------------------------------
                move_robot_Photo1(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo4(coordinates, f"6.moven voor fotos")

                led_control.set_led_range(3, 0, 29, "White")  # LEDstrip 3 aan
                # First set of photos (before painting)
                take_clean_photo(sample_base_name=f"sample_{sensor_id}_Clean",
                                 output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2")

                led_control.set_led_range(3, 0, 29, "Black")  # LEDstrip 3 uit # LED 3 uit

                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo1(coordinates, f"6.moven voor fotos")

                # Use arduino_commands to control servos or LEDs
                #arduino_commands.servo_on()  # Turn on the servo motor
                move_robot_verf1(f"7.moven voor fotos")
                move_robot_verf2(f"7.moven voor fotos")
                move_robot_verf3(f"7.moven voor fotos")
                move_robot_verf4(f"7.moven voor fotos")
                move_robot_verf5(f"7.moven voor fotos")

                # Example of using io_commands
                io_commands.activate_io_port(5)  # Activate an I/O port
                #time.sleep(3)
                move_robot_verf6(f"7.moven voor fotos")
                io_commands.deactivate_io_port(5)  # Deactivate I/O port

                vervenklaar(f"7.vervenklaar")
                move_robot_verf1(f"7.moven voor fotos")
                # klaar met verven-------------------------------------------------------------------------------------------------------------
                move_robot_terug(coordinates, f"8. Beweging om {sensor_id} terug te leggen")
                het_in_de_kast_leggen(coordinates, f"9. Beweging om {sensor_id} terug te leggen")
                orintatie_van_gripper_er_uit(coordinates,
                                             f"10. Orintatie van {sensor_id} gripper aanpassing in grid om er uit te gaan")
                terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sensor_id} weg te halen")

                #time.sleep(3)

                #led_control.set_led_range(strip_index, start_index, end_index, "Blue")  # Set LEDs to orange
                sensor.update_state(SensorState.DRYING_SAMPLE)  # Update state to DRYING_SAMPLE
                #update_sample_state(sensor_id, "Drying_sample", gui)
            check_dry_time(sensors, mux_control, gui, led_control, mux_status_tracker, arduino_commands, io_commands)
            start_dried_samples(sensors, mux_control, gui, led_control, mux_status_tracker, arduino_commands, io_commands)
            # Update all_done flag to True if all sensors are in a final state

            all_done = all(
                sensor.current_state in [SensorState.DONE_SAMPLE, SensorState.NO_SAMPLE]
                for sensor in sensors
            )
            if all_done:
                print("All sensors are in final states (Done_sample or No_sample).")

            # Sleep for a short period before rechecking
            time.sleep(1)

def check_dry_time(sensors, mux_control, gui, led_control, mux_status_tracker, arduino_commands, io_commands):
    for sensor in sensors:  # Loop through all Samples with state NEW_SAMPLE and process them. NO_SAMPLE is skipped
        sensor_id = sensor.sensor_id
        if sensor.current_state == SensorState.DRYING_SAMPLE:
            # Check timer and get remaining time
            is_done, remaining_time = sensor.check_timer(duration=60)

            # Update the drying process status based on remaining time
            print(f"Remaining Time for Sensor {sensor_id}: {remaining_time} seconds")
            if not is_done and remaining_time > 0:
                # Calculate and display the loading bar progress
                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.set_led_range(strip_index, start_index, end_index, "Purple")
            elif is_done:
                # Once drying is done, set LEDs to orange
                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.set_led_range(strip_index, start_index, end_index, "Orange")
                # Update state to DRIED_SAMPLE
                sensor.update_state(SensorState.DRIED_SAMPLE)

def start_dried_samples(sensors, mux_control, gui, led_control, mux_status_tracker, arduino_commands, io_commands):
    for sensor in sensors:  # Loop through all Samples with state NEW_SAMPLE and process them. NO_SAMPLE is skipped
        sensor_id = sensor.sensor_id
        strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]

        # Ensure proper position is retrieved
        grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
        if grid_position:
            rij, kolom = grid_position
            coordinates = grid_to_coordinates(rij, kolom)  # Retrieve the correct coordinates
        else:
            print(f"Error: Sensor {sensor_id} not found in grid mapping.")
            continue  # Skip this iteration or handle the error accordingly

        if sensor.current_state == SensorState.NO_SAMPLE:
            print(f"No_sample at {sensor_id}, skipping")
            continue

        if sensor.current_state == SensorState.DRIED_SAMPLE:
            # Run process 2 and change state to Done_sample
            print(f"Running process 2 for sensor {sensor_id}.")
            print(f"{sensor_id} is now dry and ready for the next steps.")
            strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
            led_control.set_led_range(strip_index, start_index, end_index,
                                      "Blue")  # Set LEDs to Blue for the range

            # Beweeg naar het sample
            coordinates = grid_to_coordinates(rij, kolom)

            langzaam_naar_grid(coordinates, f"1. Langzaam naar {sensor_id} in grid")  # goed
            move_robot(coordinates, f"2. Beweging om {sensor_id} op te pakken")  # goed
            pick_up(coordinates, rij,f"3. Pakken van {sensor_id} met aanpasingven van de grijper")  # goed
            orintatie_van_gripper(coordinates,
                                  f"4. Orintatie van {sensor_id} gripper aanpassing in grid")  # goed
            er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sensor_id}")

            # Fotografeer het sample
            move_robot_Photo1(coordinates, f"6.moven voor fotos")
            move_robot_Photo2(coordinates, f"6.moven voor fotos")
            move_robot_Photo3(coordinates, f"6.moven voor fotos")
            move_robot_Photo4(coordinates, f"6.moven voor fotos")

            # time.sleep(3)
            led_control.set_led_range(3, 0, 29, "White")
            # Second set of photos (after painting)
            take_white_photo(sample_base_name=f"sample_{sensor_id}_White",
                             output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2")

            led_control.set_led_range(3, 0, 29, "Black")

            # Fotografeer het sample in uv-----------------------------------------------------------------------
            io_commands.activate_io_port(4)
            # Second set of photos (after painting)
            take_uv_photo(sample_base_name=f"sample_{sensor_id}_UV",
                          output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2")

            io_commands.deactivate_io_port(4)
            # time.sleep(3)

            move_robot_Photo3(coordinates, f"6.moven voor fotos")
            move_robot_Photo2(coordinates, f"6.moven voor fotos")
            move_robot_Photo1(coordinates, f"6.moven voor fotos")

            # terug leggen
            move_robot_terug(coordinates, f"8. Beweging om {sensor_id} terug te leggen")
            het_in_de_kast_leggen(coordinates, f"9. Beweging om {sensor_id} terug te leggen")
            orintatie_van_gripper_er_uit(coordinates,
                                         f"10. Orintatie van {sensor_id} gripper aanpassing in grid om er uit te gaan")
            terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sensor_id} weg te halen")

            sensor.update_state(SensorState.DONE_SAMPLE)
            # update_sample_state(sensor_id, "Done_sample", gui)
            strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
            led_control.set_led_range(strip_index, start_index, end_index,
                                      "Red")  # Set LEDs to Blue for the range


