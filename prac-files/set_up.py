import brickpi

def public set_up_motors(interface, motors):

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

    lk_p = 0.6 * lk_u
    rk_p = 0.6 * rk_u

    rparams.pidParameters.k_i = 1.1 * lk_p * lp_u
    rparams.pidParameters.K_d = lk_p * lp_u / 8.0
    rparams.pidParameters.k_p = lk_p
    lparams.pidParameters.k_i = 1.15 * rk_p * rp_u
    lparams.pidParameters.K_d = rk_p * rp_u / 8.0
    lparams.pidParameters.k_p = rk_p
    
    interface.setMotorAngleControllerParameters(motors[0],lparams)
    interface.setMotorAngleControllerParameters(motors[1],rparams)