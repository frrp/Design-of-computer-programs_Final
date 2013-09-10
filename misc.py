__author__ = 'fr'

def same_first_last(nums):
    a = nums[0]
    b = nums[-1]
    return a == b
"""
x1 = [1, 2, 3, 1]
x1.sort()
print x1
print same_first_last(x1)
"""

def sum_of_ints(n):
    if (n <= 1):
        return n
    else:
        return sum_of_ints(n-1) + n


#Version B
def sum_of_ints1(n):
    if(n <=  1):
        return n
    else:
        sum=n
        while (n > 1):
            n=n-1
            sum=sum + n
        return sum

import time

def test():
    t0 = time.time()
    for example in examples:
        print; print 13*' ', example
        print '%6.4f sec:   %s ' % timedcall(solve, example)
    print '%6.4f tot.' % (time.time()-t0)

def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1-t0, result

print timedcall(sum_of_ints1, 1000)

print timedcall(sum_of_ints, 1000)