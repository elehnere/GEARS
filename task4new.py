import math
import time #import sleep function
import brickpi3
import grovepi #import

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3

ultrasonic_sensor_port = 4 #Set the port the program looks for ultrasonic sensor data from
conversionFactor = 1 /(8.16 * math.pi)
desiredSpeed = -15
degreeLimit = 360 * desiredSpeed * conversionFactor

def turnright():
    print("turning right")
    time.sleep(1) # gives a little offset to get around wall
    BP.set_motor_power(BP.PORT_B, 30)
    BP.set_motor_power(BP.PORT_C, -30)
    time.sleep(1)

def turnleft():
    print("turning left")
    time.sleep(1) # gives a little offset to get around wall
    BP.set_motor_power(BP.PORT_B, -30)
    BP.set_motor_power(BP.PORT_C, 30)
    time.sleep(1)
    
try:
    while True:
        BP.set_motor_power(BP.PORT_B, -30)
        BP.set_motor_power(BP.PORT_C, -30)

        userInput = input("Type r for right and l for left: ")
        if userInput == "r":
            turnright()
            
        if userInput == "l":
            turnleft()
            
        #print(BP.get_motor_encoder(BP.PORT_B))
        time.sleep(.005)
except IOError as error:
	print(error)
#except TypeError as error:
	#print(error)
except KeyboardInterrupt: #Preventing the user from cancelling the execution with CRTL + C . . . for some reason?
	print("You pressed ctrl+C...")

BP.reset_all() #resets the brick_PI
