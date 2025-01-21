# Controlls/Camera_control/Camera_module_2.py
import cv2
import os
import time


class CameraHandler:
    def __init__(self, output_dir="C:\\Users\\Denri\\Desktop\\Smr 2\\"):
        """
        Initializes the CameraHandler object. Opens the camera and sets up the output directory for photos.

        :param output_dir: Base directory to save photos.
        """
        # Try to open the camera
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.sample_counter = 1  # Counter for sample sets
        self.photo_counter_within_sample = 0  # Counter for photos within the current sample set

    def capture_photo(self, base_name="sample"):
        """
        Captures a photo, saves it with a unique name, and increments the counters.

        :param base_name: Base name for the photo (e.g., 'sample')
        :return: The path to the saved photo.
        """
        if not self.cap.isOpened():
            print("Error: Unable to open the camera.")
            return None

        # Allow the camera to stabilize
        time.sleep(2)  # This could be adjusted if needed

        # Read a few frames to allow the camera to adjust
        for _ in range(5):
            self.cap.read()

        # Capture the actual frame
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Unable to capture frame.")
            return None

        # Generate the photo file name
        photo_name = f"{base_name}_{self.sample_counter}_photo_{self.photo_counter_within_sample + 1}.jpg"
        photo_path = os.path.join(self.output_dir, photo_name)

        # Save the photo to the defined path
        cv2.imwrite(photo_path, frame)
        print(f"Photo saved: {photo_path}")

        # Update counters
        self.photo_counter_within_sample += 1
        if self.photo_counter_within_sample == 3:  # After 3 photos, move to the next sample
            self.sample_counter += 1
            self.photo_counter_within_sample = 0

        return photo_path

    def release_camera(self):
        """Releases the camera when done."""
        if self.cap.isOpened():
            self.cap.release()
        print("Camera released.")
