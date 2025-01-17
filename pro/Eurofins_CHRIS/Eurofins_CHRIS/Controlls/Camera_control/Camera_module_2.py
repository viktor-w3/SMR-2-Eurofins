# Controlls/Camera_control/Camera_module_2.py

import cv2
import os
import time

class CameraHandler:
    def __init__(self, output_dir="C:\\Users\\...\\Desktop\\Smr 2"):
        # Probeer de camera te openen
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.sample_counter = 1  # Teller voor sample sets
        self.photo_counter_within_sample = 0  # Foto's binnen huidige sample-set

    def capture_photo(self, base_name="sample"):
        """Maak een foto en sla deze op. Verander naam na elke 3 foto's."""
        if not self.cap.isOpened():
            print("Kan de camera niet openen.")
            return None

        # Wacht kort om de camera te laten stabiliseren
        time.sleep(2)  # Wacht 2 seconden
        print("Camera gestabiliseerd.")

        # Lees een paar frames om te zorgen dat de camera goed is ingesteld
        for _ in range(5):
            self.cap.read()

        # Neem het daadwerkelijke frame
        ret, frame = self.cap.read()
        if not ret:
            print("Kan geen frame lezen.")
            return None

        # Genereer de naam op basis van de huidige sample set en foto nummer
        photo_name = f"{base_name}_{self.sample_counter}_photo_{self.photo_counter_within_sample + 1}.jpg"
        photo_path = os.path.join(self.output_dir, photo_name)
        cv2.imwrite(photo_path, frame)
        print(f"Foto opgeslagen: {photo_path}")

        # Update tellers
        self.photo_counter_within_sample += 1
        if self.photo_counter_within_sample == 3:  # Na 3 foto's overschakelen naar de volgende sample
            self.sample_counter += 1
            self.photo_counter_within_sample = 0

        return photo_path

    def release_camera(self):
        """Sluit de camera."""
        if self.cap.isOpened():
            self.cap.release()
        print("Camera vrijgegeven.")
