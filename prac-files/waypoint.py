#!/usr/bin/env python

import random
from Robot import Robot
from WaypointNavigator import WaypointNavigator
from Canvas import Canvas

def main():
    robot = Robot()
    canvas = Canvas()
    navigator = WaypointNavigator(robot, canvas);
    
    navigator.navigateToWaypoints([(10,0), (20,0), (30,0), (40,0), (40,10),(40,20),(40,30), (40,40), (30,40), (20,40),(10,40),(0,40), (0,30), (0,20), (0,10), (0,0)])


main() 

