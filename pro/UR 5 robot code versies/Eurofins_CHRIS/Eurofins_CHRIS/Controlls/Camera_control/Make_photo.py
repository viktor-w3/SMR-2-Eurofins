<<<<<<< HEAD
# Controlls/Camera_control/Make_photo.py

import os
from .Camera_module_2 import CameraHandler  # Use CameraHandler from the Camera_control module

# Global photo counter (this can be better handled through a class or function arguments)
photo_counter = 0


def take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\...\\Desktop\\Smr 2"):
    """
    Takes a photo, saves it with a unique name, and organizes it into directories.

    :param sample_base_name: The base name for the sample folder.
    :param output_dir_base: The base directory to save the photos in.
    :return: The path where the photo is saved.
    """
    global photo_counter
    photo_counter += 1  # Increment the photo counter

    # Calculate the sample number based on the photo counter
    sample_number = (photo_counter - 1) // 3 + 1
    sample_name = f"{sample_base_name}{sample_number}"

    # Define the output directory where photos will be stored
    output_dir = os.path.join(output_dir_base, sample_name)

    # Ensure that the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the photo name and full path
    photo_name = f"{sample_name}_photo{photo_counter}.jpg"
    photo_path = os.path.join(output_dir, photo_name)

    # Try to create the photo using CameraHandler
    try:
        # Create the CameraHandler instance
        camera_handler = CameraHandler(output_dir=output_dir)

        # Capture the photo (CameraHandler will save it with the right name)
        camera_handler.capture_photo(photo_name)  # Specify only the photo name (CameraHandler handles directory)
        camera_handler.release_camera()  # Release the camera once done

        print(f"Photo saved: {photo_path}")

    except Exception as e:
        print(f"Error capturing photo: {e}")

    return photo_path
=======
# Controlls/Camera_control/Make_photo.py

import os
from .Camera_module_2 import CameraHandler  # Use CameraHandler from the Camera_control module

# Global photo counter (this can be better handled through a class or function arguments)
photo_counter = 0


def take_photo(sample_base_name="sample", output_dir_base="C:\\Users\\...\\Desktop\\Smr 2"):
    """
    Takes a photo, saves it with a unique name, and organizes it into directories.

    :param sample_base_name: The base name for the sample folder.
    :param output_dir_base: The base directory to save the photos in.
    :return: The path where the photo is saved.
    """
    global photo_counter
    photo_counter += 1  # Increment the photo counter

    # Ensure the base output directory exists
    if not os.path.exists(output_dir_base):
        os.makedirs(output_dir_base)

    # Calculate the sample number based on the photo counter
    sample_number = (photo_counter - 1) // 3 + 1
    sample_name = f"{sample_base_name}{sample_number}"

    # Define the output directory for the current sample
    sample_dir = os.path.join(output_dir_base, sample_name)

    # Ensure the sample directory exists
    os.makedirs(sample_dir, exist_ok=True)

    # Define the photo name and full path
    photo_name = f"{sample_name}_photo{photo_counter}.jpg"
    photo_path = os.path.join(sample_dir, photo_name)

    # Try to create the photo using CameraHandler
    try:
        # Assuming CameraHandler is a class defined elsewhere to handle camera operations
        camera_handler = CameraHandler(output_dir=sample_dir)  # Initialize with the sample directory

        # Capture the photo (CameraHandler will save it with the right name)
        camera_handler.capture_photo(photo_name)
        camera_handler.release_camera()  # Release the camera once done

        print(f"Photo saved: {photo_path}")

    except Exception as e:
        print(f"Error capturing photo: {e}")

    return photo_path
>>>>>>> 686489debd53e27e2d3c216190911a138916b44e
