#!/usr/bin/env python

import random
import math
import brickpi
from setupMotors import setupMotors


numberOfParticles = 100
particles = [(0, 0, 0)] * numberOfParticles
motors = [0,1]
interface=brickpi.Interface()
interface.initialize()

def main():
	setupMotors(interface, motors)

	while True:
		navigateToWaypoint(*getWayPoint())


def drawParticles():
    #comment this out for interactive mode
    #print "drawParticles:" + str([(200 + 2*x, 200 + 2*y, theta) for (x, y, theta) in particles])
    pass
    
def updateParticles(dist):
    for i in range(0,len(particles)):
        rand = random.gauss(0,0.05)
        angRand = random.gauss(0,0.05)
        x = particles[i][0] + (dist + rand) * math.cos(particles[i][2])
        y = particles[i][1] + (dist + rand) * math.sin(particles[i][2])
        theta = particles[i][2] + angRand
        particles[i] = (x, y, theta)
    drawParticles()
        
def estimatePosition(particles, weights):
    sumX = 0
    sumY = 0
    sumT = 0
    for i in range(0, len(particles)):
        sumX += particles[i][0] * weights[i]
        sumY += particles[i][1] * weights[i]
        sumT += particles[i][2] * weights[i]
    return (sumX, sumY, sumT)

def navigateToWaypoint(X, Y):
    weights = [1.0/len(particles)] * len(particles)
    position = estimatePosition(particles, weights)
    dx = X - position[0]
    dy = Y - position[1]
    dist = math.sqrt(dx * dx + dy * dy)
    angle = -math.atan2(dy, dx)
    dt = angle - position[2]
    rotate(dt)
    moveForward(dist)
    
        
def updateParticlesRot(ang):
    for i in range(0, len(particles)):
        rand = random.gauss(0,0.05)
        theta = particles[i][2] + ang + rand
        x = particles[i][0]
        y = particles[i][1]

        particles[i] = (x, y, theta)
    drawParticles()
        
        
def moveForward(dist):
    angle = 0.35625
    angle = dist*angle
    interface.increaseMotorAngleReferences(motors,[angle,angle])
    while not interface.motorAngleReferencesReached(motors):
        pass
    updateParticles(dist)
    
#def rotate(ang=math.pi/2):
#    angle = ((3.64+0.17)/(math.pi/2)) * ang
#    interface.increaseMotorAngleReferences(motors,[angle,-angle])
#    while not interface.motorAngleReferencesReached(motors):
#        pass
#    updateParticlesRot(ang)

def rotate(ang=math.pi/2):
    if ang > math.pi:
        ang = - (2*math.pi - ang)
    if ang < -math.pi:
        ang = (2*math.pi + ang)
    print (ang / math.pi * 180)
    angle = ((3.64+0.17)/(math.pi/2)) * ang
    interface.increaseMotorAngleReferences(motors,[angle,-angle])
    while not interface.motorAngleReferencesReached(motors):
        pass
    updateParticlesRot(ang)

 
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

interface.terminate()
