from PIL import Image
import numpy as np
import math
from scipy import signal

def boxfilter(n):
    assert n%2!=0, "The Dimensions must be odd"
    b=np.full((n,n),0.4)
    print b
    return 


