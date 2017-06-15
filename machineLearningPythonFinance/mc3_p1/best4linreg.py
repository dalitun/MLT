"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np
import math as mn

class best4linreg(object):

    def __init__(self):
        pass # move along, these aren't the drones you're looking for

    def generateSet(self):
        closePoint = True
        counter = 0
        newValueOne = 0
        newValueTwo = 0
        arr = np.ones([1000, 3])
        for i in range(0,arr.shape[0]):

            counter += 1
            if counter % 18 == 1:
                closePoint = False
            else:
                closePoint = True

            if closePoint == True:
                #print "close"
                newValueOne = newValueOne
                newValueTwo = newValueTwo
            else:
                #print "not"
                newValueOne = (newValueOne * counter) + 1
                newValueTwo = (newValueOne * counter) + 2

            arr[i][0] = newValueOne
            arr[i][1] = newValueTwo
            arr[i][2] = counter

            if counter == 40:
                counter = 0
                newValueOne = 0
                newValueTwo = 0

        return arr

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
