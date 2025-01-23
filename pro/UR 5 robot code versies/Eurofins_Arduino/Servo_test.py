import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)

it.start()

class ServoSwitch:
    board.digital[1].mode = pyfirmata.INPUT  # temporary button for testing.
    servo = board.digital('d:5:p')  # Set servo to digital pin 5 PWM mode.

    while True:

        sw = board.digital[1].read() #If switch is pressed, write 225 to servo in PWM
        if sw is True:
            servo.write(225)
        else:
            servo.write(0) #If switch is released, write 0 to servo in PWM
        time.sleep(0.1)
