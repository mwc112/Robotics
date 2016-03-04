#!/usr/bin/env python
from collections import namedtuple
import random
import math
from Robot import Robot
from WaypointNavigator import WaypointNavigator
from Canvas import Canvas

robot = Robot()
canvas = Canvas()
navigator = WaypointNavigator(robot, canvas, 84, 30)

    

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
    us_reading = robot.get_us_reading()[0]
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


navigate_with_mc(104, 30)
navigate_with_mc(124, 30)
navigate_with_mc(144, 30)
navigate_with_mc(164, 30)
navigate_with_mc(180, 30)
navigate_with_mc(180,50)
navigate_with_mc(180, 54)
navigate_with_mc(160, 54)
navigate_with_mc(138, 54)
navigate_with_mc(138, 74)
navigate_with_mc(138, 94)
navigate_with_mc(138, 114)
navigate_with_mc(138, 134)
navigate_with_mc(138, 154)
navigate_with_mc(138, 168)
navigate_with_mc(114, 168)
navigate_with_mc(114, 148)
navigate_with_mc(114, 128)
navigate_with_mc(114, 108)
navigate_with_mc(114, 84)
navigate_with_mc(94, 84)
navigate_with_mc(84, 64)
navigate_with_mc(84, 44)
navigate_with_mc(84, 30)
navigate_with_mc(84, 30)
navigate_with_mc(84, 30)
navigate_with_mc(84, 30)
navigate_with_mc(84, 30)
navigate_with_mc(84, 30)


#while True:
#    (x,y) = getWayPoint()
#    navigate_with_mc(x,y)
