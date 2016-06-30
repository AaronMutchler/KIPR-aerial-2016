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
MAX_x = 5
MAX_y = 5
PID_DELAY = 0.6

def main():
    
    drone = bebop.Bebop(8080, False)

    BLOCKS = pixy.BlockArray(1)
    pixy.pixy_init()

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

    speed_y = int(round(min(error.y * kP_y, MAX_y)))
    if speed_y < 0:
        speed_y = max(speed_y, -MAX_y)
        
    speed_x = int(round(min(error.x * kP_x, MAX_x)))
    if speed_x < 0:
        speed_x = max(speed_x, -MAX_x)
    drone.move('forward', speed_y)
    drone.move('right', speed_x)
    
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
