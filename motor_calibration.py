#!/usr/bin/python -tt

def sub_misc(x, tup):
    return x - tup[0]

import brickpi
import time
from os import listdir
from os.path import isfile

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

rparams = interface.MotorAngleControllerParameters()
rparams.maxRotationAcceleration = 20.0
rparams.maxRotationSpeed = 10.0
rparams.feedForwardGain = 255/20
rparams.minPWM = 2.0
rparams.pidParameters.minOutput = -255
rparams.pidParameters.maxOutput = 255

lparams = interface.MotorAngleControllerParameters()
lparams.maxRotationAcceleration = 20.0
lparams.maxRotationSpeed = 10.0
lparams.feedForwardGain = 255/20
lparams.minPWM = 2.0
lparams.pidParameters.minOutput = -255
lparams.pidParameters.maxOutput = 255


lp = 810
rp = 770


lparams.pidParameters.k_i = 0
lparams.pidParameters.k_d = 0
lparams.pidParameters.k_p = lp

rparams.pidParameters.k_i = 0 
rparams.pidParameters.k_d = 0
rparams.pidParameters.k_p = rp

angle = -55
interface.setMotorAngleControllerParameters(motors[0],lparams)
interface.setMotorAngleControllerParameters(motors[1],rparams)


for i in range(1,12):
    if (not isfile("logs/k_p{0}-{1}.txt".format(lp,rp))):
         interface.startLogging("logs/k_p{0}-{1}.txt".format(lp,rp))
         interface.increaseMotorAngleReferences(motors,[angle,angle])
         targetAngles = interface.getMotorAngleReferences(motors)
         time.sleep(3.5)
         interface.stopLogging()
         raw_input("Done lp:{0} rp:{1}".format(lp,rp))
    else:
         print "skipping {0},{1}".format(lp,rp)
    lp += 2
    rp += 2
    lparams.pidParameters.k_p = lp
    rparams.pidParameters.k_p = rp
    interface.setMotorAngleControllerParameters(motors[0], lparams)
    interface.setMotorAngleControllerParameters(motors[1], rparams)

interface.terminate()


    #while not interface.motorAngleReferencesReached(motors) :
    #    motorAngles = interface.getMotorAngles(motors)
    #    err = map(sub_misc, targetAngles, motorAngles) 
    #    if motorAngles :
    #        print "Error: ", err[0], ", ", err[1]
    #    time.sleep(0.1)

