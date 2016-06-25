import pixy
import ctypes as ct
import math
import time

BLOCKS = pixy.BlockArray(1)

class Point ():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Blocks (ct.Structure):
    _fields_ = [ ("type", ct.c_uint),
                 ("signature", ct.c_uint),
                 ("x", ct.c_uint),
                 ("y", ct.c_uint),
                 ("width", ct.c_uint),
                 ("height", ct.c_uint),
                 ("angle", ct.c_uint) ]


def pid(desired_point, kP=0):
    '''
    :type desired_point: Point
    :type kP: float
    :type kI: float
    :type kD: float
    '''


    pixy.pixy_init()

    while True:
        block = get_block()
        actual_point = Point(block[0].x, block[0].y)

        x_error = desired_point.x - actual_point.x
        direction = 'right'
        if x_error < 0:
            direction = 'left'

        x_speed = math.floor(x_error * kP * 30)
        print ('D: ', desired_point.x, desired_point.y)
        print ('A: ', actual_point.x, actual_point.y)
        print(direction, x_speed)
        time.sleep(.5)


def get_block():
    count = pixy.pixy_get_blocks(1, BLOCKS)
    if count == 0:
        return None
    return BLOCKS[0]

pid(Point(100, 100), 0.1)