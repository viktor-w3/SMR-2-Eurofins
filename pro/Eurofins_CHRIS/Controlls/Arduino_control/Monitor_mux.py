# Controlls/Arduino_control/Monitor_mux.py

from .Mux_control import MuxControl
from .Led_control import LEDControl

class MuxStatusTracker:
    def __init__(self, mux_control: MuxControl, led_control: LEDControl):
        self.mux_control = mux_control
        self.led_control = led_control

    def monitor_mux_and_control_leds(self):
        """Monitor multiplexer channels and control corresponding LEDs."""
        sensor_to_mux_channel = {
            0: (1, 0), 4: (1, 1), 2: (1, 2), 3: (1, 3), 1: (1, 4),
            5: (0, 0), 8: (0, 1), 7: (0, 2), 6: (0, 4)
        }

        sensor_to_led_strip = {
            0: (0, 0, 9), 1: (0, 10, 19), 2: (0, 20, 29),
            3: (1, 0, 9), 4: (1, 10, 20), 5: (1, 21, 29),
            6: (2, 0, 9), 7: (2, 10, 19), 8: (2, 20, 29)
        }

        for sensor_id in range(9):
            print(f"Checking sensor {sensor_id}...")

            # Map sensor ID to multiplexer and channel
            mux_number, channel_number = sensor_to_mux_channel[sensor_id]

            # Read the status of the channel using the correct method (read_mux_channel)
            sensor_status = self.mux_control.read_mux_channel(mux_number, channel_number)

            if sensor_status is None:
                print(f"Sensor {sensor_id} failed to respond or invalid.")
                continue

            # Map the sensor to LED strip indices
            led_strip, start_led, end_led = sensor_to_led_strip[sensor_id]

            # Act based on sensor status
            if sensor_status == '0':
                print(f"Sensor {sensor_id} is LOW. Turning LEDs red.")
                self.led_control.set_led_range(led_strip, start_led, end_led, "Red")
            elif sensor_status == '1':
                print(f"Sensor {sensor_id} is HIGH. Turning LEDs off.")
                self.led_control.set_led_range(led_strip, start_led, end_led, "Green")
