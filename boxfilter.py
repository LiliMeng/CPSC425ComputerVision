from PIL import Image
import numpy as np
import math
from scipy import signal

def boxfilter(n):
    assert n%2!=0, "The Dimensions must be odd"
    b=np.full((n,n),0.04)
    total=sum(map(sum, b))
    b[:] = [x / total for x in b]
    print b
    return b

boxfilter(3)
boxfilter(4)
boxfilter(5)


