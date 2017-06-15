"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np

class best4KNN(object):

    def __init__(self):
        pass # move along, these aren't the drones you're looking for

    def generateSet(self):
        counter = 0
        secondCounter = 0
        switch = False

        arr = np.ones([1000, 3])
        for i in range(0,arr.shape[0]):

            if secondCounter == 10:
                switch = True
            elif secondCounter == 0:
                switch = False

            if switch == True:
                 secondCounter -= 1
            else:
                 secondCounter += 1

            counter += 1

            arr[i][0] = counter
            arr[i][1] = counter
            arr[i][2] = secondCounter



            if counter == 20:
                counter = 0

        return arr

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
