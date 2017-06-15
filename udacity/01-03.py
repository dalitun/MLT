# Timing Python operations

import time

t1 = time.time()
print 'Execute your function'
t2 = time.time()
print 'The time taken by print statement is {} seconds'.format(t2-t1)