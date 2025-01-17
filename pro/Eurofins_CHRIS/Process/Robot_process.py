# Process/Robot_process.py

from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control import *
import time
from Config import SENSOR_TO_GRID_POSITION

def process_samples(self):
    drying_queue = []  # Track drying samples

    while True:  # Repeat the process continuously
        # Check each grid position for active samples
        for sensor_id in range(9):  # Loop through sensor IDs (0 to 8)
            grid_position = SENSOR_TO_GRID_POSITION.get(sensor_id)

            if grid_position:
                row, col = grid_position
                sample = grid[row][col]

                if sample and sample.startswith("sample"):  # If sample exists in grid
                    coordinates = grid_to_coordinates(row, col)

                    langzaam_naar_grid(coordinates, f"1. Slowly move to {sample} in grid")
                    move_robot(coordinates, f"2. Move to pick up {sample}")
                    pick_up(coordinates, f"3. Pick up {sample} with gripper adjustment", row)
                    orintatie_van_gripper(coordinates, f"4. Gripper orientation adjustment for {sample}")
                    er_uit_halen_van_kast(coordinates, f"5. Remove {sample} from the cabinet")

                    # Take photos for painting ------------------------------------------------------------------------------------------------------
                    move_robot_Photo1(coordinates, f"6. Moving for photos")
                    move_robot_Photo2(coordinates, f"6. Moving for photos")
                    move_robot_Photo3(coordinates, f"6. Moving for photos")
                    move_robot_Photo4(coordinates, f"6. Moving for photos")

                    # Turn on relay for light
                    take_photo(sample_base_name="sample", output_dir_base=f"Photo without paint of {sample}")

                    # Turn off relay for light
                    move_robot_Photo3(coordinates, f"6. Moving for photos")
                    move_robot_Photo2(coordinates, f"6. Moving for photos")
                    move_robot_Photo1(coordinates, f"6. Moving for photos")

                    # Painting movements -------------------------------------------------------------------------------------------------------------
                    move_robot_verf1(f"7. Moving for paint")
                    move_robot_verf2(f"7. Moving for paint")
                    move_robot_verf3(f"7. Moving for paint")
                    move_robot_verf4(f"7. Moving for paint")
                    move_robot_verf5(f"7. Moving for paint")

                    # Servo motor on
                    move_robot_verf6(f"7. Moving for paint")

                    # Servo motor off
                    vervenklaar(f"7. Painting done")
                    move_robot_verf1(f"7. Moving for paint")

                    # Back to storage -------------------------------------------------------------------------------------------------------------
                    move_robot_terug(coordinates, f"8. Return {sample} to storage")
                    het_in_de_kast_leggen(coordinates, f"9. Put {sample} in storage")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Gripper orientation out for {sample}")
                    terug_de_grijper_er_uit(coordinates, f"11. Remove gripper from {sample}")

                    # Add sample to drying queue
                    drying_queue.append((time.time(), row, col, sample))
                    print(f"{sample} added to drying queue at {time.strftime('%H:%M:%S')}.")

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
                    take_photo(f"Photo with paint under normal light of {s}")

                    # Relay for light off
                    take_photo(f"Photo in UV light of {s}")

                    # Return to storage
                    move_robot_terug(coordinates, f"8. Return {s} to storage")
                    het_in_de_kast_leggen(coordinates, f"9. Put {s} in storage")
                    orintatie_van_gripper_er_uit(coordinates, f"10. Gripper orientation out for {s}")
                    terug_de_grijper_er_uit(coordinates, f"11. Remove gripper from {s}")

                    # Mark sample as done
                    grid[r][c] = f"{s} done"

        # Check if the grid is fully processed
        all_done = all(cell is None or "done" in str(cell) for row in grid for cell in row)
        if all_done:
            print("All samples processed. Starting a new cycle.")
        else:
            print("Not all samples are processed.")

        time.sleep(5)  # Pause briefly before starting again
