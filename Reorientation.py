import math
import time #import sleep function
import brickpi3 
import grovepi #import 

def findAngle():
    frontDist = grovepi.ultrasonicRead(sensor1)
    backDist = grovepi.ultrasonicRead(sensor2) #Correct for positive/negative
    if backDist == frontDist:
        angle = 0
    else:
        opposite = (robotLength * frontDist) / (backDist - frontDist)
        opposite += robotLength
        angle = math.atan(opposite / frontDist)
    return angle

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3
targetValue = 20
sensor1 = 1
sensor2 = 2
robotLength = 0 #distance between the two right sensors, in units of ultrasonic sensor length

try:
    while (findAngle() > 0):
        BP.set_motor_power(BP.PORT_B, -30)
        BP.set_motor_power(BP.PORT_C, 30)
        time.sleep(.01)
    while (findAngle() < 0):
        BP.set_motor_power(BP.PORT_B, 30)
        BP.set_motor_power(BP.PORT_C, -30)
        time.sleep(.01)
except IOError as error:
	print(error)
except TypeError as error:
	print(error)
except KeyboardInterrupt: #Preventing the user from cancelling the execution with CRTL + C . . . for some reason?
	print("You pressed ctrl+C...")


BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) #resets the motor encoder so that the output only 
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) #represents the relative offset???
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))

BP.reset_all() #resets the brick_PI


