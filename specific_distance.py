import math
import time #import sleep function
import brickpi3
import grovepi #import

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3

ultrasonic_sensor_port = 4 #Set the port the program looks for ultrasonic sensor data from
conversionFactor = 1 /(8.16 * math.pi)
desiredSpeed = -15
degreeLimit = 360 * desiredSpeed * conversionFactor
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 

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
motorSpeed = int(input("Input your motor speed: "))
distance = int(input("Enter your distance (cm): "))
if motorSpeed == 30:
    angleRotationMax = (distance - 2.7508) / .0581
if motorSpeed == 50:
    angleRotationMax = (distance - 5.5655) / .06

try:
    while BP.get_motor_encoder(BP.PORT_B) > (-1 * angleRotationMax):
        print(BP.get_motor_encoder(BP.PORT_B))
        print(angleRotationMax)
        BP.set_motor_power(BP.PORT_B, -30)
        BP.set_motor_power(BP.PORT_C, -30)
                
        time.sleep(.005)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
except IOError as error:
	print(error)
#except TypeError as error:
	#print(error)
except KeyboardInterrupt: #Preventing the user from cancelling the execution with CRTL + C . . . for some reason?
	print("You pressed ctrl+C...")

BP.reset_all() #resets the brick_PI
