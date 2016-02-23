import math
import brickpi
from setupMotors import setupMotors

class Robot:
    def __init__(self):
        self.motors = [0,1]
        self.interface = brickpi.Interface()
        self.interface.initialize()
        setupMotors(self.interface, self.motors)

    def moveForward(self, dist):
        angle = 0.35625
        angle = dist*angle
        self.interface.increaseMotorAngleReferences(self.motors,[angle,angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            pass
        
    def rotate(self, ang=math.pi/2):
        if ang > math.pi:
            ang = - (2*math.pi - ang)
        if ang < -math.pi:
            ang = (2*math.pi + ang)
        print (ang / math.pi * 180)
        angle = ((3.64+0.17)/(math.pi/2)) * ang
        self.interface.increaseMotorAngleReferences(self.motors,[angle,-angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            pass
        
    def __del__(self):
        self.interface.terminate()
