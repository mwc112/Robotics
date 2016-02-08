#!/usr/bin/python -tt

import brickpi
import time
import sys
interface=brickpi.Interface()
interface.initialize()

port = int(sys.argv[1]) # port which ultrasoic sensor is plugged in to

interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);

while True:
	usReading = interface.getSensorValue(port)

	if usReading :
		print usReading
	else:
		print "Failed US reading"

	time.sleep(0.05)

interface.terminate()
