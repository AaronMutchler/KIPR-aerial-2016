'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import time

def main():

    drone = bebop.Bebop(8080)

     while True:
         s = input('Enter a String: ')
         if s == '':
             break
         drone._send_string(s)

#    drone.connect()
#    drone.takeoff()
#    time.sleep(2)
#    drone.move_seconds('forward', 18, 2)
#    time.sleep(1)
#    drone.move_seconds('backward', 1, 5)
    drone.land()
    drone.disconnect()



if __name__ == '__main__':
    main()
