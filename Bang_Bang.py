#!/usr/bin/env python
#
#
# This code is an example of a Bang-Bang controller.
# 
# Hardware: Connect EV3 or NXT motor(s) to any of the BrickPi3 motor ports.
#

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

try:

    speed = 100 # User can change this value to see how the behavior of the controller changes
    angle_delta = 360 # User can change this value to see how the behavior of the controller changes

    #NOTE: The user should select which port to use here, and comment out the other three.
    USED_PORT = BP.PORT_A
    #USED_PORT = BP.PORT_B
    #USED_PORT = BP.PORT_C
    #USED_PORT = BP.PORT_D
    BP.offset_motor_encoder(USED_PORT, BP.get_motor_encoder(USED_PORT))
    
    while True:
     #   if BP.get_motor_encoder(USED_PORT) < angle_delta:
      #      BP.set_motor_power(USED_PORT, speed)
       # else:
        #    BP.set_motor_power(USED_PORT, -1*speed)
        BP.set_motor_position(USED_PORT, angle_delta)
        time.sleep(0.02) 
    

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
