import math
import time
import brickpi
from setupMotors import setupMotors

class Robot:
    def __init__(self):
        self.motors = [0,1]
	self.sensorPos = 0.0;
        self.interface = brickpi.Interface()
        self.interface.initialize()
        setupMotors(self.interface, self.motors)
        self.interface.sensorEnable(2, brickpi.SensorType.SENSOR_ULTRASONIC);

    def moveForward(self, dist):
        angle = 0.35625/94.0 * 100.0
        angle = dist*angle
        self.interface.increaseMotorAngleReferences(self.motors,[angle,angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            pass
        
    def rotate(self, ang=math.pi/2):
        ang = -ang
        if ang > math.pi:
            ang = ang-(math.pi*2)
        if ang < -math.pi:
            ang = ang+(math.pi*2)
        print (ang / math.pi * 180)
        angle = ((3.64+0.21)/(math.pi/2)) * ang
        self.interface.increaseMotorAngleReferences(self.motors,[angle,-angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            pass
        

    def rotateUSTo(self, angDeg):
        angDeg = angDeg % 360
        angRad = angDeg / 180.0 * math.pi
        ang = angRad - self.sensorPos
	self.interface.increaseMotorAngleReference(3, ang)
        self.sensorPos += ang
        while not self.interface.motorAngleReferenceReached(3):
            pass

    def __del__(self):
        self.interface.terminate()

    def get_us_reading(self):
        return self.interface.getSensorValue(2)
