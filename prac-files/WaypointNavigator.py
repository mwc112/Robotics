import random
import math
class WaypointNavigator:
    def __init__(self, robot, canvas=None, startX=10, startY=10):
        self.robot = robot;
        self.numberOfParticles = 100
        self.particles = [(startX, startY, 0)] * self.numberOfParticles
        self.canvas = canvas
        self.weights = [1.0/len(self.particles)] * len(self.particles)
        
    def estimatePosition(self):
        sumX = 0
        sumY = 0
        sumT = 0
        for i in range(0, len(self.particles)):
            sumX += self.particles[i][0] * self.weights[i]
            sumY += self.particles[i][1] * self.weights[i]
            sumT += self.particles[i][2] * self.weights[i]
        return (sumX, sumY, sumT)
        
    def updateParticles(self, dist):
        for i in range(0,len(self.particles)):
            randx = random.gauss(0,0.025)
            randy = random.gauss(0,0.025)
            angRand = random.gauss(0,0.05)
            x = self.particles[i][0] + (dist + randx) * math.cos(self.particles[i][2])
            y = self.particles[i][1] + (dist + randy) * math.sin(self.particles[i][2])
            theta = self.particles[i][2] + angRand
            self.particles[i] = (x, y, theta)
        #if not self.canvas is None:
            #self.canvas.drawParticles(self.particles)
        
    def updateParticlesRot(self, ang):
        for i in range(0, len(self.particles)):
            rand = random.gauss(0,0.05)
            theta = self.particles[i][2] + ang + rand
            x = self.particles[i][0]
            y = self.particles[i][1]

            self.particles[i] = (x, y, theta)
        #if not self.canvas is None:
            #self.canvas.drawParticles(self.particles)
        
        
    def navigateToWaypoints(self, wps):
        for wp in wps:
            self.navigateToWaypoint(*wp)
            print self.estimatePosition()

    def navigateToWaypoint(self, X, Y):
        position = self.estimatePosition()
        if not self.canvas is None:
            self.canvas.drawLine((position[0], position[1], X, Y))
        dx = X - position[0]
        print dx
        dy = Y - position[1]
        print dy
        dist = math.sqrt(dx * dx + dy * dy)
        angle = math.atan2(dy, dx)
        dt = angle - position[2]
        self.robot.rotate(dt)
        self.updateParticlesRot(dt)
        self.robot.moveForward(dist)
        self.updateParticles(dist)
        
    
