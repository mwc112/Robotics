#!/usr/bin/python

import matplotlib.pyplot as plt
import csv

from os import listdir
from os.path import isfile, join

path = "logsSleep/"

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
        plt.plot(time, leftRef, 'b',  label="left reference")
        plt.plot(time, leftReal, 'k', label="left real")    
        plt.plot(time, leftErr, 'k', label="left error")    
        plt.axis([0, time[count-1], -5, 21])    
        plt.axhline(0, color='black')
        plt.title(join("left ",log))
        plt.legend(loc=7)
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()
        plt.plot(time, rightRef, 'g',  label="right reference")
        plt.plot(time, rightReal, 'c', label="right real")     
        plt.plot(time, rightErr, 'k', label="right error")    
        plt.axis([0, time[count-1], -5, 21])    
        plt.axhline(0, color='black')
        plt.title(join("right ",log))
        plt.legend(loc=7)
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()
except IOError:
    print "lol"


