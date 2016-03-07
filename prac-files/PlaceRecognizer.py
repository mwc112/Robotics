import random
import math
import time
import sys
from SignatureContainer import LocationSignature, SignatureContainer

class PlaceRecognizer:
    def __init__(self, robot, signatures):
        self.robot = robot;
        self.signatures = signatures

    def getReading(self):
        max = 40
        readings = [0] * max
        for i in range(0,max):
            readings[i] = self.robot.get_us_reading()[0]
        return sum(readings)/len(readings)

    def characterizeLocation(self, ls):
        for i in range(len(ls.sig)):
            self.robot.rotateUSTo(i)
            ls.sig[i] = self.getReading()
        self.robot.rotateUSTo(0)

    def learnLocation(self, idx):
        ls = LocationSignature(360)
        self.characterizeLocation(ls)
        self.signatures.save(ls, idx)


    def recognizeLocation(self):
        ls_obs = LocationSignature()
        self.characterizeLocation(ls_obs)

        minsqdiff = sys.maxint
        minreadsig = -1
        minsqindex = -1
        for idx in range(self.signatures.size):
            ls_read = self.signatures.read(idx)
            for i in range(len(ls_read.sig)):
                diff = abs(ls_read.sig[i] - ls_obs.sig[i])
#                print "read: " + str(ls_read.sig[i]) + " obs: " + str(ls_obs.sig[i]) + " diff: " + str(diff)
            obs_hist = self.countDepths(ls_obs.sig)
            read_hist = self.countDepths(ls_read.sig)
            sqdiff = self.squaredDiff(obs_hist, read_hist)
            if sqdiff < minsqdiff:
                minsqdiff = sqdiff
                minsqindex = idx
                minreadsig = ls_read
            #for i in range(len(obs_hist)):
            #    print "i "+str(i) +" obs: " + str(obs_hist[i]) + " read: " + str(read_hist[i])
        rot = self.findRotation(minreadsig.sig, ls_obs.sig)
        return (minsqindex, rot)

    def countDepths(self,arr):
        d = [0] * 256
        for idx in arr:
            d[idx] += 1
        return d

    def squaredDiff(self, arr1, arr2):
        sum = 0
        for i in range(len(arr1)):
            sum += pow(arr1[i] - arr2[i], 2)
        return sum

    def findRotation(self, obs, saved):
        saved.extend(saved)
        minsum = sys.maxint
        minidx = 0;
        for j in range(len(obs)):
            sum = 0
            for i in range(len(obs)):
                sum += math.pow(saved[j+i] - obs[i],2)
            if sum < minsum:
                minidx = j
                minsum = sum
        return  minidx - 360
