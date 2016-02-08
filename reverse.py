#!/usr/bin/python -tt

def sub_misc(x, tup):
    return x - tup[0]

import brickpi
import time
from os import listdir, mkdir
from os.path import isfile, join
from errno import EEXIST

interface=brickpi.Interface()
motors = [0,1]
angle2 = -14.25
angle = 3.64

def main():
	interface.initialize()
	setupMotors()
	touch_right = 3
	touch_left = 2 
	 
	interface.sensorEnable(touch_right, brickpi.SensorType.SENSOR_TOUCH)
	interface.sensorEnable(touch_left, brickpi.SensorType.SENSOR_TOUCH)
	backwards()
	while True:
		pass
	interface.terminate()

def left(ang=1):
	interface.increaseMotorAngleReferences(motors,[-ang*angle, ang*angle])
	time.sleep(ang*2)

def right(ang=1):
	interface.increaseMotorAngleReferences(motors, [ang*angle, -ang*angle])
	time.sleep(ang*2)

def forwards(spd=6):
	interface.setMotorRotationSpeedReferences(motors, [spd, spd])

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

	lk_u = 870 
	rk_u = 920
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
	rparams.pidParameters.k_i = 1.1 * lk_p * lp_u
	rparams.pidParameters.K_d = lk_p * lp_u / 8.0
	rparams.pidParameters.k_p = lk_p


	lparams.pidParameters.k_i = 1.15 * rk_p * rp_u
	lparams.pidParameters.K_d = rk_p * rp_u / 8.0
	lparams.pidParameters.k_p = rk_p

	interface.setMotorAngleControllerParameters(motors[0],lparams)
	interface.setMotorAngleControllerParameters(motors[1],rparams)


main()

