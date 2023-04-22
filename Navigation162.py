import math as m
import time #import sleep function
import brickpi3 
import grovepi #import 
hazardList = ["Hazard Type", "Parameter of Interest", "Parameter Value", "Hazard X Coordinate", "Hazard Y Coordinate"]
BP = brickpi3.BrickPi3() #Create an instance of BrickPi3
currentPosition = [3, 0]
mapArray =  [["0", "0", "0", "0", "0", "0"], 
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"]]
currentOrientation = 0
frontClose = 100 #When the reading is lower than this value, the bot is too close to a front wall
rightFar = 100 #When the reading is larger than this value, the bot is too far from a right wall (Aka, a right turn is possible)
angleMax = 0
threshold = 0
frontSensorReading = 100 #For example. To Replace.
frontSensorReading = 100 #For example. To Replace.
def detectRight():
    #output 1 if the right side is clear
    #output 0 otherwise
    print("ok")
def detectFront():
    #output 1 if the front side is clear
    #output 0 otherwise
    print("ok")
def turnRight():
    global currentOrientation
    currentOrientation += 1
def turnLeft():
    global currentOrientation
    currentOrientation -= 1
def goForward():
    global currentOrientation
    global mapArray
    global currentPosition
    global hazardList
    magCheck = 0
    heatCheck = 0
    #move forward a certain distance or until it sees a hazard
    #output 1 if no hazard was detected, 0 if a hazard was found
    #note down hazards in both the table and the map
    BP.set_motor_power(BP.PORT_B, -30)
    BP.set_motor_power(BP.PORT_C, -30)
    while (not heatCheck) and (not magCheck) and (BP.get_motor_encoder(BP.PORT_B) < angleMax):
        #Read IR
        #Read IMU
        if grovepi.analog_read(4)[1] > threshold:
            heatCheck = 1
        if IMURead()[3] > threshold:
            magCheck = 1
        time.sleep(.02)
    while (heatCheck or magCheck) and (BP.get_motor_encoder(BP.PORT_B) > 0):
        BP.set_motor_power(BP.PORT_B, 30)
        BP.set_motor_power(BP.PORT_C, 30)
        time.sleep(0.02)
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
    signCheck = m.floor((orientation % 4) / 2)
    signCheck *= -2
    signCheck += 1
    return signCheck
def xyFind(orientation):
    xyCheck = (orientation % 2)
    return xyCheck

while True: #infinite loop 
    if (detectRight()):
        turnRight()
        if (goForward() == 0):
            turnLeft()
            if detectFront():
                if (goForward() == 0):
                    turnLeft()
            else:
                turnLeft()
    elif detectFront():
        if (goForward() == 0):
            turnLeft()
    else:
        turnLeft()
    #Adjust