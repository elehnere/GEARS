 # Program provides feedback control based on motor encoder readings
# Developed for in class activity
# ENGR 162, Spring 2018

import time #import sleep function
import brickpi3 
import grovepi #import 
from MPU9250 import MPU9250

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
myIMU = MPU9250() # create an instance of the IMU sensor
IMUPort = 3


# initialization
# Tuning parameters
KP = 0.001 # proportional control gain
KI = 0.0001 # integral control gain
KD = 0.005 # derivative control gain

dT = 0.02 # time step

target_pos = 0

current_pos = [0,0]

P = 0
I = 0
D = 0
e_prev = [0, 0]

motors = [BP.PORT_A, BP.PORT_D]

# --------------------------------
# Hardware initialization
# --------------------------------
BP.offset_motor_encoder(motors[0], BP.get_motor_encoder(motors[0]) )
BP.offset_motor_encoder(motors[1], BP.get_motor_encoder(motors[1]) )


BP.set_motor_limits(motors[0], power=50, dps=200)
BP.set_motor_limits(motors[1], power=50, dps=200)
# --------------------------------
# ---------------------------------------------------------
# Control loop -- run infinitely until a keyboard interrupt
# ---------------------------------------------------------
try:
    while True:
        # get current position
        current_pos = myIMU.readAccel(IMUPort)
        #print("current position: " + str(current_pos) )
        for axis in range(2):
            e = target_pos - current_pos[axis] # error

            # set up P,I,D, terms for control inputs
            P = KP * e
            I += KI * e * dT/2
            D = KD * (e - e_prev[axis])/ dT
            #print("D" + str(D))


            # control input for motor
            power_in = P + I + D
            BP.set_motor_power(motors[axis], power_in)
            # save error for this step; needed for D term of PID control
            e_prev[axis] = e
            print("error is", e_prev)
            time.sleep(dT)

# ---------------------------------------------------------------------
# If a problem occurse with the while or an interrupt from the keyboard
# ---------------------------------------------------------------------
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print("C")
    BP.reset_all()  
