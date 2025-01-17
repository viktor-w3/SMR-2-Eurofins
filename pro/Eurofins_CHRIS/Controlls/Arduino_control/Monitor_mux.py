# Controlls/Arduino_control/Monitor_mux.py

from .Mux_control import MuxControl
from .Led_control import LEDControl
from Config import SENSOR_TO_MUX_CHANNEL, SENSOR_TO_LED_STRIP

class MuxStatusTracker:
    def __init__(self, mux_control, led_control, sensor_to_mux_channel, sensor_to_led_strip):
        self.mux_control = mux_control
        self.led_control = led_control
        self.sensor_to_mux_channel = sensor_to_mux_channel
        self.sensor_to_led_strip = sensor_to_led_strip

    def monitor_mux_and_control_leds(self):
        """
        Monitor multiplexer channels and control LEDs based on the sensor status.
        Each sensor is checked 5 times, and the LED status is updated only if the sensor is HIGH most of the time.
        """
        for sensor_id in SENSOR_TO_MUX_CHANNEL:
            mux_number, channel_number = SENSOR_TO_MUX_CHANNEL[sensor_id]

            # Check the sensor status 5 times
            status_votes = []
            for _ in range(3):
                status = self.mux_control.read_mux_channel(mux_number, channel_number)
                if status is not None:
                    status_votes.append(status == 1)  # Store True for HIGH (1), False for LOW (0)

            # Determine the majority vote
            high_count = sum(status_votes)
            is_active = high_count >= 2  # HIGH must occur at least 3 times to be considered active

            # Get LED strip indices
            strip_index, start_index, end_index = SENSOR_TO_LED_STRIP[sensor_id]

            print(f"Sensor {sensor_id}: Active={is_active}, MUX={mux_number}, Channel={channel_number}, "
                  f"LED Range=Strip {strip_index}, LEDs {start_index}-{end_index}")

            # Update LED status based on the majority vote
            if is_active:
                self.led_control.set_led_range(strip_index, start_index, end_index, "Green")
            else:
                self.led_control.set_led_range(strip_index, start_index, end_index, "Red")
