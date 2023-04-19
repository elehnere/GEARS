import math
import time #import sleep function
import brickpi3 
import grovepi #import 

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3
#SET THESE TO THE RIGHT VALUES LATER
leftSensor = 4
frontSensor = 5
rightSensor = 6

def turnright():
    print("turning right")
    BP.set_motor_power(BP.PORT_B, 30)
    BP.set_motor_power(BP.PORT_C, -30)
    time.sleep(1)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    time.sleep(.2)
def turnleft():
    print("turning left")
    BP.set_motor_power(BP.PORT_B, -30)
    BP.set_motor_power(BP.PORT_C, 30)
    time.sleep(1)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    time.sleep(.2)
def moveforward():
    print("moving forward")
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 
    while (BP.get_motor_encoder(BP.PORT_B)) > (-641):
        BP.set_motor_power(BP.PORT_B, -30)
        BP.set_motor_power(BP.PORT_C, -30)
        time.sleep(.002)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    
try:
    while True:
        #checking if each hallway is open:
        if grovepi.ultrasonicRead(rightSensor) > 30 and grovepi.ultrasonicRead(rightSensor) < 2000:
            turnright()
            moveforward()
        elif grovepi.ultrasonicRead(frontSensor) > 30 and grovepi.ultrasonicRead(frontSensor) < 2000:
            moveforward()
        elif grovepi.ultrasonicRead(leftSensor) > 30 and grovepi.ultrasonicRead(leftSensor) < 2000:
            turnleft()
            moveforward()
        else:
            turnright()
            turnright()
            moveforward()

except IOError as error:
	print(error)
except TypeError as error:
	print(error)
except KeyboardInterrupt: #Preventing the user from cancelling the execution with CRTL + C . . . for some reason?
	print("You pressed ctrl+C...")