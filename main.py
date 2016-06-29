'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import time
import pixy

BLOCKS = pixy.BlockArray(1)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y





def main():

    drone = bebop.Bebop(8080)

    BLOCKS = pixy.BlockArray(1)
    pixy.pixy_init()

    desired = Point(100, 100)
    pid_loop(drone, desired, BLOCKS)

    drone.land()
    drone.disconnect()


def pid_loop(drone, desired, BLOCKS):


    while True:
        if False:
            drone.land()
            break
        actual = take_picture(BLOCKS)
        react(drone, actual, desired)


def react(drone, actual, desired):
    print actual


def take_picture(BLOCKS):
    block = get_block(BLOCKS)  # do error handling
    return Point(block.x, block.y) if block else None


def get_block(BLOCKS):
    count = pixy.pixy_get_blocks(1, BLOCKS)
    return BLOCKS[0] if count > 0 else None


def run_from_input(drone):
    while True:
        s = input('Enter a String: ')
        if s == '':
            break
        drone._send_string(s)



if __name__ == '__main__':
    main()
