#!/usr/bin/python -tt

def sub_misc(x, tup):
    return x - tup[0]

import brickpi
import time
from os import listdir, mkdir
from os.path import isfile, join
from errno import EEXIST
import inspect

interface=brickpi.Interface()
interface.initialize()

lparams = interface.MotorAngleControllerParameters()
lparams.pidParameters.lfoflfo = 4;
print [name for (name, value) in inspect.getmembers(lparams.pidParameters)]
