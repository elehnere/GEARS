from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi
import math

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# BP.set_sensor_type configures the BrickPi3 for a specific sensor.
# BP.PORT_1 specifies that the sensor will be on sensor port 1.
# BP.Sensor_TYPE.EV3_GYRO_ABS_DPS specifies that the sensor will be an EV3 gyro sensor.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
currentPosition = [3, 0]
mapArray = [["0", "0", "0", "0", "0", "0"], 
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0"]]
angleMax = 610
hazardList = ["Hazard Type", "Parameter of Interest", "Parameter Value", "Hazard X Coordinate", "Hazard Y Coordinate"]
currentOrientation = 0
kP = -0.5
kI = -0.06
kD = -0.03
dT = 0.02
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

def turn(type):
    global currentOrientation
    sensorData = BP.get_sensor(BP.PORT_1)
    angleVal = sensorData[0]
    print(angleVal)
    initialAngle = (angleVal)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    if type == "r":
        currentOrientation += 1
        while (angleVal) < (initialAngle + 80):
            print(angleVal)
            #print(BP.get_motor_encoder(BP.PORT_B))
            BP.set_motor_power(BP.PORT_B, 30)
            BP.set_motor_power(BP.PORT_C, -30)
            
            sensorData = BP.get_sensor(BP.PORT_1)
            angleVal = sensorData[0]

            time.sleep(0.01)
        type = "STOP"
        
    if type == "l":
        currentOrientation -= 1
        while (angleVal) > (initialAngle - 80):
            print(angleVal)
            #print(BP.get_motor_encoder(BP.PORT_B))
            BP.set_motor_power(BP.PORT_B, -30)
            BP.set_motor_power(BP.PORT_C, 30)
            
            sensorData = BP.get_sensor(BP.PORT_1)
            angleVal = sensorData[0]

            time.sleep(0.01)
        type = "STOP"

def goForward():
    global currentOrientation
    global mapArray
    global currentPosition
    global hazardList
    magCheck = 0
    heatCheck = 0
    BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
    #move forward a certain distance or until it sees a hazard
    #output 1 if no hazard was detected, 0 if a hazard was found
    #note down hazards in both the table and the map
    P = 0
    I = 0
    D = 0
    e_last = 0 
    
    #Read IMU
    #Read IR
    if (not magCheck) and (not heatCheck):
        while ((BP.get_motor_encoder(BP.PORT_B) + BP.get_motor_encoder(BP.PORT_C)) / 2)  > (-1 * angleMax):
            #print("B", BP.get_motor_encoder(BP.PORT_B), "C", BP.get_motor_encoder(BP.PORT_C))
            current_diff = (BP.get_motor_encoder(BP.PORT_B)) - (BP.get_motor_encoder(BP.PORT_C))
            P = kP * current_diff
            I += kI * current_diff * dT / 2
            D = kD * (current_diff - e_last)
            deltaPow = P + I + D
            BP.set_motor_power(BP.PORT_B, -30 + deltaPow)
            BP.set_motor_power(BP.PORT_C, -30 - deltaPow)
            #print(deltaPow, " ", end = '')
            #print("P",P, "I", I, "D", D, end = '')
            e_last = current_diff
            time.sleep(dT)
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)     
    currentPosition[xyFind(currentOrientation)] += signFind(currentOrientation) 
    if magCheck == 1:
        hazardList.append(["MRI", "Field strength (uT)", "N/A", str(40 * currentPosition[0]),  str(40 * currentPosition[1])])
        #note electricomagnetic hazard
        mapArray[currentPosition[1], currentPosition[0]] = 3
        currentPosition[xyFind(currentOrientation)] -= signFind(currentOrientation)
    elif heatCheck == 1:
        hazardList.append(["Cesium-137", "Radiated Power (W)", "N/A", str(40 * currentPosition[0]),  str(40 * currentPosition[1])])
        #note heat hazard
        mapArray[currentPosition[1], currentPosition[0]] = 2
        currentPosition[xyFind(currentOrientation)] -= signFind(currentOrientation)
    else:
        mapArray[currentPosition[1], currentPosition[0]] = 1
        return 1
    return 0



def signFind(orientation):
    signCheck = math.floor((orientation % 4) / 2)
    signCheck *= -2
    signCheck += 1
    return signCheck


def xyFind(orientation):
    xyCheck = (orientation % 2)
    return xyCheck

# global traveledSegmentCount #tracks number of segments traveled in a single run before turning
# traveledSegmentCount = 0 

# def driveSequence():
#     distance = 40 #cm
#     angleRotationMax = (distance - 2.7508) / .0581 #experimentally determined motor encoder value for 40 cm at speed 30

#     while BP.get_motor_encoder(BP.PORT_B) > (-1 * angleRotationMax): #simply uses left motor encoder assuming right is same
#         BP.set_motor_power(BP.PORT_B, -30)
#         BP.set_motor_power(BP.PORT_C, -30)
    
    
# Uses right wall tracking and coordinate math to make decisions    
def detectRight():
    rightDistance2 = grovepi.ultrasonicRead(7) # right sensor on the connecting bar 
    if rightDistance2 > 12:
        return 1    #output 1 if the right side is clear
    if rightDistance2 < 12:
        return 0    #output 0 otherwise
    print(rightDistance2)

def detectFront():
    frontDistance = grovepi.ultrasonicRead(6)
    if frontDistance > 12:
        return 1    #output 1 if the front side is clear
    if frontDistance < 12:
        return 0    #output 0 otherwise
    print(frontDistance)



try:
    while True:
        if (detectRight()):
            turn("r")
            if (goForward() == 0):
                turn("l")
                if detectFront():
                    if (goForward() == 0):
                        turn("l")
                else:
                    turn("l")
        elif detectFront():
            if (goForward() == 0):
                turn("l")
        else:
            turn("l")
            
        # ##### GYRO #####
        # sensorData = BP.get_sensor(BP.PORT_1)
        # angleVal = sensorData[0]
        # #converts negative angle values to positive
        # if angleVal < 0:
        #     angleVal = 360 - (abs(angleVal) % 360)
        # #stops any angle values from exceeding 360 and converts them to a single 2pi range
        # if angleVal >= 360:
        #     angleVal = angleVal % 360
        # print(angleVal)
        # ################

        #mapDirectionsArray.append(getDirection(angleVal))
        #driveSequence()
        #mapDirectionsArray.append(traveledSegmentCount)
        #traveledSegmentCount = 0

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