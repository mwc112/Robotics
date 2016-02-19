#!/usr/bin/python -tt

def sub_misc(x, tup):
    return x - tup[0]

import brickpi
import time
import collections
from os import listdir, mkdir
from os.path import isfile, join
from errno import EEXIST

interface=brickpi.Interface()
motors = [0,1]
angle2 = -14.25
angle = 3.64

zeroOffset = 30 
currentSpeed = [0,0]
port = 2
maxspeed = 20

def usToSpeed(us):
	return min(maxspeed, us/2)

def main():
	interface.initialize()
	setupMotors()
	interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);
	prevReading = 0
	while True:
		usReading = getUSReading()
		if usReading != prevReading:
			print usReading
			prevReading = usReading
		if usReading > 0:
			forwards(maxspeed + 6 - usReading, maxspeed - 6 -usReading)
		elif usReading < 0:
			forwards(maxspeed - 6 +usReading, maxspeed + 6 +usReading)
	stop()
	interface.terminate()

readings = 0
def median(l):
    half = len(l) // 2
    l.sort()
    if not len(l) % 2:
        return (l[half - 1] + l[half]) / 2.0
    return l[half]

def getUSReading():
	global readings
	r = interface.getSensorValue(port)[0] - zeroOffset
	return r 

def left(ang=1):
	interface.increaseMotorAngleReferences(motors,[-ang*angle, ang*angle])
	time.sleep(ang*2)

def right(ang=1):
	interface.increaseMotorAngleReferences(motors, [ang*angle, -ang*angle])
	time.sleep(ang*2)

def forwards(spdl=6, spdr=6):
	spdl = min(spdl, 25)
	spdr = min(spdr, 25)
	global currentSpeed
	if currentSpeed[0] != spdl or currentSpeed[1] != spdr:
		print "speddd"
		interface.setMotorRotationSpeedReferences(motors, [spdl, spdr])
		currentSpeed[0] = spdl
		currentSpeed[1] = spdr
		print currentSpeed
	

def backwards(spd=6):
	interface.setMotorRotationSpeedReferences(motors, [-spd, -spd])

def backwards40(dist=1):
        interface.increaseMotorAngleReferences(motors, [-dist*angle2, -dist*angle2])
        time.sleep(3)

def stop():
	interface.setMotorRotationSpeedReferences(motors, [0, 0])

def setupMotors():

	interface.motorEnable(motors[0])
	interface.motorEnable(motors[1])

	rparams = interface.MotorAngleControllerParameters()
	rparams.maxRotationAcceleration = 15.0
	rparams.maxRotationSpeed = 8.0
	rparams.feedForwardGain = 255/22.2
	rparams.minPWM = 42.0
	rparams.pidParameters.minOutput = -300
	rparams.pidParameters.maxOutput = 300

	lparams = interface.MotorAngleControllerParameters()
	lparams.maxRotationAcceleration = 15.0
	lparams.maxRotationSpeed = 8.0
	lparams.feedForwardGain = 255/22.2
	lparams.minPWM = 42.0
	lparams.pidParameters.minOutput = -300
	lparams.pidParameters.maxOutput = 300

	lk_u = 600 
	rk_u = 600
	lp_u = 0.270
	rp_u = 0.276

	logsFolder = "logs/tuned-l{0},r{1}".format(lk_u, rk_u)

	try:
		mkdir(logsFolder)
	except OSError as e:
		if e.errno != EEXIST:
			raise

	lk_p = 0.6 * lk_u
	rk_p = 0.6 * rk_u

	#2.2
	rparams.pidParameters.k_i = 0 #0.5 * lk_p * lp_u
	rparams.pidParameters.K_d = lk_p * lp_u / 8.0
	rparams.pidParameters.k_p = lk_p


	lparams.pidParameters.k_i = 0 #0.5 * rk_p * rp_u
	lparams.pidParameters.K_d = rk_p * rp_u / 8.0
	lparams.pidParameters.k_p = rk_p

	interface.setMotorAngleControllerParameters(motors[0],lparams)
	interface.setMotorAngleControllerParameters(motors[1],rparams)


main()

