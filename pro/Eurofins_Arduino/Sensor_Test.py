import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)

it.start()

class SensorData:
    board.digital[2].mode = pyfirmata.INPUT #MUX 1
    board.digital[3].mode = pyfirmata.INPUT #MUX 2
    board.digital[4].mode = pyfirmata.OUTPUT #selector 1
    board.digital[6].mode = pyfirmata.OUTPUT #selector 2
    board.digital[7].mode = pyfirmata.OUTPUT #selector 3