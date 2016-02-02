#!/usr/bin/python

import csv

from scipy.optimize import curve_fit
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import numpy as np

# create the function we want to fit
def my_sin(x, freq, amplitude, phase, offset):
        return np.sin(x * freq + phase) * amplitude + offset

path = "../logsF2/"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

try:
    for log in onlyfiles:
        time = []
        leftRef = []
        leftReal = []
        rightRef = []
        rightReal = []
        leftErr = []
        rightErr = []
        count = 0
        tsv = open(join(path,log)) 
        tsvin = csv.reader(tsv, delimiter='\t')
        leftMin = 0
        rightMin = 0
        for row in tsvin:
            time.append(float(row[0]))
            leftRef.append(float(row[1]) * -1 -  leftMin)
            leftReal.append(float(row[2]) * -1 - leftMin)
            rightRef.append(float(row[3]) * -1 - rightMin)
            rightReal.append(float(row[4]) * -1 -rightMin)
            if count == 0:
                leftMin = leftRef[0]
                leftRef[0] = 0
                leftReal[0]= 0
                rightMin = rightRef[0]
                rightRef[0] = 0
                rightReal[0] = 0
            leftErr.append((leftReal[count]-leftRef[count])*10)
            rightErr.append((rightReal[count]-rightRef[count]) * 10)
            if count > 10:
                if leftRef[count] == leftRef[count-5] and rightRef[count] == rightRef[count-5]:
                    break;
            count +=1
        tsv.close()
        
#        N = count + 1 # number of data points
#        t = np.linspace(0, 15*np.pi, N)
#        guess_freq = 1
#        guess_amplitude = 10*np.std(leftErr)/(2**0.5)
#        guess_phase = 0
#        guess_offset = np.mean(leftErr)        
#     
#        p0=[guess_freq, guess_amplitude,
#                    guess_phase, guess_offset]
#     
#        # now do the fit
#        fit = curve_fit(my_sin, t, leftErr, p0=p0)
#        data_fit = my_sin(t, *fit[0])

        plt.clf()
        plt.plot(time, leftRef, 'b',  label="left reference")
        plt.plot(time, leftReal, 'k', label="left real")    
        plt.plot(time, leftErr, 'k', label="left error")    
        plt.axis([time[0], time[count-1], -5, 21])    
        plt.axhline(0, color='black')
        plt.axhline(min(leftErr), color='green')
        plt.axhline(max(leftErr), color='green')
        plt.axhline(np.mean(leftErr), color='green')
        plt.title(join("left ",log))
        plt.legend(loc=7)
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        
        plt.savefig(join(path,"log","left" + log[:-4] + ".png"))
        plt.clf()
        plt.plot(time, rightRef, 'g',  label="right reference")
        plt.plot(time, rightReal, 'c', label="right real")     
        plt.plot(time, rightErr, 'k', label="right error")    
        plt.axis([time[0], time[count-1], -5, 21])    
        plt.axhline(0, color='black')
        plt.title(join("right ",log))
        plt.legend(loc=7)
        plt.axhline(min(rightErr), color='green')
        plt.axhline(max(rightErr), color='green')
        plt.axhline(np.mean(rightErr), color='green')
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.savefig(join(path,"log","right" + log[:-4] + ".png"))
except IOError:
    print "IO"


