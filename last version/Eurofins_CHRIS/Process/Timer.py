# Process/Timer.py

import time

class Timer:
    def __init__(self):
        self.sample_timers = {}  # Dictionary to store timers for sensors

    def start_timer(self, sensor_id):
        """Start a new timer for the given sensor"""
        self.sample_timers[sensor_id] = time.time()

    def get_remaining_time(self, sensor_id, duration=120):
        """Get the remaining time for a sensor's drying process"""
        if sensor_id not in self.sample_timers:
            self.start_timer(sensor_id)  # Start the timer if it's not already started
        elapsed_time = int(time.time() - self.sample_timers[sensor_id])
        remaining_time = max(0, duration - elapsed_time)
        return remaining_time

    def is_timer_done(self, sensor_id, duration=120):
        """Check if the drying timer is done"""
        remaining_time = self.get_remaining_time(sensor_id, duration)
        return remaining_time == 0
