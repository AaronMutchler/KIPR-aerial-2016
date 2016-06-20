'''
Created on Jun 19, 2016

@author: Aaron
'''

import socket
import time


class drone(object):
    '''
    classdocs
    '''


    def __init__(self, port):
        '''
        Constructs a new drone object with a connection to a given port
        
        :type port: int
        '''
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', port))


    def move(self, direction, speed):
        '''
        Moves the drone in a given direction at a given speed (1-10)
        
        - Direction must be one of the following:
            - 'forward'
            - 'backward'
            - 'left'
            - 'right'
            - 'up'
            - 'down'
            - 'clockwise'
            - 'counterClockwise'
        
        Preconditions:
        :type direction: string
        :type speed: int
        '''
        self._set_speed(speed)
        self._send_string(direction)

    def move_seconds(self, direction, speed, seconds):
        '''
        Moves the drone in a given direction at a given speed for a given amount of time in seconds
        
        - Direction must be one of the following:
            - 'forward'
            - 'backward'
            - 'left'
            - 'right'
            - 'up'
            - 'down'
            - 'clockwise'
            - 'counterClockwise'
        - Speed is a value between 1 and 10 (inclusive)
        
        Preconditions:
        :type direction: string
        :type speed: int
        :type seconds: float
        '''
        self.move(direction, speed)
        time.sleep(seconds)
        self.stop()


    def stop(self):
        '''
        Stops the drone's current motion and resets the speed to 1
        '''
        self._send_string('stop')
        self._set_speed(1)


    def land(self):
        '''
        Lands the drone
        '''
        self._send_string('land')


    def connect(self):
        '''
        Connects the nodejs server to the drone
        '''
        self._send_string('connect')


    def takeoff(self):
        self._send_string('takeoff')


    def emergency(self):
        self._send_string('emergency')


    def disconnect(self):
        self.client.shutdown(socket.SHUT_WR)
        self.client.close()


    def _set_speed(self, speed):
        '''
        Changes the speed of the drone. Value must be between 1 and 10
        
        Preconditions:
        :type speed: int
        '''
        if speed > 10:
            speed = 10
        elif speed < 1:
            speed = 1
        speed_msg = 'speed' + str(speed * 10)
        self._send_string(speed_msg)


    def _send_string(self, string):
        '''
        Sends the string to a client
        
        Preconditions:
        :type client: socket
        :type string: string
        '''
        self.client.send(str.encode(string))
        time.sleep(.05)




