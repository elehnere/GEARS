#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for reading an EV3 gyro sensor connected to PORT_1 of the BrickPi3
#
# Hardware: Connect an EV3 gyro sensor to BrickPi3 sensor port 1.
#
# Results:  When you run this program, the gyro's absolute rotation and rate of rotation will be printed.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import math as m

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# Configure for an EV3 color sensor.
# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.Sensor_TYPE.EV3_GYRO_ABS_DPS specifies that the sensor will be an EV3 gyro sensor.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

time.sleep(4)
##### GYRO #####
#sensorData = BP.get_sensor(BP.PORT_1) #inserted below
#angleVal = sensorData[0] inserted below
#converts negative angle values to positive
#if angleVal < 0:
    #angleVal = 360 - (abs(angleVal) % 360)
#stops any angle values from exceeding 360 and converts them to a single 2pi range
#if angleVal >= 360:
    #angleVal = angleVal % 360
#print(angleVal) #inserted below
################
#initialAngle = abs(angleVal) #inserted below

try:
    while True:
        sensorData = BP.get_sensor(BP.PORT_1)
        angleVal = sensorData[0]
        print(angleVal)
        initialAngle = abs(angleVal)
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)
        type = input("Right (r) or left (l)? ")
        if type == "r":
            while (angleVal) < (initialAngle + 90):
                print(angleVal)
                #print(BP.get_motor_encoder(BP.PORT_B))
                BP.set_motor_power(BP.PORT_B, 30)
                BP.set_motor_power(BP.PORT_C, -30)
                
                sensorData = BP.get_sensor(BP.PORT_1)
                angleVal = sensorData[0]

                time.sleep(0.01)
            type = "STOP"
        if type == "l":
            while (angleVal) > (initialAngle - 90):
                print(angleVal)
                #print(BP.get_motor_encoder(BP.PORT_B))
                BP.set_motor_power(BP.PORT_B, -30)
                BP.set_motor_power(BP.PORT_C, 30)
                
                sensorData = BP.get_sensor(BP.PORT_1)
                angleVal = sensorData[0]

                time.sleep(0.01)
            type = "STOP"

        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)

        time.sleep(1)
        sensorData = BP.get_sensor(BP.PORT_1)
        angleVal = sensorData[0]
        print(f'FINAL ANGLE AFTER STOPPING: {angleVal}')
        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load.

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
