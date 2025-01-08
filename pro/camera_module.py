import cv2
import os
import threading
import time

class CameraHandler:
    def __init__(self, output_dir="C:\\Users\\vikto\\Desktop\\Smr 2"):
        # Probeer de camera met DirectShow backend te openen
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
        self.frame = None
        self.running = True
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.lock = threading.Lock()  # Voor veilige toegang tot gedeelde data

    def start_camera(self):
        """Start de camera en blijf frames lezen."""
        if not self.cap.isOpened():
            print("Kan de camera niet openen.")
            return

        print("Camera gestart. Live stream actief...")
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Kan frame niet lezen.")
                break
            with self.lock:
                self.frame = frame  # Sla het huidige frame op
            # Toon de live stream (optioneel)
            cv2.imshow("Live Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Live stream gestopt.")
                self.stop()
                break
        self.stop()
        self.cap.release()
        cv2.destroyAllWindows()

    def capture_photo(self):
        """Maak een foto en sla deze op."""
        with self.lock:
            if self.frame is not None:
                timestamp = int(time.time())  # Unieke timestamp
                photo_path = os.path.join(self.output_dir, f"photo_{timestamp}.jpg")
                cv2.imwrite(photo_path, self.frame)
                print(f"Foto opgeslagen: {photo_path}")
                return photo_path
            else:
                print("Geen frame beschikbaar om een foto te maken.")
                return None

    def stop(self):
        """Stop de camera."""
        self.running = False
        print("Camera gestopt.")

def run_camera_in_background(output_dir="captured_photos"):
    """Functie om de camera in de achtergrond te starten."""
    camera_handler = CameraHandler(output_dir=output_dir)
    camera_thread = threading.Thread(target=camera_handler.start_camera)
    camera_thread.daemon = True  # Zorgt ervoor dat de thread eindigt wanneer het hoofdprogramma stopt
    camera_thread.start()
    return camera_handler, camera_thread
