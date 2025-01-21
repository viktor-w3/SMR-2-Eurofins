# Controlls/Camera_control/Make_photo.py
import os
from .Camera_module_2 import CameraHandler  # Use CameraHandler from the Camera_control module

def take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2"):
    """
    Takes three photos (clean, UV, and white) for each sample, saves them with unique names,
    and organizes them into directories.

    :param sample_base_name: The base name for the sample folder.
    :param output_dir_base: The base directory to save the photos in.
    :return: The list of paths where the photos are saved.
    """
    # Define the sample number based on the sample base name
    sample_name = f"{sample_base_name}"

    # Define the output directory where photos will be stored
    output_dir = os.path.join(output_dir_base, sample_name)

    # Ensure that the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the camera handler
    camera_handler = CameraHandler(output_dir=output_dir)

    photo_paths = []

    try:
        # Take the clean photo (normal light)
        clean_photo_name = f"{sample_name}_clean.jpg"
        clean_photo_path = os.path.join(output_dir, clean_photo_name)
        camera_handler.capture_photo(clean_photo_name)  # Capture the clean photo
        photo_paths.append(clean_photo_path)  # Add to the list of saved photo paths
        print(f"Clean photo saved: {clean_photo_path}")

        # Take the UV photo
        uv_photo_name = f"{sample_name}_UV.jpg"
        uv_photo_path = os.path.join(output_dir, uv_photo_name)
        camera_handler.capture_photo(uv_photo_name)  # Capture the UV photo
        photo_paths.append(uv_photo_path)  # Add to the list of saved photo paths
        print(f"UV photo saved: {uv_photo_path}")

        # Take the white light photo
        white_photo_name = f"{sample_name}_white.jpg"
        white_photo_path = os.path.join(output_dir, white_photo_name)
        camera_handler.capture_photo(white_photo_name)  # Capture the white light photo
        photo_paths.append(white_photo_path)  # Add to the list of saved photo paths
        print(f"White photo saved: {white_photo_path}")

        # Release the camera once done
        camera_handler.release_camera()

    except Exception as e:
        print(f"Error capturing photo: {e}")

    return photo_paths
