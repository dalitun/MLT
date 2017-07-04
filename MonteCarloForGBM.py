# Example of Monte Carlo simulation for the GBM process
# Copyright (C) Nakamura Seminars (www.nakamuraseminars.com)
# Distributed under the GNU Public License (GPL version 2) 

import numpy as np 
import pylab as pl

# variables and set-up
M = 1000 	# Number of paths
N = 50	 	# Number of time steps
T = 1.0 	# Simulation time horizon

sigma = 0.3 	# annual volatlity 
mu = 0.05	# annual drift rate

dt = T/N	# simulation time step 
S0 = 100	# assset price at t=0

S = np.zeros((M,N+1))
S[:,0] = S0

# path generation
for m in range(M):
  for n in range(N):
    eps = np.random.normal(0, 1, 1)[0]
    print eps
    S[m,n+1] = S[m,n]*np.exp( (mu-0.5*sigma**2)*dt + eps*sigma*np.sqrt(dt) );
    print S[m,n+1]
# Admittedly this is not a very efficient implementation.
# The code should be vectorized - rewrite path generation!
# (uncomment the below to test)
# for n in range(N):
#   eps = np.random.normal(0, 1, (M))
#   S[:,n+1] = S[:,n]*np.exp((mu-0.5*sigma**2)*dt + eps*sigma*np.sqrt(dt));

# or even faster (but less transparent)
# eps = np.random.normal(0, 1, (M,N))
# S[:,1:] = np.exp((mu-0.5*sigma**2)*dt + eps*sigma*np.sqrt(dt));
# S = np.cumprod(S, axis = 1);

# now we use it for something
pl.plot(np.linspace(0,T,N+1), np.percentile(S, 95, axis = 0))
pl.title('asset price projection at 95 percentile')
pl.xlabel('t')
pl.show()
