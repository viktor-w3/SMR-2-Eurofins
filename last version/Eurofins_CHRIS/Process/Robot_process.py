# Process/Robot_process.py

from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
from Controlls.Arduino_control.Mux_control import MuxControl
from Controlls.Robot_control.Robot_grid import grid
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Command import ArduinoCommands
from Controlls.Robot_control import IO_commands
from Controlls.Arduino_control.Led_control import LEDControl

import time
from Config import SENSOR_TO_GRID_POSITION


def process_samples(arduino_connection,gui, running):
    """Process samples by monitoring MUX channels and controlling LEDs."""
    print("Process started.")
    # Create ArduinoCommands instance using the existing arduino_connection
    arduino_commands = ArduinoCommands(arduino_connection)
    io_commands = IO_commands

    # Create MuxControl and LEDControl using the ArduinoCommands instance
    mux_control = MuxControl(arduino_connection)  # MuxControl will use the connection to communicate with Arduino
    led_control = LEDControl(arduino_commands)  # LEDControl will use ArduinoCommands to send LED commands

    io_commands.io_ports_init()
    print(f"Initialize all IO ports")
    io_commands.io_activate_all()
    print(f"Turn all IO ports ON")
    io_commands.deactivate_io_port(4)
    print(f"Turn IO port 4 OFF")

    # Initialize LEDs via ArduinoCommands
    arduino_commands.initialize_leds()
    arduino_commands.initialize_servo()

    # Now handle the MUX channels and LEDs monitoring
    mux_tracker = MuxStatusTracker(
        mux_control=mux_control,
        led_control=led_control,
        sensor_to_mux_channel=SENSOR_TO_MUX_CHANNEL,
        sensor_to_led_strip=SENSOR_TO_LED_STRIP
    )

    drying_queue = []  # Track drying samples

    while running:
        # Check each sensor and process the sample
        print("Process runnn.")
        mux_tracker.run_for_next_minute(gui)  # Assuming this method processes the MUX channels
        for sensor_id in range(9):
            grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
            gui.update_sensor_status(sensor_id, "green")
            if not grid_position:
                continue

            rij, kolom = grid_position
            sample = grid[rij][kolom]

            if sample and sample.startswith("sample"):
                print(f"Processing {sample} at grid[{rij}][{kolom}]...")

                gui.update_sensor_status(sensor_id, "orange")
                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.set_led_range(strip_index, start_index, end_index, "Orange")  # Set LEDs to orange for the range

                coordinates = grid_to_coordinates(rij, kolom)

                langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")
                move_robot(coordinates, f"2. Beweging om {sample} op te pakken")
                grid[rij][kolom] = None
                pick_up(coordinates, f"3. Pakken van {sample} met aanpasingven van de grijper")
                orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")
                er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sample}")
                # photo maken voor verven------------------------------------------------------------------------------------------------------
                move_robot_Photo1(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo4(coordinates, f"6.moven voor fotos")

                led_control.set_led_range(3, 0, 29, "White") # LEDstrip 3 aan
                # First set of photos (before painting)
                take_photo(sample_base_name=f"sample_{sample}_Clean",
                           output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2")

                led_control.set_led_range(3, 0, 29, "Black") # LEDstrip 3 uit # LED 3 uit

                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo1(coordinates, f"6.moven voor fotos")
                # fotot voor verven klaar------------------------------------------------------------------------------------------------------
                move_photo_en_verf_punt()
                # bewegingen voor het verven---------------------------------------------------------------------------------------------------
                move_robot_verf1(f"7.moven voor fotos")
                move_robot_verf2(f"7.moven voor fotos")
                move_robot_verf3(f"7.moven voor fotos")
                move_robot_verf4(f"7.moven voor fotos")
                move_robot_verf5(f"7.moven voor fotos")
                
                #io_commands.activate_io_port(5)
                arduino_commands.servo_on()# servomoter aan
                move_robot_verf6(f"7.moven voor fotos")
                #io_commands.deactivate_io_port(5)
                arduino_commands.servo_off()# servomotor uit

                vervenklaar(f"7.vervenklaar")
                move_robot_verf1(f"7.moven voor fotos")
                # klaar met verven-------------------------------------------------------------------------------------------------------------
                move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                orintatie_van_gripper_er_uit(coordinates,
                                             f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sample} weg te halen")
                #grid update--------


                # Voeg toe aan drooglijst
                drying_queue.append((time.time(), rij, kolom, sample))

                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.load_bar_range("Orange", 120, strip_index, start_index, end_index)

                gui.update_sensor_status(sensor_id, "Orange")
                print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")
                # Wachten tot alles droog is en foto's maken

                mux_tracker.run_for_next_minute(gui)
                grid[rij][kolom] = sample

    while drying_queue:
        drying_queue.sort(key=lambda x: x[0])  # Sorteer op droogtijd

        current_time = time.time()
        for drying_start_time, rij, kolom, sample, sensor_id in drying_queue[:]:
            elapsed_time = int(current_time - drying_start_time)
            if elapsed_time < 120:
                # Update the drying load bar progress
                progress = int((elapsed_time / 120) * 30)  # 30 LEDs total for the load bar
                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.load_bar_range("Orange", elapsed_time, strip_index, start_index, start_index + progress)

                print(f"{sample} is drying. Time elapsed: {elapsed_time // 60}m {elapsed_time % 60}s.")
            else:
                # Drying is complete, finish processing the sample
                print(drying_queue)
                drying_queue.remove((drying_start_time, rij, kolom, sample, sensor_id))
                print(f"{sample} is now dry and ready for the next steps.")

                # Beweeg naar het sample
                coordinates = grid_to_coordinates(rij, kolom)
                langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")  # goed
                move_robot(coordinates, f"2. Beweging om {sample} op te pakken")  # goed
                pick_up(coordinates, f"3. Pakken van {sample} met aanpasingven van de grijper")  # goed
                orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")  # goed
                er_uit_halen_van_kast(coordinates, f"5. er uit halen van {sample}")

                # Fotografeer het sample
                move_robot_Photo1(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo4(coordinates, f"6.moven voor fotos")

                led_control.set_led_range(3, 0, 29, "White")
                # Second set of photos (after painting)
                take_photo(sample_base_name=f"sample_{sample}_White",
                           output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2")

                led_control.set_led_range(3, 0, 29, "Black")

                # Fotografeer het sample in uv-----------------------------------------------------------------------
                io_commands.activate_io_port(4)
                # Second set of photos (after painting)
                take_photo(sample_base_name=f"sample_{sample}_UV",
                           output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2")

                io_commands.deactivate_io_port(4)

                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo1(coordinates, f"6.moven voor fotos")

                # terug leggen
                move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                orintatie_van_gripper_er_uit(coordinates,
                                             f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sample} weg te halen")

                # Markeer sample als klaar
                grid[rij][kolom] = f"{sample} klaar"

                mux_tracker.run_for_next_minute(gui)
                gui.update_sensor_status(sensor_id, "Blue")
                strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]
                led_control.set_led_range(strip_index, start_index, end_index, "Blue")  # Set LEDs to orange for the range


                grid[rij][kolom] = sample

    # Controleer of het grid volledig verwerkt is
    all_done = all(cell is None or "klaar" in str(cell) for row in grid for cell in row)
    if all_done:
        print("Alle samples zijn verwerkt. Start een nieuwe cyclus.")
    else:
        print("Nog niet alle samples zijn verwerkt.")
        time.sleep(5)  # Pause briefly before starting again
