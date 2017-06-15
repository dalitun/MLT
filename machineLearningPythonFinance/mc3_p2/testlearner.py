"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import KNNLearner as knn
import BagLearner as bl
import best4KNN as bknn
import best4linreg as bln
import matplotlib.pyplot as plt

if __name__=="__main__":
    inf = open('Data/ripple.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    #bestCase = bknn.best4KNN()
    #data = bestCase.generateSet()

    #bestCase = bln.best4linreg()
    #data = bestCase.generateSet()


    # compute how much of the data is training and testing
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]

    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]



    # create a learner and train it

    # print data

    #learner = knn.KNNLearner(3)
    #learner.addEvidence(trainX, trainY) # train it

    # create a learner and train it
    #learner = lrl.LinRegLearner() # create a LinRegLearner
    #learner.addEvidence(trainX, trainY) # train it

    #learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":3}, bags = 20, boost = False)
    #learner.addEvidence(trainX, trainY)

    """
    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])



    print "---------------- LINEAR ---------------"


    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample

    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])

    f = open('Data/results.csv','w')
    # python will convert \n to os.linesep

    #print predY

    for i in range(0,data.shape[0]):
        col1 = math.ceil(data[i][0] * 100.0) / 100.0
        col2 = math.ceil(data[i][1] * 100.0) / 100.0
        col3 = math.ceil(data[i][2] * 100.0) / 100.0

        #col4 = math.ceil(data[i][3] * 100.0) / 100.0
        f.write(str(col1) + ', ' + str(col2) + ', ' + str(col3) + '\n')
    f.close()

    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]

    """

    print "---------------- KNN ---------------"

    inSampleError = []
    outOfSampleError = []
    kArr = []
    for i in range(3,4):
        #learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":3}, bags = 20, boost = False)
        #learner.addEvidence(trainX, trainY)

        print "BAGS:"
        print i
        learner = knn.KNNLearner(k = 3)
        learner.addEvidence(trainX, trainY) # tra

        kArr.append(i)
        #learner = knn.KNNLearner(i)
        #learner.addEvidence(trainX, trainY) # train it
        predY = learner.query(trainX) # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        print "In sample results"
        print "RMSE: ", rmse
        inSampleError.append(rmse)
        c = np.corrcoef(predY, y=trainY)
        print "corr: ", c[0,1]
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        print "Out of sample results"
        print "RMSE: ", rmse
        outOfSampleError.append(rmse)
        c = np.corrcoef(predY, y=testY)
        print "corr: ", c[0,1]


    f = open('Data/knnoverfitting.csv','w')
    # python will convert \n to os.linesep

    #print predY

    for i in range(0,len(kArr)):
        col1 = inSampleError[i]
        col2 = outOfSampleError[i]
        col3 = kArr[i]

        #col4 = math.ceil(data[i][3] * 100.0) / 100.0
        f.write(str(col1) + ', ' + str(col2) + ', ' + str(col3) + '\n')
    f.close()




