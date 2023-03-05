import math
import time #import sleep function
import brickpi3
import grovepi #import

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3
ultrasonic_sensor_port = 4
current_pos = [0, 0, 0]
pos_diff = [0, 0, 0]
xyswitch = 1
minusSwitch = 1

def turnright():
    print("turning right")
    BP.set_motor_power(BP.PORT_B, 30)
    BP.set_motor_power(BP.PORT_C, -30)
    time.sleep(1)

def turnleft():
    print("turning left")
    BP.set_motor_power(BP.PORT_B, -30)
    BP.set_motor_power(BP.PORT_C, 30)
    time.sleep(1)

try:
    for i in range(4):
        desired_pos = [0, 0, 0]
        desired_pos[1] = int(input("What is the x-coordinate you wish to go to? "))
        desired_pos[-1] = int(input("What is the y-coordinate you wish to go to? "))
        for axis in range(1,3):
            pos_diff[axis] = desired_pos[axis] - current_pos[axis]
        if pos_diff[xyswitch] < 0:
            minusSwitch = -1
        else:
            minusSwitch = 1
        for steps in range(pos_diff[xyswitch]):
            print("moving forward")
            
            #move forward 40 cm, multiply power by minusSwitch to move backwards

            #turn right, multiply power by minusSwitch to turn left every other time
            turnright()
        xyswitch *= -1
        if pos_diff[xyswitch] < 0:
            minusSwitch = -1
        else:
            minusSwitch = 1
        for steps in range(pos_diff[xyswitch]):
            print("moving forward")
            #move forward 40 cm, multiply power by minusSwitch to move backwards
        current_pos = desired_pos

        
except IOError as error:
	print(error)
#except TypeError as error:
	#print(error)
except KeyboardInterrupt: #Preventing the user from cancelling the execution with CRTL + C . . . for some reason?
	print("You pressed ctrl+C...")

BP.reset_all() #resets the brick_PI
