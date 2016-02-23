import random
import math
class WaypointNavigator:
    def __init__(self, robot, canvas=None):
        self.robot = robot;
        self.numberOfParticles = 100
        self.particles = [(0, 0, 0)] * self.numberOfParticles
        self.canvas = canvas
        
    def estimatePosition(self, weights):
        sumX = 0
        sumY = 0
        sumT = 0
        for i in range(0, len(self.particles)):
            sumX += self.particles[i][0] * weights[i]
            sumY += self.particles[i][1] * weights[i]
            sumT += self.particles[i][2] * weights[i]
        return (sumX, sumY, sumT)
        
    def updateParticles(self, dist):
        for i in range(0,len(self.particles)):
            rand = random.gauss(0,0.05)
            angRand = random.gauss(0,0.05)
            x = self.particles[i][0] + (dist + rand) * math.cos(self.particles[i][2])
            y = self.particles[i][1] + (dist + rand) * math.sin(self.particles[i][2])
            theta = self.particles[i][2] + angRand
            self.particles[i] = (x, y, theta)
        if not self.canvas is None:
            self.canvas.drawParticles(self.particles)
        
    def updateParticlesRot(self, ang):
        for i in range(0, len(self.particles)):
            rand = random.gauss(0,0.05)
            theta = self.particles[i][2] + ang + rand
            x = self.particles[i][0]
            y = self.particles[i][1]

            self.particles[i] = (x, y, theta)
        if not self.canvas is None:
            self.canvas.drawParticles(self.particles)
        
        
    def navigateToWaypoints(self, wps):
        for wp in wps:
            self.navigateToWaypoint(*wp)

    def navigateToWaypoint(self, X, Y):
        weights = [1.0/len(self.particles)] * len(self.particles)
        position = self.estimatePosition(weights)
        if not self.canvas is None:
           self.canvas.drawLine((position[0], position[1], X, Y))
        dx = X - position[0]
        dy = Y - position[1]
        dist = math.sqrt(dx * dx + dy * dy)
        angle = -math.atan2(dy, dx)
        dt = angle - position[2]
        self.robot.rotate(dt)
        self.updateParticlesRot(dt)
        self.robot.moveForward(dist)
        self.updateParticles(dist)
        
    
