#!/usr/bin/env python
from collections import namedtuple
import random
import math
from Robot import Robot
from WaypointNavigator import WaypointNavigator
from Canvas import Canvas

def main():
    robot = Robot()
    canvas = Canvas()
    navigator = WaypointNavigator(robot, canvas);
    

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
           
            
    print closestWall.name
        
#main() 

