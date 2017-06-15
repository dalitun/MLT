"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

from util import get_data, plot_data


def get_portfolio_value(prices, allocs, start_val=1):
    """Compute daily portfolio value given stock prices, allocations and starting value.

    Parameters
    ----------
        prices: daily prices for each stock in portfolio
        allocs: initial allocations, as fractions that sum to 1
        start_val: total starting value invested in portfolio (default: 1)

    Returns
    -------
        port_val: daily portfolio value
    """
    # TODO: Your code here

    # print prices
    # Normalize

    #print allocs

    normed = prices/prices.ix[0,:]
    alloctable = normed * allocs
    pos_vals = alloctable * start_val
    port_val = pos_vals.sum(axis=1)
    return port_val


def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    """Calculate statistics on given portfolio values.

    Parameters
    ----------
        port_val: daily portfolio value
        daily_rf: daily risk-free rate of return (default: 0%)
        samples_per_year: frequency of sampling (default: 252 trading days)

    Returns
    -------
        cum_ret: cumulative return
        avg_daily_ret: average of daily returns
        std_daily_ret: standard deviation of daily returns
        sharpe_ratio: annualized Sharpe ratio
    """
    # TODO: Your code here

    daily_rets = (port_val[1:] / port_val[:-1].values) - 1
    #daily_rets = daily_rets[1:]
    cum_ret = (port_val[-1] / port_val[0]) - 1
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = (np.mean(daily_rets[0:].values - daily_rf) / std_daily_ret) * np.sqrt(samples_per_year)

    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


def plot_normalized_data(df,prices_short_entry,prices_short_exit,prices_long_entry,prices_long_exit):

    plt.plot(df.index, df["IBM"], "b-", label='IBM')
    plt.plot(df.index, df["SMA"], "y-", label='SMA')
    plt.plot(df.index, df["upperStd"], "cyan", label='Bollinger Bands')
    plt.plot(df.index, df["lowerStd"], "cyan")
    plt.legend(loc='upper left')

    print prices_long_exit
    plt.vlines(x=prices_short_entry, ymin=60, ymax=140, colors = "red")
    plt.vlines(x=prices_short_exit, ymin=60, ymax=140, colors = "black")
    plt.vlines(x=prices_long_entry, ymin=60, ymax=140, colors = "green")
    plt.vlines(x=prices_long_exit, ymin=60, ymax=140, colors = "black")




    plt.show()

def assess_portfolio(start_date, end_date, symbols):
    """Simulate and assess the performance of a stock portfolio."""
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)  # automatically adds SPY
    prices = prices_all[symbols]  # only portfolio symbols


    #pd['MEAN'] =
    prices_all['SMA'] = pd.rolling_mean(prices, window=20)
    prices_all['Rolling Std Upper'] = prices_all['SMA'] + pd.rolling_std(prices, window=20) * 2
    prices_all['Rolling Std Lower'] = prices_all['SMA'] - pd.rolling_std(prices, window=20) * 2

    prices_all['short_entry'] = np.pad(np.diff(np.array(prices['IBM'] > prices_all['Rolling Std Upper']).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    prices_all['short_exit'] = np.pad(np.diff(np.array(prices['IBM'] > prices_all['SMA']).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    prices_all['long_entry'] = np.pad(np.diff(np.array(prices['IBM'] < prices_all['Rolling Std Lower']).astype(int)),
       (1,0), 'constant', constant_values = (0,))

    prices_all['long_exit'] = np.pad(np.diff(np.array(prices['IBM'] < prices_all['SMA']).astype(int)),
       (1,0), 'constant', constant_values = (0,))


    currentShortExit = False
    currentLongExit = False
    longEntry = []
    longExit = []
    shortEntry = []
    shortExit = []


    #Date,Symbol,Order,Shares
    rows = []
    dates = []
    for index, row in prices_all.iterrows():
        if row['short_entry'] == -1 and currentShortExit == False and currentLongExit == False:
            currentShortExit = True
            dates.append(index)
            rows.append({'Symbol':'IBM','Order':'SELL','Shares': 100})
            shortEntry.append(index)
            print index

        if row['long_entry'] == -1 and currentShortExit == False and currentLongExit == False:
            currentLongExit = True
            rows.append({'Symbol':'IBM','Order':'BUY','Shares': 100})
            dates.append(index)
            longEntry.append(index)
            print index

        if row['long_exit'] == -1 and currentShortExit == False and currentLongExit == True:
            shortExit.append(index)
            rows.append({'Symbol':'IBM','Order':'SELL','Shares': 100})
            dates.append(index)
            currentLongExit = False
            currentShortExit = False
            print index

        if row['short_exit'] == -1 and currentShortExit == True and currentLongExit == False:
            longExit.append(index)
            rows.append({'Symbol':'IBM','Order':'BUY','Shares': 100})
            dates.append(index)
            currentShortExit = False
            currentLongExit = False
            print index



    csv_out = pd.DataFrame(rows,index=dates)
    cols = ['Symbol','Order','Shares']
    csv_out = csv_out[cols]
    #print csv_out
    csv_out.to_csv('orders/orders.csv',sep=",")
    #with pd.option_context('display.max_rows', 999, 'display.max_columns', 10):
        #print prices_all

    #exit()

    #prices_short_entry = prices_all[prices_all['short_entry'] == -1].index.tolist()


    """
    print prices_short_entry
    print prices_short_exit
    print prices_long_entry
    print prices_long_exit
    """
    #print prices_all

    """

    #print prices_all
    #prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Get daily portfolio value
    #port_val = get_portfolio_value(prices, allocs, start_val)
    #plot_data(port_val, title="Daily Portfolio Value")

    # Get portfolio statistics (note: std_daily_ret = volatility)
    # cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_val)

    # Print statistics

    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocs
    print "Sharpe Ratio:", sharpe_ratio
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret

    # Compare daily portfolio value with SPY using a normalized plot

    """
    df_temp = pd.concat([prices_all['IBM'], prices_all['SMA'], prices_all['Rolling Std Upper'], prices_all['Rolling Std Lower']],  keys=['IBM', 'SMA', 'upperStd', 'lowerStd'], axis=1)
    plot_normalized_data(df_temp,shortEntry,shortExit,longEntry,longExit)


def test_run():
    """Driver function."""
    # Define input parameters

    #start_date = '2007-12-31'
    #end_date = '2009-12-31'

    start_date = '2009-12-31'
    end_date = '2010-12-31'

    symbols = ['IBM']
    start_val = 1000000  # starting value of portfolio

    # Assess the portfolio
    assess_portfolio(start_date, end_date, symbols)


if __name__ == "__main__":
    test_run()