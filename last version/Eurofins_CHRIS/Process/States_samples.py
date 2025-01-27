# Process/States_samples.py
from Config import SENSOR_TO_GRID_POSITION
from enum import Enum
from Process.Timer import Timer
import time

class SensorState(Enum):
    NO_SAMPLE = "No_sample"
    NEW_SAMPLE = "New_sample"
    DRYING_SAMPLE = "Drying_sample"
    DRIED_SAMPLE = "Dried_sample"
    DONE_SAMPLE = "Done_sample"

class TimerSensor:
    def __init__(self):
        self.start_time = None  # To store the start time of the timer

    def start(self):
        """Start the timer."""
        self.start_time = time.time()

    def get_remaining_time(self, duration=120):
        """Get the remaining time based on the given duration."""
        if self.start_time is None:
            return duration  # Timer hasn't started, return the full duration
        elapsed_time = int(time.time() - self.start_time)
        return max(0, duration - elapsed_time)

    def is_done(self, duration=120):
        """Check if the timer is finished."""
        return self.get_remaining_time(duration) == 0

    def reset(self):
        """Reset the timer."""
        self.start_time = None




class Sensor:
    timer_manager = Timer()

    def __init__(self, sensor_id, current_state = SensorState.NO_SAMPLE):
        self.sensor_id = sensor_id

        self.current_state = current_state  # Initial state is No_sample
        self.position = SENSOR_TO_GRID_POSITION.get(sensor_id, None)
        if not self.position:
            raise ValueError(f"Sensor ID {sensor_id} is not defined in the grid.")
        self.timer = TimerSensor()

    def update_state(self, new_state):
        """Update the sensor state"""
        self.current_state = new_state

        # Automatically start the timer when transitioning to the DRYING_SAMPLE state
        if self.current_state == SensorState.DRYING_SAMPLE:
            self.timer.start()
            print(f"Timer started for Sensor {self.sensor_id}.")

    def check_timer(self, duration=120):
        """
        Check the remaining time or completion status of the timer.
        :param duration: Total duration of the drying process in seconds (default: 120 seconds).
        :return: A tuple (is_done, remaining_time).
        """
        remaining_time = self.timer.get_remaining_time(duration)
        is_done = self.timer.is_done(duration)
        return is_done, remaining_time

    def reset_timer(self):
        """Reset the timer for this sensor."""
        self.timer.reset()
        print(f"Timer reset for Sensor {self.sensor_id}.")

    def __str__(self):
        """String representation of the sensor for easy debugging."""
        return f"Sensor ID: {self.sensor_id}, Position: {self.position}, State: {self.current_state}, Timer: {self.timer}"

    @classmethod
    def get_sensor_count(cls):
        """Class method to get the total number of sensors based on the grid."""
        return len(SENSOR_TO_GRID_POSITION)
