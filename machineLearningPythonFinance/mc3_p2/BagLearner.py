"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np

class BagLearner(object):

    def __init__(self, learner, **kwargs):
        #print self

        self.learners = []
        for i in range(0,kwargs['bags']):
            self.learners.append(learner(**kwargs['kwargs']))


    def addEvidence(self,dataX,dataY):
        finalData = np.column_stack( (dataX,dataY) )
        #np.set_printoptions(threshold='nan')
        # ADDED THIS AFTER THE FACT FOR TESTING TO COMPARE TO OTHERS ON PIAZZA
        np.random.seed(42)
        for learner in self.learners:
            randomData = finalData[np.random.choice(finalData.shape[0], finalData.shape[0])]
            #print randomData
            trainX = randomData[0:,0:-1]
            trainY = randomData[0:,-1]
            learner.addEvidence(trainX,trainY)

    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        results = []
        for learner in self.learners:
            results.append(learner.query(points))

        theMean = np.mean( results, axis=0 )
        return theMean

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
