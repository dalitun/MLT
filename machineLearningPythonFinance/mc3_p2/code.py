"""MC3-P2"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import LinRegLearner as lrl
import KNNLearner as knn
import BagLearner as bl

from util import get_data, plot_data


def buySell(dataFrame) :
    dataFrame['short_entry'] = np.pad(np.diff(np.array(dataFrame['predY'] < 0.02).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    dataFrame['short_exit'] = np.pad(np.diff(np.array(dataFrame['predY'] > 0.02).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    dataFrame['long_entry'] = np.pad(np.diff(np.array(dataFrame['predY'] > 0.02).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    dataFrame['long_exit'] = np.pad(np.diff(np.array(dataFrame['predY'] < 0.02).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    return dataFrame


def generateOrders(prices_all_temp, predY, symbols):
    currentShortExit = False
    currentLongExit = False
    longEntry = []
    longExit = []
    shortEntry = []
    shortExit = []


    prices_all_temp['predY'] = 0.0
    i = 0
    loopRow = prices_all_temp.iterrows()
    for index, row in loopRow:
        prices_all_temp.set_value(index,'predY',predY[i])
        i += 1

    prices_all_temp['predYPrice'] = prices_all_temp[symbols[0]] * (prices_all_temp['predY'] + 1)

    #print prices_all_temp

    prices_all_temp = buySell(prices_all_temp)


    #exit();

    #Date,Symbol,Order,Shares
    #print prices_all_temp
    rows = []
    dates = []
    currentShortEntry = False
    currentLongEntry = False

    """
    for index, row in prices_all_temp.iterrows():
        if row['short_entry'] == 1 and row['short_exit'] == -1:
            rows.append({'Symbol':symbols[0],'Order':'SELL','Shares': 100})
            dates.append(index)
            shortEntry.append(index)
            currentShortEntry = True

        if row['long_entry'] == 1 and row['long_exit'] == -1:
            rows.append({'Symbol':symbols[0],'Order':'BUY','Shares': 100})
            dates.append(index)
            longEntry.append(index)
            currentLongEntry = True

        if currentShortExit:
            rows.append({'Symbol':symbols[0],'Order':'BUY','Shares': 100})
            dates.append(index)
            currentShortExit = True

        if currentLongExit:
            rows.append({'Symbol':symbols[0],'Order':'SELL','Shares': 100})
            dates.append(index)
            currentLongExit = True
    """

    for index, row in prices_all_temp.iterrows():
        if row['short_entry'] == 1 and currentShortExit == False and currentLongExit == False:
            currentShortExit = True
            dates.append(index)
            rows.append({'Symbol':symbols[0],'Order':'SELL','Shares': 100})
            shortEntry.append(index)
            #print index

        if row['long_entry'] == 1 and currentShortExit == False and currentLongExit == False:
            currentLongExit = True
            rows.append({'Symbol':symbols[0],'Order':'BUY','Shares': 100})
            dates.append(index)
            longEntry.append(index)
            #print index

        if row['long_exit'] == 1 and currentShortExit == False and currentLongExit == True:

            shortExit.append(index)
            rows.append({'Symbol':symbols[0],'Order':'SELL','Shares': 100})

            dates.append(index)
            currentLongExit = False
            currentShortExit = False
            #print index

        if row['short_exit'] == 1 and currentShortExit == True and currentLongExit == False:
            longExit.append(index)
            rows.append({'Symbol':symbols[0],'Order':'BUY','Shares': 100})
            #print "HERE"

            dates.append(index)
            currentShortExit = False
            currentLongExit = False
            #print index

    csv_out = pd.DataFrame(rows,index=dates)
    cols = ['Symbol','Order','Shares']
    csv_out = csv_out[cols]
    #print csv_out
    csv_out.to_csv('orders/orders.csv',sep=",")

    #prices_all_chart = prices_all_temp.ix['2008-03-31':'2008-06-04']
    prices_all_chart = prices_all_temp
    #print prices_all_chart
    #print prices_all_chart.index

    plt.plot(prices_all_chart.index, prices_all_chart[symbols[0]], "b-", label=symbols[0])
    plt.plot(prices_all_chart.index, prices_all_chart['ytrainPrice'], "purple", label='true y')
    #plt.plot(prices_all_chart.index, prices_all_chart['ytrainPrice'], "purple", label='true y')
    plt.plot(prices_all_chart.index, prices_all_chart['predYPrice'], "y-", label='predY')
    plt.legend(loc='upper left')


    plt.vlines(x=shortEntry, ymin=60, ymax=90, colors = "red")
    plt.vlines(x=shortExit, ymin=60, ymax=90, colors = "black")
    plt.vlines(x=longEntry, ymin=60, ymax=90, colors = "green")
    plt.vlines(x=longExit, ymin=60, ymax=90, colors = "black")


    """
    plt.vlines(x=shortEntry, ymin=60, ymax=160, colors = "red")
    plt.vlines(x=shortExit, ymin=60, ymax=160, colors = "black")
    plt.vlines(x=longEntry, ymin=60, ymax=160, colors = "green")
    plt.vlines(x=longExit, ymin=60, ymax=160, colors = "black")
    """

    plt.show()

    return prices_all_temp


def shiftY(shift,prices_all,symbols):


    #if shift:
    prices_all['y'] = ((prices_all[symbols[0]].shift(-5)/prices_all[symbols[0]]) - 1.0)
    #else:
        #prices_all['y'] = ((prices_all[symbols[0]].shift(-1)/prices_all[symbols[0]]) - 1.0)

    prices_all['ytrainPrice'] = prices_all[symbols[0]] * (prices_all['y'] + 1)
    #print prices_all
    return prices_all


def calculate(prices_all, symbols, prices):
    prices_all = prices_all.drop('SPY', 1)
    prices_all['SMA'] = pd.rolling_mean(prices, window=10)
    prices_all['BB_value'] = (prices_all[symbols[0]] -  prices_all['SMA'])/(1.9 * prices_all[symbols[0]].std())
    prices_all['momentum'] = (prices_all[symbols[0]]/prices_all[symbols[0]].shift(10)) - 1

    daily_rets = (prices_all[symbols[0]][1:] / prices_all[symbols[0]][:-1].values) - 1
    prices_all['volatility'] = pd.rolling_std(daily_rets , window=10)

    #prices_all['exponmovtemp'] = pd.ewma(prices_all[symbols[0]],span = 10, min_periods = 5)
    #prices_all['exponmov'] = (prices_all['exponmovtemp'][1:] / prices_all['exponmovtemp'][:-1].values) - 1
    #prices_all['shifted'] = prices_all[symbols[0]].shift(5)

    prices_all = prices_all.drop('SMA', 1)
    #prices_all = prices_all.drop('exponmovtemp', 1)
    return prices_all

def assess_portfolio(start_date, end_date, symbols):
    """Simulate and assess the performance of a stock portfolio."""
    # Read in adjusted closing prices for given symbols, date range
    pd.set_option('display.expand_frame_repr', False)
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices_all_temp = prices_all
    prices = prices_all[symbols]  # only portfolio symbols

    prices_all_temp = prices_all
    prices_all_temp = calculate(prices_all_temp, symbols, prices)
    prices_all_temp = shiftY(False,prices_all_temp,symbols)
    prices_all_test = prices_all_temp.ix['2009-12-31':'2010-12-31']
    prices_all_temp = prices_all_temp.ix['2007-12-31':'2008-12-31']

    """
    prices_all_test = prices_all_temp.ix['2008-12-31':'2009-12-31']

    prices_all_test = calculate(prices_all_test, symbols, prices)
    prices_all_test = shiftY(False,prices_all_test,symbols)
    prices_all_test = prices_all_test.fillna(method='bfill')
    prices_all_test = prices_all_test.fillna(method='ffill')

    prices_all_temp = prices_all_temp.ix['2007-12-31':'2008-12-31']
    prices_all_temp = calculate(prices_all_temp, symbols, prices)
    prices_all_temp = shiftY(False,prices_all_temp,symbols)
    prices_all_temp = prices_all_temp.fillna(method='bfill')
    prices_all_temp = prices_all_temp.fillna(method='ffill')
    """

    # separate out training and testing data
    #print prices_all_temp
    trainX = prices_all_temp.values[:,1:-2]
    trainY = prices_all_temp.values[:,-2]

    testX = prices_all_test.values[:,1:-2]
    testY = prices_all_test.values[:,-2]

    #print trainX

    #learner = bl.BagLearner(learner = knn.KNNLearner, kwargs = {"k":3}, bags = 50, boost = False)
    #learner.addEvidence(trainX, trainY)

    learner = knn.KNNLearner(3)
    learner.addEvidence(trainX, trainY) # train it

    #learner = lrl.LinRegLearner()
    #learner.addEvidence(trainX, trainY) # train it

    predY = learner.query(trainX) # get the predictons
    generateOrders(prices_all_temp,predY, symbols)
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])

    print "---------------- ----- ---------------"

    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    #exit()

    predY = learner.query(testX) # get the predictions
    generateOrders(prices_all_test,predY, symbols)
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])

    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]


def test_run():
    """Driver function."""
    # Define input parameters

    start_date = '2007-11-30'
    end_date = '2011-01-09'

    symbols = ['IBM']
    start_val = 1000000  # starting value of portfolio

    # Assess the portfolio
    assess_portfolio(start_date, end_date, symbols)


if __name__ == "__main__":
    test_run()