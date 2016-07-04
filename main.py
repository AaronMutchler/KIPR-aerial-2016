'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import time
import pixy
import os
import create_library

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

kD_x = 0.0125 * 5
kD_y = 0.0215 * 5

MAX_x = 20
MAX_y = 20

PREV_ERROR = Point(0, 0)

PID_DELAY = 0.02 # 0.01

TIME = time.time()
LOG_FILE = None

def main():
    create_library.make_functions_for_the_create_robot()
    create_library.connect_to_arduino()
    time.sleep(1.0)
    while True:
        if create_library.read_chr() == 's':
            break
    create_library.start() 
    create_library.full()

    drone = bebop.Bebop(8080, True)
    drone._send_string('send_to_drone_true')

    BLOCKS = pixy.BlockArray(1)
    pixy.pixy_init()

    #drone.connect()
    #drone.takeoff()
    start_logging()

    time.sleep(1)
    #drone.move_seconds('forward', 10, 2)
    create_library.drive_direct(50, 50) 
    desired = CENTER
    pid_loop(drone, CENTER, BLOCKS)

    drone.land()
    drone.disconnect()


def pid_loop(drone, desired, BLOCKS):
    while True:
        if False:
            drone.land()
            break

        if not os.path.exists("FLYING.txt"):
            stop_logging()
            while True:
                if os.path.exists("FLYING.txt"):
                  start_logging()
                  break
 
        actual = take_picture(BLOCKS)
        react(drone, actual, desired)
        time.sleep(PID_DELAY)


def react(drone, actual, desired):
    if actual == None:
        log()
        return

    global PREV_ERROR
    
    error = actual - desired
    delta_error = PREV_ERROR - error

    fb = 'forward' if error.y > 0 else 'backward'
    rl = 'right' if error.y > 0 else 'left'

    speed_x = int(round(abs(min((error.x * kP_x) + (delta_error.x * kD_x), MAX_x))))
    speed_y = int(round(abs(min(error.y * kP_y + (delta_error.y * kD_y), MAX_y))))

    drone.move(fb, speed_y)
    drone.move(rl, speed_x)

    PREV_ERROR = error

    log(actual, Point(speed_x, speed_y), fb, rl)
    

def take_picture(BLOCKS):
    block = get_block(BLOCKS)  # do error handling
    return Point(block.x, block.y) if block else None


def get_block(BLOCKS):
    count = pixy.pixy_get_blocks(1, BLOCKS)
    return BLOCKS[0] if count > 0 else None


def start_logging():
    global LOG_FILE
    LOG_FILE = open('log.txt', 'w')
    TIME = time.time()
    print(LOG_FILE)

def stop_logging():
    LOG_FILE.close()

def log(actual=None, speed=None, direction_y=None, direction_x=None):
    seconds = time.time() - TIME
    time_data = '{:5.2f}'.format(seconds)
    position_data = ' X/Y: {:3} {:3}'.format(actual.x, actual.y) if actual else ''

    #speed_data = ' Fwd/Right: {:3} {:3}'.format(speed.x, speed.y) if speed else ''
    speed_data = ' ' + direction_y + ': {:3} '.format(speed.y) + direction_x + ': {:3}'.format(speed.x) if speed else ''

    LOG_FILE.write(time_data + speed_data + position_data + '\n')
    #LOG_FILE.write(time_data + speed_data + '\n')
    #print(time_data + speed_data + position_data)

def run_from_input(drone):
    while True:
        s = input('Enter a String: ')
        if s == '':
            break
        drone._send_string(s)



if __name__ == '__main__':
    main()
