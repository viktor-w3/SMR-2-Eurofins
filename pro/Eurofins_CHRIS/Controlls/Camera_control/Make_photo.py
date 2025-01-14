# Controlls/Camera_control/Make_photo.py

from Camera_module import CameraHandler
import os

global photo_counter
photo_counter = 0

#een foto maken code
def take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\vikto\\Desktop\\Smr 2"):
    global photo_counter
    photo_counter += 1  # Verhoog de teller

    # Bereken de sample map (elke 3 foto's verandert de sample naam)
    sample_number = (photo_counter - 1) // 3 + 1
    sample_name = f"{sample_base_name}{sample_number}"
    output_dir = os.path.join(output_dir_base, sample_name)

    # Zorg ervoor dat de output-directory bestaat
    os.makedirs(output_dir, exist_ok=True)

    # Stel de bestandsnaam voor de foto in
    photo_name = f"{sample_name}_photo{photo_counter}.jpg"
    photo_path = os.path.join(output_dir, photo_name)

    # Maak de foto (camera-module)
    try:
        camera_handler = CameraHandler(output_dir=output_dir)
        camera_handler.capture_photo(photo_path)  # Specificeer de volledige bestandsnaam
        camera_handler.release_camera()
        print(f"Foto opgeslagen: {photo_path}")
    except Exception as e:
        print(f"Fout bij het maken van de foto: {e}")

    return photo_path