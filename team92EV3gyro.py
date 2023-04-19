from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.Sensor_TYPE.EV3_GYRO_ABS_DPS specifies that the sensor will be an EV3 gyro sensor.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

startPointX = int(input("What is your starting x coordinate? "))
startPointY = int(input("What is your starting y coordinate? "))
mapArray = [["0", "0", "0", "0", "0", "0"], 
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"]]


startAngle = BP.get_sensor(BP.PORT_1)[1]

direction = "north" #initializes a compass direction variable relative to starting point
def getDirection(a):
    if (350 <= abs(a - startAngle)) or (abs(a - startAngle) <= 10):
        direction = "north"
    if (80 <= abs(a - startAngle)) and (abs(a - startAngle) <= 100):
        direction = "west"
    if (170 <= abs(a - startAngle)) and (abs(a - startAngle) <= 190):
        direction = "south"
    if (260 <= abs(a - startAngle)) and (abs(a - startAngle) <= 280):
        direction = "east"
    return direction

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

global traveledSegmentCount #tracks number of segments traveled in a single run before turning
traveledSegmentCount = 0 

def driveSequence():
    distance = 40 #cm
    angleRotationMax = (distance - 2.7508) / .0581 #experimentally determined motor encoder value for 40 cm at speed 30

    while BP.get_motor_encoder(BP.PORT_B) > (-1 * angleRotationMax): #simply uses left motor encoder assuming right is same
        BP.set_motor_power(BP.PORT_B, -30)
        BP.set_motor_power(BP.PORT_C, -30)

    rightDistance1 = grovepi.ultrasonicRead(rightSensor1)
    rightDistance2 = grovepi.ultrasonicRead(rightSensor2)       
    frontDistance = grovepi.ultrasonicRead(frontSensor)
    
    rightAvg = (rightDistance1 + rightDistance2) / 2
    
    # Uses right wall tracking and coordinate math to make decisions
    
    # Case 1 & 6: If walls on right and front is open, go straight
    if rightAvg < 12 and frontDistance > 12:
        #go straight
        #updatePosition(straight)
        
    # Case 2 & 4: If walls on front and right (possibly dead end), turn left
    if rightAvg < 12 and frontDistance < 12:
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)
        turnLeft()
        
    # Case 3 & 7: If walls on front and right is open, turn right (must 
    #   turn right even if option to go left since robot doesn't know)
    if rightAvg > 12 and frontDistance < 12:
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)
        turnRight()
        
    # Case 5: If front and right is open, check if at the end, if not do math
    if rightAvg > 12 and frontDistance > 12:
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)
        turnLeft() # Turn left to check left side using front sensor
        if rightAvg > 12 and frontDistance > 12:
            # Robot has reached the end
            print("Deposit cargo")
        else:
            print("Do math")

    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    traveledSegmentCount = traveledSegmentCount + 1

mapDirectionsArray = []

try:
    while True:
        ##### GYRO #####
        sensorData = BP.get_sensor(BP.PORT_1)
        angleVal = sensorData[0]
        #converts negative angle values to positive
        if angleVal < 0:
            angleVal = 360 - (abs(angleVal) % 360)
        #stops any angle values from exceeding 360 and converts them to a single 2pi range
        if angleVal >= 360:
            angleVal = angleVal % 360
        print(angleVal)
        ################

        mapDirectionsArray.append(getDirection(angleVal))
        driveSequence()
        mapDirectionsArray.append(traveledSegmentCount)
        traveledSegmentCount = 0

        time.sleep(0.02)  # delay for 0.02 seconds (20ms) to reduce the Raspberry Pi CPU load. 


except brickpi3.SensorError as error:
    print(error)
except Exception as e:
    print ("Error:{}".format(e))
except IOError as error:
    print(error)
except TypeError as error:
    print(error)
        
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
