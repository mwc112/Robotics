#!/usr/bin/env python
from collections import namedtuple
import random
import math
import time
import sys
from Robot import Robot
from WaypointNavigator import WaypointNavigator
from Canvas import Canvas
from SignatureContainer import LocationSignature, SignatureContainer
from PlaceRecognizer import PlaceRecognizer


Point = namedtuple('Point', 'x y')

O = Point(0.0, 0.0)
A = Point(0.0, 168.0)
B = Point(84.0, 168.0)
C = Point(84.0, 126.0)
D = Point(84.0, 210.0)
E = Point(168.0, 210.0)
F = Point(168.0, 84.0)
G = Point(210.0, 84.0)
H = Point(210.0, 0.0)

Wall = namedtuple('Wall', 'A B name')

walls = [ Wall(O, A, 'a'), Wall(A, B, 'b'), Wall(C, D, 'c'), Wall(D, E, 'd'),
            Wall(E, F, 'e'), Wall(F,G, 'f'), Wall(G,H, 'g'), Wall(H,O, 'h')]

def dist_to_wall(x, y, theta, wall):
    try:
        return ((wall.B.y - wall.A.y)*(wall.A.x - x) - (wall.B.x - wall.A.x)*(wall.A.y - y)) / ((wall.B.y - wall.A.y)*math.cos(theta) - (wall.B.x - wall.A.x)*math.sin(theta))
    except:
        return float("inf")

def distance_point(A, B):
    dx = B.x - A.x
    dy = B.y - A.y
    return math.sqrt(dx * dx + dy * dy)

def calculate_likelihood(x, y, theta, z):
    closestWallDistance = -1;
    closestWall = None
    for wall in walls:
        m = abs(dist_to_wall(x, y, theta, wall))
        intersection = Point(x + m * math.cos(theta), y + m * math.sin(theta))
        if distance_point(wall.A, wall.B) == distance_point(wall.A, intersection) + distance_point(wall.B, intersection):
            if closestWallDistance == -1 or m <= closestWallDistance:
                closestWallDistance = m
                closestWall = wall

    likelihood = math.pow(math.e, (-math.pow(z - closestWallDistance, 2))/(2 * 0.005))
    return likelihood

def update_normalise_resample_weights():
    #print navigator.particles
    us_reading = placerec.getReading();
    print us_reading
    if us_reading > 149.0 or us_reading < 7.0:
        return
    for i in range(1, len(navigator.particles)):
        likelihood = calculate_likelihood(navigator.particles[i][0], navigator.particles[i][1], navigator.particles[i][2], us_reading) + 20
        navigator.weights[i] = likelihood * navigator.weights[i]

    sum = 0
    cumulative_weights = [0] * 100
    #print navigator.weights
    for i in range(0,len(navigator.weights)):
        sum = sum + navigator.weights[i]
    for i in range(0, len(navigator.weights)):
        navigator.weights[i] = navigator.weights[i] / sum
    new_particles = [0] * 100
    sum = 0
    for i in range(0,len(navigator.weights)):
        sum = sum + navigator.weights[i]
        cumulative_weights[i] = sum
    for i in range(0,100):
        rand = random.random()
        j = 0
        while rand > cumulative_weights[j]:
            j+=1
        new_particles[i] = navigator.particles[j]
    navigator.particles = new_particles
    navigator.weights = [1/100.0] * 100

def navigate_with_mc(x, y):
    navigator.navigateToWaypoint(x,y)
    if not navigator.canvas is None:
            #print navigator.particles
            navigator.canvas.drawParticles(navigator.particles)
    update_normalise_resample_weights()
    if not navigator.canvas is None:
            navigator.canvas.drawParticles(navigator.particles)


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

def navigate_in_steps(x, y):
    (cx, cy, ct) = navigator.estimatePosition()
    dx = x - cx
    dy = y - cy
    stepX = dx/5.0
    stepY = dy/5.0
    print "stepping to " + str(x) + "," + str(y) + " in: " + str(stepX) + "," + str(stepY)
    for i in range(0,5):
        cx+=stepX
        cy+=stepY
        navigate_with_mc(cx,cy)

robot = Robot()
canvas = None #Canvas()
sigCon = SignatureContainer()
placerec = PlaceRecognizer(robot, sigCon)

#for i in range(6):
#   placerec.learnLocation(i)
#   raw_input("Enter your name: ")



(locidx, rot) = placerec.recognizeLocation()
#(locidx, rot) = (4, 0)

print "current loc" + str(locidx) + " at " + str(rot)  


waypoints = [(84,30), (180,30), (180,54), (138,54), (138,168)]

currentLocation = waypoints[locidx]

navigator = WaypointNavigator(robot, canvas, currentLocation[0], currentLocation[1], rot/180.0 * math.pi)

for i in range(1, 6):
    nextWP = waypoints[(locidx +i)%5]
    navigate_in_steps(nextWP[0], nextWP[1])
    time.sleep(1)


