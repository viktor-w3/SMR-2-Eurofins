# Process/Robot_process.py

from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control.Monitor_mux import MuxStatusTracker
from Controlls.Arduino_control.Mux_control import MuxControl
from Controlls.Robot_control.Robot_grid import grid
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP
from Controlls.Arduino_control.Command import ArduinoCommands

import time
from Config import SENSOR_TO_GRID_POSITION

from Controlls.Arduino_control.Led_control import LEDControl


def process_samples(arduino_connection,gui, running):
    """Process samples by monitoring MUX channels and controlling LEDs."""

    # Create ArduinoCommands instance using the existing arduino_connection
    arduino_commands = ArduinoCommands(arduino_connection)

    # Create MuxControl and LEDControl using the ArduinoCommands instance
    mux_control = MuxControl(arduino_connection)  # MuxControl will use the connection to communicate with Arduino
    led_control = LEDControl(arduino_commands)  # LEDControl will use ArduinoCommands to send LED commands

    # Initialize LEDs via ArduinoCommands
    arduino_commands.initialize_leds()

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
        mux_tracker.run_for_next_minute()  # Assuming this method processes the MUX channels
        for sensor_id in range(9):
            grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)
            if not grid_position:
                continue

            rij, kolom = grid_position
            sample = grid[rij][kolom]

            if sample and sample.startswith("sample"):
                gui.update_sensor_status(sensor_id, "green")
                print(f"Processing {sample} at grid[{rij}][{kolom}]...")
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
                # rele schakelen voor licth
                take_photo(sample_base_name="sample",
                           output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2"f"Photo zonder verf van {sample}")
                # rele uitschakelen voor licth
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
                # servomoter aan
                move_robot_verf6(f"7.moven voor fotos")
                # servomotor uit
                vervenklaar(f"7.vervenklaar")
                move_robot_verf1(f"7.moven voor fotos")
                # klaar met verven-------------------------------------------------------------------------------------------------------------
                move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                orintatie_van_gripper_er_uit(coordinates,
                                             f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sample} weg te halen")
                grid[rij][kolom] = sample

                # Voeg toe aan drooglijst
                drying_queue.append((time.time(), rij, kolom, sample))
                print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")
        # Wait until all samples are dry
        while drying_queue:
            drying_queue.sort(key=lambda x: x[0])  # Sort by drying time

            current_time = time.time()
            for start_time, r, c, s in drying_queue[:]:
                elapsed = int(current_time - start_time)
                if elapsed < 120:  # Check drying time
                    print(f"{s} is drying. Time elapsed: {elapsed // 60}m {elapsed % 60}s.")
                else:
                    # Sample is droog, verwerk het
                    drying_queue.remove((start_time, r, c, s))
                    print(f"{s} is nu droog en klaar voor foto.")

                    # Beweeg naar het sample
                    coordinates = grid_to_coordinates(r, c)
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
                    # rele schakelen voor licht
                    take_photo(f"Photo met verf in normaal licht van {sample}")
                    # rele schakelen voor licht uit te zetten
                    # Fotografeer het sample in uv-----------------------------------------------------------------------
                    # io poort 4 aan voor uv
                    take_photo(f"Photo in uv licht van {sample}")
                    # io port 4 uit voor uv licht
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
                    grid[r][c] = f"{s} klaar"

        # Controleer of het grid volledig verwerkt is
        all_done = all(cell is None or "klaar" in str(cell) for row in grid for cell in row)
        if all_done:
            print("Alle samples zijn verwerkt. Start een nieuwe cyclus.")
        else:
            print("Nog niet alle samples zijn verwerkt.")

        time.sleep(5)  # Pause briefly before starting again
