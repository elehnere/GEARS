import math as m
import time #import sleep function
import brickpi3 
import grovepi #import 

BP = brickpi3.BrickPi3() #Create an instance of BrickPi3
currentPosition = [0, 0]
mapArray =  [["0", "0", "0", "0", "0", "0"], 
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0", "0"]]
currentOrientation = 0
frontClose = 100 #When the reading is lower than this value, the bot is too close to a front wall
rightFar = 100 #When the reading is larger than this value, the bot is too far from a right wall (Aka, a right turn is possible)

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
    #move forward a certain distance or until it sees a hazard
    #output 1 if no hazard was detected, 0 if a hazard was found
    #note down hazards in both the table and the map
    currentPosition[1] += 1
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
