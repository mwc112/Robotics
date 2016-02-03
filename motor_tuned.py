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
rparams.maxRotationAcceleration = 20.0
rparams.maxRotationSpeed = 10.0
rparams.feedForwardGain = 255/20
rparams.minPWM = 38.0
rparams.pidParameters.minOutput = -255
rparams.pidParameters.maxOutput = 255

lparams = interface.MotorAngleControllerParameters()
lparams.maxRotationAcceleration = 20.0
lparams.maxRotationSpeed = 10.0
lparams.feedForwardGain = 255/20
lparams.minPWM = 38.0
lparams.pidParameters.minOutput = -255
lparams.pidParameters.maxOutput = 255


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

lparams.pidParameters.k_i = 0.5 * lk_p * lp_u
lparams.pidParameters.k_d = lk_p * lp_u / 8.0 
lparams.pidParameters.k_p = lk_p

rparams.pidParameters.k_i = 0.5 * rk_p * rp_u
rparams.pidParameters.k_d = rk_p * rp_u /8.0
rparams.pidParameters.k_p = rk_p

#angle2 = -14.75
angle2 = -7.125
angle = 3.63
interface.setMotorAngleControllerParameters(motors[0],lparams)
interface.setMotorAngleControllerParameters(motors[1],rparams)

for i in range(0,16):
	interface.increaseMotorAngleReferences(motors,[angle2,angle2])
	while not interface.motorAngleReferencesReached(motors):
		pass
	interface.increaseMotorAngleReferences(motors,[angle, -angle])
	while not interface.motorAngleReferencesReached(motors):
		pass
	#interface.increaseMotorAngleReferences(motors,[angle2,angle2])
	#while not interface.motorAngleReferencesReached(motors):
	#	pass
        
	


#interface.startLogging(join(logsFolder,"tunedl{0}r{1}.txt".format(lk_u,rk_u)))
#interface.increaseMotorAngleReferences(motors,[angle,-angle])
#targetAngles = interface.getMotorAngleReferences(motors)
time.sleep(7)
#interface.stopLogging()

interface.terminate()

