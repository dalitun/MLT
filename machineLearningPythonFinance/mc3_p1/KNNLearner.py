"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np
import math as ma

class KNNLearner(object):

    def __init__(self,k):
        self.k = k

    def findDistance(self, testSet, trainingSet, testLength):
        totalDistances = 0
        for x in range(testLength):
            totalDistances += pow((testSet[x] - trainingSet[x]), 2)
        return ma.sqrt(totalDistances)

    def findClosetPoints(self, training, test):
        testLength = len(test)
        distances = []
        for x in range(len(training)):
            distance = self.findDistance(test, training[x], testLength)
            distances.append((training[x][2], distance))
        distances.sort(key=lambda tup: tup[1])
        kPoints = distances[0:self.k]
        sum = 0
        for x in kPoints:
            sum += x[0]
        return sum / self.k

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        finalData = np.column_stack( (dataX,dataY) )
        self.model_coefs = finalData
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        predY = []
        for x in range(len(points)):
            #print points[x]
            predY.append(self.findClosetPoints( self.model_coefs , points[x]))

        #print "DONE"
        return np.asarray(predY)



if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
