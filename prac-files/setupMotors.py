def setupMotors(interface, motors):

    interface.motorEnable(motors[0])
    interface.motorEnable(motors[1])

    rparams = createParams(interface)
    lparams = createParams(interface)
    sparams = createParams(interface)

    lk_u = 600
    rk_u = 580
    sk_u = 700
    #lk_u = 910
    #rk_u = 870
    lp_u = 0.270
    rp_u = 0.276
    sp_u = 0.270

    lk_p = 0.6 * lk_u
    rk_p = 0.6 * rk_u
    sk_p = 0.6 * sk_u

    rparams.pidParameters.k_i = 1.65 * lk_p * lp_u
    rparams.pidParameters.K_d = lk_p * lp_u / 8.0
    rparams.pidParameters.k_p = lk_p
    lparams.pidParameters.k_i = 1.7 * rk_p * rp_u
    lparams.pidParameters.K_d = rk_p * rp_u / 8.0
    lparams.pidParameters.k_p = rk_p


    sparams.feedForwardGain = 255/25.0
    sparams.minPWM = 40
    sparams.pidParameters.k_i = 0#1.1 * sk_p * sp_u
    sparams.pidParameters.K_d = sk_p * sp_u / 8.0
    sparams.pidParameters.k_p = sk_p

    interface.setMotorAngleControllerParameters(motors[0],lparams)
    interface.setMotorAngleControllerParameters(motors[1],rparams)
    interface.setMotorAngleControllerParameters(3,sparams)

    interface.motorEnable(3)

def createParams(interface):
    params = interface.MotorAngleControllerParameters()
    params.maxRotationAcceleration = 15.0
    params.maxRotationSpeed = 8.0
    params.feedForwardGain = 255/23.0
    params.minPWM = 42.0
    params.pidParameters.minOutput = -300
    params.pidParameters.maxOutput = 300
    return params

