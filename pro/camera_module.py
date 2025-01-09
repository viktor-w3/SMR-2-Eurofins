import cv2
import os
import time

class CameraHandler:
    def __init__(self, output_dir="C:\\Users\\vikto\\Desktop\\Smr 2"):
        # Probeer de camera te openen
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def capture_photo(self):
        """Maak een foto en sla deze direct op."""
        if not self.cap.isOpened():
            print("Kan de camera niet openen.")
            return None

        # Wacht kort om de camera te laten stabiliseren
        time.sleep(1)  # Wacht 2 seconden
        print("Camera gestabiliseerd.")

        # Lees een paar frames om te zorgen dat de camera goed is ingesteld
        for _ in range(5):
            self.cap.read()

        # Neem het daadwerkelijke frame
        ret, frame = self.cap.read()
        if not ret:
            print("Kan geen frame lezen.")
            return None

        timestamp = int(time.time())  # Unieke timestamp
        photo_path = os.path.join(self.output_dir, f"photo_{timestamp}.jpg")
        cv2.imwrite(photo_path, frame)
        print(f"Foto opgeslagen: {photo_path}")
        return photo_path

    def release_camera(self):
        """Sluit de camera."""
        if self.cap.isOpened():
            self.cap.release()
        print("Camera vrijgegeven.")
