'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import time
import pixy
import os
import create_library

# PID constants:
kP = Point(0.0125 * 5, 0.0215 * 5)
kD = Point(0.0125 * 5, 0.0215 * 5)
kI = Point(0, 0)
MAX_PITCH = 20
MAX_ROLL = 20
PID_DELAY = 0.02 # 0.01 

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({:3}, {:3})".format(self.x, self.y)

    def __sub__(self, other_point):
        return Point(self.x - other_point.x, self.y - other_point.y)

class Log(object):
    def __init__(self, logging_filename='log.txt', log_straight_to_file=True):
        self.filename = logging_filename
        self.log_straight_to_file = log_straight_to_file
        self.logging_list = None
        self.logging_file = None
        self.start_time = None
        self.is_logging = False
    
    def start_logging(self):        
        self.logging_list = []
        if self.log_straight_to_file:
            self.logging_file = open(self.filename, 'w')
            
        self.start_time = time.time()
        self.current_time = 0
        self.is_logging = True

    def stop_logging(self):
        self.is_logging = False
        
        # Write list to file if not logging straight to the file:
        if not self.log_straight_to_file:
            self.logging_file = open(self.filename, 'w')
            for log_item in self.logging_list:
                self.log_item(*log_item)

        self.logging_file.close()
        
    def log(self, state, action, error):
        current_time = time.time() - self.start_time
        if self.is_logging:
            if self.log_straight_to_file:
                self.log_item(current_time, state, action, error)
            else:
                self.logging_list.append([current_time, state, action, error])

    def log_item(self, timestamp, state, action, error):
        self.logging_file.write(timestamp + state + action + error + '\n')
    
class State(object):
    CENTER = Point(160, 100)

    def __init__(self, blocks_to_consider=3):
        self.blocks_to_consider = blocks_to_consider
        
        self.number_of_blocks = 0
        self._BLOCKS = pixy.BlockArray(self.blocks_to_consider)
        
        self.position = State.CENTER
        self.area = 0

    def __repr__(self):
        s = []
        s.append(self.position)
        s.append(s.area)
        for k in range(min(len(self._BLOCKS), self.blocks_to_consider)):
            s.append(' ({:3} {:3} {:4})'.format(self._BLOCKS[k].x,
                                                self._BLOCKS[k].y,
                                                self._BLOCKS[k].area))
        for k in range(self.blocks_to_consider - len(self._BLOCKS)):
                .append(' {:14}'.format(' '))
                
        return s.join()

    def update_state(self):
        self.number_of_blocks = pixy.pixy_get_blocks(self.blocks_to_consider,
                                                     self._BLOCKS)
        if self.number_of_blocks > 0:
            # CONSIDER: Use the middle of all big-enough blocks?
            self.position = Point(self._BLOCKS[0].x, self._BLOCKS[0].y)
            self.area = self._BLOCKS[0].area
        else:
            # CONSIDER: Estimate position based on previous position and velocity?
            # Or just leave it unchanged (as here)?
            pass

class Action(object):
    def __init__(self, pitch, roll, yaw, gaz):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.gaz = gaz
    
    def __repr__(self):
        return '({:2} {:2} {:2} {:2})'.format(self.pitch,
                                              self.roll,
                                              self.yaw,
                                              self.pitch)
    
    def __eq__(self, other_action):
        return (self.pitch == other_action.pitch) and \
            (self.roll == other_action.roll) and \
            (self.yaw = other_action.yaw) and \
            (self.gaz = other_action.yaz)

class PID(object):
    def __init__(self, drone, log, state, desired=None, kP=KP, kD=KD, kI=KI,
                 self.max_pitch=MAX_PITCH, self.max_roll=MAX_ROLL,
                 sum_discount_rate=SUM_DISCOUNT_RATE,
                 loop_delay=LOOP_DELAY):
        self.drone = drone
        self.log = log
        self.state = state
        self.desired = desired
        
        self.kP = kP
        self.kD = kD
        self.kI = kI
        
        self.max_pitch = max_pitch
        self.max_roll = max_roll
        
        self.SUM_DISCOUNT_RATE = sum_discount_rate
        self.LOOP_DELAY = loop_delay
        
        self.looping = False

    def loop(self):
        self.previous_error = 0
        self.sum_error = 0
        self.previous_action = None

        while self.looping:
            self.update_state()
            self.update_error()
            self.react()
            
            self.log.log()
            time.sleep(self.loop_delay)
        
    def update_state(self):
        self.state.update_state()
            
    def update_error(self):
        self.error = self.state.position - self.desired
        self.delta_error = self.previous_error - self.error
        self.sum_error = (self.sum_error * self.SUM_DISCOUNT_RATE) + self.error
        
        self.previous_error = self.error
        
    def react(self):
        pitch = (self.error.x * self.kP.x) + \
            (self.delta_error.x * self.kD.x) + \
            (self.sum_error.x * self.kI.x)
        pitch = round(max(min(pitch, self.max_pitch), -self.max_pitch))
        
        roll = (self.error.y * self.kP.y) + \
            (self.delta_error.y * self.kD.y) + \
            (self.sum_error.y * self.kI.y)
        roll = round(max(min(roll, self.max_roll), -self.max_roll))
        
        # If this new action is different than the previous action,
        # change to this action and send it to the drone.
        action = Action(pitch, roll, 0, 0)
        if self.action != action:
            self.action = action
            self.drone.move(self.action)

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
    global LOG_LIST
    global LOG_FILE
    LOG_FILE = open('log.txt', 'w')
    LOG_LIST = []
    TIME = time.time()

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
