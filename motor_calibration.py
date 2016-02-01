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

#830
#910

lp = 0.6*830
rp = 0.6*990

rparams = interface.MotorAngleControllerParameters()
rparams.maxRotationAcceleration = 20.0
rparams.maxRotationSpeed = 10.0
rparams.feedForwardGain = 255/20
rparams.minPWM = 30.0
rparams.pidParameters.minOutput = -255
rparams.pidParameters.maxOutput = 255
rparams.pidParameters.k_p = rp

lparams = interface.MotorAngleControllerParameters()
lparams.maxRotationAcceleration = 20.0
lparams.maxRotationSpeed = 10.0
lparams.feedForwardGain = 255/20
lparams.minPWM = 30.0
lparams.pidParameters.minOutput = -255
lparams.pidParameters.maxOutput = 255
lparams.pidParameters.k_p = lp


interface.setMotorAngleControllerParameters(motors[0],lparams)
interface.setMotorAngleControllerParameters(motors[1],rparams)


lparams.pidParameters.k_i = (lp * (1.2/5.0)) / 2.0
lparams.pidParameters.k_d = (lp * (1.2/5.0)) / 8.0
lparams.pidParameters.k_p = lp

rparams.pidParameters.k_i = (rp * (1.2/6.0)) / 2.0
rparams.pidParameters.k_d = (rp * (1.2/6.0)) / 8.0
rparams.pidParameters.k_p = rp

angle = 7

interface.startLogging("./lol.txt")

for i in range(1,10):
    #lparams.pidParameters.k_p = lp
    #rparams.pidParameters.k_p = rp
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
    #lp += 50
    #rp += 10
    print "lol"
    time.sleep(1)

interface.stopLogging

interface.terminate()



