#!/usr/bin/env python
import random
from Robot import Robot
from WaypointNavigator import WaypointNavigator
from Canvas import Canvas

def main():
    robot = Robot()
    canvas = Canvas()
    navigator = WaypointNavigator(robot);
    
    while True:
        navigator.navigateToWaypoint(*getWayPoint())


 
    
def getWayPoint():
    inputStr = raw_input("Enter waypoint as 'x,y' in meters:")
    if inputStr == 'q':
        exit()
    try:
        x = float(inputStr.split(",")[0]) * 100
        y = float(inputStr.split(",")[1]) * 100
    except:
        print("Please enter valid coordinates as numbers in the format x,y or type q to quit")
        return getWayPoint()
    return (x,y)
    

main() 

