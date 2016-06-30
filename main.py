'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import time
import pixy

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __repr__(self):
        return "({:3}, {:3})".format(self.x, self.y)


    def __sub__(self, other_point):
        return Point(self.x - other_point.x, self.y - other_point.y)
    

CENTER = Point(160, 100)
BLOCKS = pixy.BlockArray(1)
kP_x = 0.0125 * 5
kP_y = 0.0215 * 5
MAX_x = 10
MAX_y = 10
PID_DELAY = 0.01

def main():
    
    drone = bebop.Bebop(8080)
    drone._send_string('send_to_drone_true')

    BLOCKS = pixy.BlockArray(1)
    pixy.pixy_init()

    drone.connect()
    drone.takeoff()
    time.sleep(1)
    drone.move_seconds('forward', 10, 2)
    
    desired = CENTER
    pid_loop(drone, CENTER, BLOCKS)

    drone.land()
    drone.disconnect()


def pid_loop(drone, desired, BLOCKS):


    while True:
        if False:
            drone.land()
            break
        actual = take_picture(BLOCKS)
        react(drone, actual, desired)
        time.sleep(PID_DELAY)


def react(drone, actual, desired):
    if actual == None:
        return
    
    error = actual - desired
    fb = ''
    rl = ''

    speed_y = int(round(abs(min(error.y * kP_y, MAX_y))))
    fb = 'forward' if error.y > 0 else 'backward'
    speed_x = int(round(abs(min(error.x * kP_x, MAX_x))))
    rl = 'right' if error.y > 0 else 'left'
    drone.move(fb, speed_y)
    drone.move(rl, speed_x)
    
    #print '{:4}, {:4}'.format(speed_x, speed_y)


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
