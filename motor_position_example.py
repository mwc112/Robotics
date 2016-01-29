#!/usr/bin/python -tt

def sub_misc(x, tup):
    return x - tup[0]

import brickpi
import time

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])



lp = 869
rp = 897

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 30.0
motorParams.maxRotationSpeed = 10.0
motorParams.feedForwardGain = 255/11
motorParams.minPWM = 2.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_i = 0
motorParams.pidParameters.k_d = 0
motorParams.pidParameters.k_p = lp

interface.setMotorAngleControllerParameters(motors[0],motorParams)
motorParams.pidParameters.k_p = rp
interface.setMotorAngleControllerParameters(motors[1],motorParams)


lparams = motorParams
rparams = motorParams

angle = 30

interface.startLogging("./lol.txt")

for i in range(0,1):
    lparams.pidParameters.k_p = 0.8*lp
    rparams.pidParameters.k_p = 0.8*rp
    lparams.pidParameters.k_i = (2*0.6*lp)/(5)
    rparams.pidParameters.k_i = (2*0.6*rp)/(5)
    lparams.pidParameters.k_d = ((0.6*lp)*5)/8
    rparams.pidParameters.k_d = ((0.6*rp)*5)/8
    interface.setMotorAngleControllerParameters(motors[0], lparams)
    interface.setMotorAngleControllerParameters(motors[1], rparams)
    interface.increaseMotorAngleReferences(motors,[angle,angle])
    targetAngles = interface.getMotorAngleReferences(motors)
    while not interface.motorAngleReferencesReached(motors) :
        motorAngles = interface.getMotorAngles(motors)
        err = map(sub_misc, targetAngles, motorAngles) 
        if motorAngles :
            print "Error: ", err[0], ", ", err[1]
        time.sleep(0.1)
    #lp += 1
    #rp += 1
    print "lol"
    time.sleep(1)

interface.stopLogging

interface.terminate()



