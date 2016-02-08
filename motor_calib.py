#!/usr/bin/python -tt

def sub_misc(x, tup):
    return x - tup[0]

import brickpi
import time
from os import listdir, mkdir
from os.path import isfile, join
from errno import EEXIST

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

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

dir(rparams)

lk_u = 870 
rk_u = 920
lp_u = 0.270
rp_u = 0.276

#lk_u = 830;
#rk_u = 990;
#lp_u = 1.2/5.0;
#rp_u = 1.2/6.0;  

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

#2.15
lparams.pidParameters.k_i = 1.15 * rk_p * rp_u
lparams.pidParameters.K_d = rk_p * rp_u / 8.0
lparams.pidParameters.k_p = rk_p

#angle2 = -14.75
angle2 = -14.25
#0.6
angle = 3.64
#angle = 3.725
#0.55
#angle = 3.78
interface.setMotorAngleControllerParameters(motors[0],lparams)
interface.setMotorAngleControllerParameters(motors[1],rparams)


def Left90deg():
	interface.increaseMotorAngleReferences(motors,[-angle, angle])
	time.sleep(2)

def Right90deg():
	interface.increaseMotorAngleReferences(motors, [angle, -angle])
	time.sleep(2)

def forwards40():
	interface.increaseMotorAngleReferences(motors, [angle2, angle2])
	time.sleep(3)

def backwards40():
	interface.increaseMotorAngleReferences(motors, [-angle2, -angle2])
	time.sleep(3)

Left90deg()
Right90deg()

forwards40()
backwards40()

interface.terminate()

