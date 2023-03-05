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


try:
    power = -30
    initialTime = time.time_ns()
    while BP.get_motor_encoder(BP.PORT_B) > -608:
        print(BP.get_motor_encoder(BP.PORT_B))
        BP.set_motor_power(BP.PORT_B, power)
        BP.set_motor_power(BP.PORT_C, power)
        time.sleep(.005)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    print(BP.get_motor_encoder(BP.PORT_B))
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
