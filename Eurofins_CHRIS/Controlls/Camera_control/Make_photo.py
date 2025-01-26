# Controlls/Camera_control/Make_photo.py
import os
from .Camera_module_2 import CameraHandler  # Assuming CameraHandler is the correct class for handling the camera


def take_clean_photo(sample_base_name="sample", output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2"):
    """
    Takes a clean photo (normal light) for each sample and saves it with a unique name.

    :param sample_base_name: The base name for the sample folder.
    :param output_dir_base: The base directory to save the photos in.
    :return: The path where the clean photo is saved.
    """
    # Define the sample name and output directory
    sample_name = f"{sample_base_name}"
    output_dir = os.path.join(output_dir_base, sample_name)
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the camera handler
    camera_handler = CameraHandler(output_dir=output_dir)

    try:
        # Take the clean photo (normal light)
        clean_photo_name = f"{sample_name}_clean.jpg"
        clean_photo_path = os.path.join(output_dir, clean_photo_name)
        camera_handler.capture_photo(clean_photo_name)  # Capture the clean photo
        print(f"Clean photo saved: {clean_photo_path}")

        # Release the camera once done
        camera_handler.release_camera()

    except Exception as e:
        print(f"Error capturing clean photo: {e}")
        clean_photo_path = None

    return clean_photo_path


def take_uv_photo(sample_base_name="sample", output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2"):
    """
    Takes a UV photo for each sample and saves it with a unique name.

    :param sample_base_name: The base name for the sample folder.
    :param output_dir_base: The base directory to save the photos in.
    :return: The path where the UV photo is saved.
    """
    # Define the sample name and output directory
    sample_name = f"{sample_base_name}"
    output_dir = os.path.join(output_dir_base, sample_name)
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the camera handler
    camera_handler = CameraHandler(output_dir=output_dir)

    try:
        # Take the UV photo
        uv_photo_name = f"{sample_name}_UV.jpg"
        uv_photo_path = os.path.join(output_dir, uv_photo_name)
        camera_handler.capture_photo(uv_photo_name)  # Capture the UV photo
        print(f"UV photo saved: {uv_photo_path}")

        # Release the camera once done
        camera_handler.release_camera()

    except Exception as e:
        print(f"Error capturing UV photo: {e}")
        uv_photo_path = None

    return uv_photo_path


def take_white_photo(sample_base_name="sample", output_dir_base="C:\\Users\\Denri\\Desktop\\Smr 2"):
    """
    Takes a white light photo for each sample and saves it with a unique name.

    :param sample_base_name: The base name for the sample folder.
    :param output_dir_base: The base directory to save the photos in.
    :return: The path where the white light photo is saved.
    """
    # Define the sample name and output directory
    sample_name = f"{sample_base_name}"
    output_dir = os.path.join(output_dir_base, sample_name)
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the camera handler
    camera_handler = CameraHandler(output_dir=output_dir)

    try:
        # Take the white light photo
        white_photo_name = f"{sample_name}_white.jpg"
        white_photo_path = os.path.join(output_dir, white_photo_name)
        camera_handler.capture_photo(white_photo_name)  # Capture the white photo
        print(f"White photo saved: {white_photo_path}")

        # Release the camera once done
        camera_handler.release_camera()

    except Exception as e:
        print(f"Error capturing white light photo: {e}")
        white_photo_path = None

    return white_photo_path
