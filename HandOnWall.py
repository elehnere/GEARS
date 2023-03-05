import sys

from simple_pid import PID
import math
import time #import sleep function
import brickpi3
import grovepi #import

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3
pid = PID(5, 0.1, .1, setpoint=50)
ultrasonicRight = 5
BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A))
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))


try:
    while True:
        distance = grovepi.ultrasonicRead(ultrasonicRight)
        control = pid(distance)
        BP.set_motor_power(BP.PORT_B, 50 - control)
        BP.set_motor_power(BP.PORT_C, 50 + control)
        time.sleep(.02)



except IOError as error: #catching and throwing errors
    print(error)
except TypeError as error:
    print(error)
except KeyboardInterrupt: #Notifiying the user when they cancel via crtl c
    print("You pressed ctrl+C...")
BP.reset_all()
sys.exit()



