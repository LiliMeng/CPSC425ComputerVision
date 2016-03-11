
import numpy as np


def boxfilter(n):
    assert n%2!=0, "The Dimensions must be odd"
    b=np.full((n,n),0.04)
    total=np.sum(np.sum(b))
    result = b/total
    return result
    
print boxfilter(3)
print boxfilter(5)
print boxfilter(4)

