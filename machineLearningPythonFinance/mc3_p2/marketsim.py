"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import os
import csv

from util import get_data, plot_data
from portfolio.analysis import get_portfolio_value, get_portfolio_stats, plot_normalized_data

def compute_portvals(start_date, end_date, orders_file, start_val):
    """Compute daily portfolio value given a sequence of orders in a CSV file.

    Parameters
    ----------
        start_date: first date to track
        end_date: last date to track
        orders_file: CSV file to read orders from
        start_val: total starting cash available

    Returns
    -------
        portvals: portfolio value for each trading day from start_date to end_date (inclusive)
    """
    # TODO: Your code here
    symbols = list()
    rowCount = 0
    startDate = 0
    endDate = 0
    lastRow = []

    reader = csv.reader(open(orders_file,'rU'), delimiter=',')
    for row in reader:
        if rowCount > 0:
            if rowCount == 1:
                startDate = row[0]
            symbols.append(row[1])
        rowCount += 1
        lastRow = row

    orders = pd.read_csv(orders_file, index_col='Date',
                parse_dates=True, na_values=['nan'])

    #print orders

    endDate = lastRow[0]
    uniqueList = list(set(symbols))

    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(uniqueList, dates)  # automatically adds SPY
    prices_all['CASH'] = 1.0
    ordersDF = prices_all.copy(deep=True)
    for item in uniqueList:
        ordersDF[item] = 0
    ordersDF['CASH'] = 0.0

    ordersDF = ordersDF.drop('SPY', 1)

    for index, row in orders.iterrows():
        shares = row[2]
        if row[1] == 'SELL' :
            print "SELL"
            row[2] = -1 * row[2]
        if index in ordersDF.index:
            testValue = ordersDF.get_value(index,row[0])
            setValue = row[2]
            if testValue:
                setValue = setValue + testValue

            ordersDF.set_value(index,row[0], setValue)

    #print ordersDF
    for index, row in ordersDF.iterrows():
        rowTotal = 0
        for item in uniqueList:
            price = prices_all.get_value(index,item)
            rowTotal += row[item] * price * -1
        #print rowTotal
        ordersDF.set_value(index,'CASH',rowTotal)

    #print ordersDF
    holdingsDF = ordersDF.copy(deep=True)

    holdingsDF['CASH'] = 0.0

    holdingsDF.set_value(start_date,'CASH', start_val)

    loopRow = holdingsDF.iterrows()
    holdingsDF.set_value(start_date,'CASH',start_val)

    prevValue = start_val
    for index, row in loopRow:
        sharesValue = ordersDF.get_value(index,'CASH')
        holdingsDF.set_value(index,'CASH',prevValue + sharesValue)
        prevValue = prevValue + sharesValue

    #print holdingsDF

    loopRow = holdingsDF.iterrows()

    previousValues = {}
    for item in uniqueList:
        previousValues[item] = 0

    for index, row in loopRow:
        for item in uniqueList:

            holdingsDF.set_value(index,item,row[item] + previousValues[item])

            previousValues[item] = row[item] + previousValues[item]


    dfValues = holdingsDF.copy(deep=True)

    dfValues = dfValues.drop('CASH', 1)
    dfValues['VALUES'] = 0.0

    loopRow = holdingsDF.iterrows()
    for index, row in loopRow:
        total = 0
        for item in uniqueList:
            holdingsValue = holdingsDF.get_value(index,item)
            pricesValue = prices_all.get_value(index,item)
            total += holdingsValue * pricesValue
        dfValues.set_value(index,'VALUES',total)
    #print dfValues
    finalDF = dfValues.copy(deep=True)
    for item in uniqueList:
        finalDF = finalDF.drop(item, 1)

    #print dfValues

    finalDF = finalDF.drop('VALUES', 1)
    finalDF['TOTALS'] = 0
    finalDF['TOTALS'] = dfValues['VALUES'] + holdingsDF['CASH']

    with pd.option_context('display.max_rows', 999, 'display.max_columns', 5):
        print finalDF['TOTALS']


    return finalDF['TOTALS']

def test_run():
    """Driver function."""
    # Define input parameters
    #start_date = '2011-01-14'
    #end_date = '2011-12-14'
    #orders_file = os.path.join("orders", "orders2.csv")
    #start_date = '2010-05-20'
    #end_date = '2012-06-30'

    #start_date = '2008-01-08'
    #end_date = '2008-12-22'
    start_date = '2010-01-06'
    end_date = '2010-12-30'

    orders_file = os.path.join("orders", "orders.csv")
    start_val = 10000

    print orders_file

    # Process orders
    portvals = compute_portvals(start_date, end_date, orders_file, start_val)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # if a DataFrame is returned select the first column to get a Series

    # Get portfolio stats
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals)

    # Simulate a $SPX-only reference portfolio to get stats
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]  # remove SPY
    portvals_SPX = get_portfolio_value(prices_SPX, [1.0])
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = get_portfolio_stats(portvals_SPX)

    # Compare portfolio against $SPX
    print "Data Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX: {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX: {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX: {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX: {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    # Plot computed daily portfolio value
    df_temp = pd.concat([portvals, prices_SPX['$SPX']], keys=['Portfolio', '$SPX'], axis=1)
    plot_normalized_data(df_temp, title="Daily portfolio value and $SPX")

if __name__ == "__main__":
    test_run()