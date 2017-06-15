"""
kurtosis (quantifies whether the shape of the data distribution matches the Gaussian distribution)
  + fat tails
  - skinny tails
  
Scatterplots
  slope (Beta): how reactive a stock is to the market - higher Beta means
the stock is more reactive to the market

NOTE: slope != correlation
correlation is a measure of how tightly do the individual points fit the line
  
  intercept (alpha): +ve --> the stock on avg is performing a little bit better
than the market

In many cases in financial research we assume the daily returns are normally distributed,
but this can be dangerous because it ignores kurtosis or the probability in the
tails.
"""

# Compute daily returns
daily_returns = compute_daily_returns(df)

# Plot a histogram
daily_returns.hist(bins=20)

# Get mean as standard deviation
mean = daily_returns['SPY'].mean()
std = daily_returns['SPY'].std()

plt.axvline(mean, color='w', linestyle='dashed', linewidth=2)
plt.axvline(std, color='r', linestyle='dashed', linewidth=2)
plt.axvline(-std, color='r', linestyle='dashed', linewidth=2)
plt.show()

# Compute kurtosis
daily_returns.kurtosis()


# Compute and plot two histograms on the same chart
daily_returns['SPY'].hist(bins=20, label='SPY')
daily_returns['XOM'].hist(bins=20, label='XOM')
plt.legend(loc='upper right')
plt.show()


# Scatterplots
daily_returns.plot(kind='scatter', x='SPY', y='XOM')  # SPY vs XOM
beta_XOM, alpha_XOM = np.polyfit(daily_returns['SPY'], daily_returns['XOM'], 1)  # fit poly degree 1
plt.plot(daily_returns['SPY'], beta_XOM*daily_returns['SPY'] + alpha_XOM, '-', color='r')

daily_returns.plot(kind='scatter', x='SPY', y='GLD')  # SPY vs GLD
beta_GLD, alpha_GLD = np.polyfit(daily_returns['SPY'], daily_returns['GLD'], 1)  # fit poly degree 1
plt.plot(daily_returns['SPY'], beta_GLD*daily_returns['SPY'] + alpha_GLD, '-', color='r')

# Calculate correlation coefficient
daily_returns.corr(method='pearson')