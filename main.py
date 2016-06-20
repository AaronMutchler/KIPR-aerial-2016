'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop

def main():
    drone = bebop.drone(8080)
    drone.connect()
    drone.takeoff()
    drone.move_seconds('forward', 3, 2)
    drone.move_seconds('left', 3, 2)
    drone.move_seconds('backward', 3, 2)
    drone.land()
    drone.disconnect()

if __name__ == '__main__':
    main()
