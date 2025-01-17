# Process/Robot_process.py

from Controlls.Robot_control import *
from Controlls.Camera_control import *
from Controlls.Arduino_control import *
import time


def process_samples(self):
    while True:  # Herhaal het proces continu
        drying_queue = []  # Houdt bij welke samples drogen

        # Verf en droog samples
        for rij in range(len(grid)):
            for kolom in range(len(grid[rij])):
                if grid[rij][kolom] is not None:
                    sample = grid[rij][kolom]
                    coordinates = grid_to_coordinates(rij, kolom)

                    langzaam_naar_grid(coordinates, f"1. Langzaam naar {sample} in grid")
                    move_robot(coordinates, f"2. Beweging om {sample} op te pakken")
                    grid[rij][kolom] = None
                    pick_up(coordinates, f"3. Pakken van {sample} met aanpassing van de grijper",
                            rij)  # Pass 'rij' here
                    orintatie_van_gripper(coordinates, f"4. Orintatie van {sample} gripper aanpassing in grid")
                    er_uit_halen_van_kast(coordinates, f"5. Er uit halen van {sample}")

                    # Foto maken voor verven ------------------------------------------------------------------------------------------------------
                    move_robot_Photo1(coordinates, f"6.moven voor foto's")
                    move_robot_Photo2(coordinates, f"6.moven voor foto's")
                    move_robot_Photo3(coordinates, f"6.moven voor foto's")
                    move_robot_Photo4(coordinates, f"6.moven voor foto's")

                    # Rele schakelen voor licht
                    take_photo(sample_base_name="sample",
                               output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2" f"Photo zonder verf van {sample}")

                    # Rele uitschakelen voor licht
                    move_robot_Photo3(coordinates, f"6.moven voor foto's")
                    move_robot_Photo2(coordinates, f"6.moven voor foto's")
                    move_robot_Photo1(coordinates, f"6.moven voor foto's")

                    # Foto voor verven klaar ------------------------------------------------------------------------------------------------------

                    # Bewegingen voor het verven ---------------------------------------------------------------------------------------------------
                    move_robot_verf1(f"7.moven voor verf")
                    move_robot_verf2(f"7.moven voor verf")
                    move_robot_verf3(f"7.moven voor verf")
                    move_robot_verf4(f"7.moven voor verf")
                    move_robot_verf5(f"7.moven voor verf")

                    # Servomotor aan
                    move_robot_verf6(f"7.moven voor verf")

                    # Servomotor uit
                    vervenklaar(f"7.vervenklaar")
                    move_robot_verf1(f"7.moven voor verf")

                    # Klaar met verven -------------------------------------------------------------------------------------------------------------
                    move_robot_terug(coordinates, f"8. Beweging om {sample} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {sample} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates,
                                                 f"10. Orintatie van {sample} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {sample} weg te halen")
                    grid[rij][kolom] = sample

                    # Voeg toe aan drooglijst
                    drying_queue.append((time.time(), rij, kolom, sample))
                    print(f"{sample} toegevoegd aan drooglijst op {time.strftime('%H:%M:%S')}.")

        # Wachten tot alles droog is en foto's maken
        while drying_queue:
            drying_queue.sort(key=lambda x: x[0])  # Sorteer op droogtijd

            current_time = time.time()
            for start_time, r, c, s in drying_queue[:]:
                elapsed = int(current_time - start_time)
                if elapsed < 120:  # Controleer droogtijd
                    print(f"{s} is aan het drogen. Tijd verstreken: {elapsed // 60}m {elapsed % 60}s.")
                else:
                    # Sample is droog, verwerk het
                    drying_queue.remove((start_time, r, c, s))
                    print(f"{s} is nu droog en klaar voor foto.")

                    # Beweeg naar het sample
                    coordinates = grid_to_coordinates(r, c)
                    langzaam_naar_grid(coordinates, f"1. Langzaam naar {s} in grid")
                    move_robot(coordinates, f"2. Beweging om {s} op te pakken")
                    pick_up(coordinates, f"3. Pakken van {s} met aanpassing van de grijper",
                            r)  # Pass 'r' (row index) here
                    orintatie_van_gripper(coordinates, f"4. Orintatie van {s} gripper aanpassing in grid")
                    er_uit_halen_van_kast(coordinates, f"5. Er uit halen van {s}")

                    # Fotografeer het sample
                    move_robot_Photo1(coordinates, f"6.moven voor foto's")
                    move_robot_Photo2(coordinates, f"6.moven voor foto's")
                    move_robot_Photo3(coordinates, f"6.moven voor foto's")
                    move_robot_Photo4(coordinates, f"6.moven voor foto's")

                    # Rele schakelen voor licht
                    take_photo(f"Photo met verf in normaal licht van {s}")

                    # Rele schakelen voor licht uit te zetten
                    # Fotografeer het sample in uv-----------------------------------------------------------------------
                    # IO poort 4 aan voor UV
                    take_photo(f"Photo in uv licht van {s}")
                    # IO poort 4 uit voor UV licht
                    move_robot_Photo3(coordinates, f"6.moven voor foto's")
                    move_robot_Photo2(coordinates, f"6.moven voor foto's")
                    move_robot_Photo1(coordinates, f"6.moven voor foto's")

                    # Terug leggen
                    move_robot_terug(coordinates, f"8. Beweging om {s} terug te leggen")
                    het_in_de_kast_leggen(coordinates, f"9. Beweging om {s} terug te leggen")
                    orintatie_van_gripper_er_uit(coordinates,
                                                 f"10. Orintatie van {s} gripper aanpassing in grid om er uit te gaan")
                    terug_de_grijper_er_uit(coordinates, f"11. Beweging om grijper van {s} weg te halen")

                    # Markeer sample als klaar
                    grid[r][c] = f"{s} klaar"

        # Controleer of het grid volledig verwerkt is
        all_done = all(cell is None or "klaar" in str(cell) for row in grid for cell in row)
        if all_done:
            print("Alle samples zijn verwerkt. Start een nieuwe cyclus.")
        else:
            print("Nog niet alle samples zijn verwerkt.")

        time.sleep(5)  # Pauzeer kort voordat je opnieuw begint
