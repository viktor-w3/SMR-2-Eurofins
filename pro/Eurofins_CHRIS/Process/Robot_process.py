# Process/Robot_process.py

from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control import *
import time
from Config import SENSOR_TO_GRID_POSITION

def process_samples(self):
    drying_queue = []  # Track drying samples

    while True:
        # Check each sensor
        for sensor_id in range(9):
            grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)

            if not grid_position:
                print(f"Sensor ID {sensor_id} is not mapped.")
                continue

            rij, kolom = grid_position
            try:
                sample = grid[rij][kolom]
            except IndexError:
                print(f"Invalid grid position: rij={rij}, kolom={kolom}. Skipping.")
                continue

            if sample and sample.startswith("sample"):
                print(f"Processing {sample} at grid[{rij}][{kolom}]...")
                coordinates = grid_to_coordinates(rij, kolom)

                #
                # grid controleren op sampel
                #

                langzaam_naar_grid(coordinates, f"1. Slowly move to {sample} in grid")
                move_robot(coordinates, f"2. Move to pick up {sample}")
                pick_up(coordinates, rij, f"3. Pick up {sample} with gripper adjustment")
                orintatie_van_gripper(coordinates, f"4. Adjust gripper for {sample}")
                er_uit_halen_van_kast(coordinates, f"5. Remove {sample} from cabinet")
                # photo maken voor verven------------------------------------------------------------------------------------------------------
                move_robot_Photo1(coordinates, f"6.moven voor fotos")
                move_robot_Photo2(coordinates, f"6.moven voor fotos")
                move_robot_Photo3(coordinates, f"6.moven voor fotos")
                move_robot_Photo4(coordinates, f"6.moven voor fotos")
                
                led_control.set_led_range(3, 0, 29, "White")
                take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2"f"Photo zonder verf van {sample}")
                led_control.set_led_range(3, 0, 29, "lBack")
                
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
                
                servo_control.initialize_servo()
                move_robot_verf6(f"7.moven voor fotos")
                servo_control.servo_off()

                vervenklaar(f"7.vervenklaar")
                move_robot_verf1(f"7.moven voor fotos")
                # klaar met verven-------------------------------------------------------------------------------------------------------------
                move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                orintatie_van_gripper_er_uit(coordinates, f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sample} weg te halen")

                #
                # grid controleren op sampel
                #


                # Add to drying queue
                drying_queue.append((time.time(), rij, kolom, sample))
                print(f"{sample} added to drying queue.")
        # Wait until all samples are dry
        while drying_queue:
            drying_queue.sort(key=lambda x: x[0])  # Sort by drying time

            current_time = time.time()
            for start_time, r, c, s in drying_queue[:]:
                elapsed = int(current_time - start_time)
                if elapsed < 120:  # Check drying time
                    print(f"{s} is drying. Time elapsed: {elapsed // 60}m {elapsed % 60}s.")
                else:
                    # Sample is dry, process it
                    drying_queue.remove((start_time, r, c, s))
                    print(f"{s} is now dry and ready for photo.")

                    # Move to sample
                    coordinates = grid_to_coordinates(r, c)
                    langzaam_naar_grid(coordinates, f"1. Slowly move to {s} in grid")
                    move_robot(coordinates, f"2. Move to pick up {s}")
                    pick_up(coordinates, f"3. Pick up {s} with gripper", r)
                    orintatie_van_gripper(coordinates, f"4. Gripper orientation adjustment for {s}")
                    er_uit_halen_van_kast(coordinates, f"5. Remove {s} from cabinet")

                    # Take photos
                    move_robot_Photo1(coordinates, f"6. Moving for photos")
                    move_robot_Photo2(coordinates, f"6. Moving for photos")
                    move_robot_Photo3(coordinates, f"6. Moving for photos")
                    move_robot_Photo4(coordinates, f"6. Moving for photos")

                    # Relay for light on
                    led_control.set_led_range(3, 0, 29, "White")
                    take_photo(f"Photo with paint under normal light of {s}")
                    led_control.set_led_range(3, 0, 29, "Black")
                    # Relay for light off
                    
                    #uv foto
                    io_ports_init(4)
                    take_photo(f"Photo in UV light of {s}")
                    deactivate_io_port(4)

                    # Return to storage
                    move_robot_terug(coordinates, f"8. Return {s} to storage")
                    het_in_de_kast_leggen(coordinates, f"9. Put {s} in storage")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Gripper orientation out for {s}")
                    terug_de_grijper_er_uit(coordinates, f"11. Remove gripper from {s}")

                    # Mark sample as done
                    grid[r][c] = f"{s} done"

                    #
                    # grid controleren op sampel
                    #

        # Check if the grid is fully processed
        all_done = all(cell is None or "done" in str(cell) for row in grid for cell in row)
        if all_done:
            print("All samples processed. Starting a new cycle.")
        else:
            print("Not all samples are processed.")

        time.sleep(5)  # Pause briefly before starting again
