from Servo_test import ServoSwitch
from LED_strip import LedColours
from Sensor_Test import SensorData

def startup():
    ServoSwitch() #runs servo program?
    LedColours() #runs led program?
    SensorData() #runs sensor program?

startup() #runs main program
