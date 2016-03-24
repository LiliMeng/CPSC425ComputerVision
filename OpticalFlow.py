from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal
import numpy.linalg as lin
from numpy.linalg import inv

# START OF FUNCTIONS CARRIED FORWARD FROM ASSIGNMENT 2

def boxfilter(n):
    assert n%2!=0, "The Dimensions must be odd"
     # create an empty n by n numpy array
    boxFilter = np.empty([n, n])

    # fill each entry with 1/n^2 
    boxFilter.fill(float(1) / (n * n))
    
    return boxFilter

def gauss1d(sigma):
    tmp=round(sigma*6)
    if tmp%2!=0:
    	length=tmp
    else:
    	length=tmp+1
    x=range(-(int)(length/2),(int)(length/2+1))
    PI=3.1415926 
    results=[]
    #print "the result for sigma value %f is the following:" %sigma
    for index in range(len(x)):
    	result= 1/(math.sqrt(2*PI)*math.pow(sigma, 2))*math.exp(-math.pow(x[index],2)/(2*math.pow(sigma,2))) 
    	results.append(result)
    total=sum(results)
    results[:] = [x / total for x in results]
    #print results
    return np.array(results)
    
def gauss2d(sigma):
    gaus1d=gauss1d(sigma)
    gaus1d = gaus1d[np.newaxis]
    gaus1dTrans=np.transpose(gaus1d)
    finalResult=signal.convolve2d(gaus1d,gaus1dTrans)  # a 2D Gaussian can be formed by convolution of a 1D Gaussian with its transpose.
    return finalResult


def gaussconvolve2d(image,sigma):
    filterG=gauss2d(sigma)
    gaussconvolve2dresult=signal.convolve2d(image,filterG,'same')   #convolve the gaussian filter with image
    return gaussconvolve2dresult

# END OF FUNCTIONS CARRIED FORWARD FROM ASSIGNMENT 2

# Define a function, boxconvolve2d, to convolve an image with a boxfilter of size n
# (used in Estimate_Derivatives below).

def boxconvolve2d(image, n):
    filterB=boxfilter(n)      
    boxconvovle2dResult=signal.convolve2d(image,filterB,'same')  #convolve an image with a boxfilter with size n
    return boxconvovle2dResult

def Estimate_Derivatives(im1, im2, sigma=1.5, n=3):
    """
    Estimate spatial derivatives of im1 and temporal derivative from im1 to im2.

    Smooth im1 with a 2D Gaussian of the given sigma.  Use first central difference to
    estimate derivatives.

    Use point-wise difference between (boxfiltered) im2 and im1 to estimate temporal derivative
    """
    # UNCOMMENT THE NEXT FOUR LINES WHEN YOU HAVE DEFINED THE FUNCTIONS ABOVE
    im1_smoothed = gaussconvolve2d(im1,sigma)
    Ix, Iy = np.gradient(im1_smoothed)
    It = boxconvolve2d(im2, n) - boxconvolve2d(im1, n)   #estimate temporal difference
    # make sure all the partial derivative estimates returned are the same size as the original image
    assert(Ix.shape==im1.shape)
    assert(Iy.shape==im1.shape)
    assert(It.shape==im1.shape)
    return Ix, Iy, It
    
 

def Optical_Flow(im1, im2, x, y, window_size, sigma=1.5, n=3):
    assert((window_size % 2) == 1) , "Window size must be odd"
    # UNCOMMENT THE NEXT LINE WHEN YOU HAVE COMPLETED Estimate_Derivatives
    Ix, Iy, It = Estimate_Derivatives(im1, im2, sigma, n)
    half = np.floor(window_size/2)
    # select the three local windows of interest
    # UNCOMMENT THE NEXT LINE WHEN YOU HAVE COMPLETED Estimate_Derivatives
    win_Ix = Ix[y-half:y+half+1, x-half:x+half+1].T
   
    #
    # PROVIDE THE REST OF THE IMPLEMENTATION HERE (BASED ON THE WIKIPEDIA ARTICLE)
    #
    win_Iy = Iy[y-half:y+half+1, x-half:x+half+1].T
    win_It = -It[y-half:y+half+1, x-half:x+half+1].T
    #win_It =
    # ...
    # calculate the matrix A by first flatting win_Ix and win_Iy, then transpose
    A = np.vstack((win_Ix.flatten(), win_Iy.flatten())).T
    V = np.linalg.pinv(A)*win_It.flatten()    # inverse(A)*Av=inverse(A)*b
    
    #################################from PIL import ImageShow
    # change the return line to:
    return V[1], V[0]
    # (when you have completed the implementation)
    #################################
    #return -1, 2  # skeleton program returns a hard-coded value

def AppendImages(im1, im2):
    """Create a new image that appends two images side-by-side.

    The arguments, im1 and im2, are PIL images of type RGB
    """
    im1cols, im1rows = im1.size
    im2cols, im2rows = im2.size
    im3 = Image.new('RGB', (im1cols+im2cols, max(im1rows,im2rows)))
    im3.paste(im1,(0,0))
    im3.paste(im2,(im1cols,0))
    return im3

def DisplayFlow(im1, im2, x, y, uarr, varr):
    """Display optical flow match on a new image with the two input frames placed side by side.

    Arguments:
     im1           1st image (in PIL 'RGB' format)
     im2           2nd image (in PIL 'RGB' format)
     x, y          point coordinates in 1st image
     u, v          list of optical flow values to 2nd image

    Displays and returns a newly created image (in PIL 'RGB' format)
    """
    im3 = AppendImages(im1,im2)
    offset = im1.size[0]
    draw = ImageDraw.Draw(im3)
    xinit = x+uarr[0]
    yinit = y+varr[0]
    for u,v,ind in zip(uarr[1:], varr[1:], range(1, len(uarr))):
		draw.line((offset+xinit, yinit, offset+xinit+u, yinit+v),fill="red",width=2)
		xinit += u
		yinit += v
    draw.line((x, y, offset+xinit, yinit), fill="yellow", width=2)
    im3.show()
    del draw
    return im3

def HitContinue(Prompt='Hit any key to continue'):
    raw_input(Prompt)

##############################################################################
#                  Here's your assigned target point to track                #
##############################################################################

# uncomment the next two lines if the leftmost digit of your student number is 0
#x=222
#y=213
# uncomment the next two lines if the leftmost digit of your student number is 1
#x=479
#y=141
# uncomment the next two lines if the leftmost digit of your student number is 2
#x=411
#y=242
# uncomment the next two lines if the leftmost digit of your student number is 3
#x=152
#y=206
# uncomment the next two lines if the leftmost digit of your student number is 4
#x=278
#y=277
# uncomment the next two lines if the leftmost digit of your student number is 5
#x=451
#y=66
# uncomment the next two lines if the leftmost digit of your student number is 6
#x=382
#y=65
# uncomment the next two lines if the leftmost digit of your student number is 7
x=196
y=197
# uncomment the next two lines if the leftmost digit of your student number is 8
#x=274
#y=126
# uncomment the next two lines if the leftmost digit of your student number is 9
#x=305
#y=164

##############################################################################
#                            Global "magic numbers"                          #
##############################################################################

# window size (for estimation of optical flow)
window_size=21

# sigma of the 2D Gaussian (used in the estimation of Ix and Iy)
sigma=1.5

# size of the boxfilter (used in the estimation of It)
n = 3

##############################################################################
#             basic testing (optical flow from frame 7 to 8 only)            #
##############################################################################

# scale factor for display of optical flow (to make result more visible)
scale=10

PIL_im1 = Image.open('frame07.png')
PIL_im2 = Image.open('frame08.png')
im1 = np.asarray(PIL_im1)
im2 = np.asarray(PIL_im2)
dx, dy = Optical_Flow(im1, im2, x, y, window_size, sigma, n)
#print 'Optical flow: [', dx, ',', dy, ']'
plt.imshow(im1, cmap='gray')
plt.hold(True)
plt.plot(x,y,'xr')
plt.plot(x+dx*scale,y+dy*scale, 'dy')
print 'Close figure window to continue...'
plt.show()
uarr = [dx]
varr = [dy]

##############################################################################
#                   run the remainder of the image sequence                  #
##############################################################################

# UNCOMMENT THE CODE THAT FOLLOWS (ONCE BASIC TESTING IS COMPLETE/DEBUGGED)

print 'frame 7 to 8'
DisplayFlow(PIL_im1, PIL_im2, x, y, uarr, varr)
#HitContinue()

"""
prev_im = im2
xcurr = x+dx
ycurr = y+dy
offset = PIL_im1.size[0]

for i in range(8, 14):
    im_i = 'frame%0.2d.png'%(i+1)
    print 'frame', i, 'to', (i+1)
    PIL_im_i = Image.open('%s'%im_i)
    numpy_im_i = np.asarray(PIL_im_i)
    dx, dy = Optical_Flow(prev_im, numpy_im_i, xcurr, ycurr, window_size, sigma, n)
    xcurr += dx
    ycurr += dy
    prev_im = numpy_im_i
    uarr.append(dx)
    varr.append(dy)
    # redraw the (growing) figure
    DisplayFlow(PIL_im1, PIL_im_i, x, y, uarr, varr)
    HitContinue()
"""

##############################################################################
# Don't forget to include code to document the sequence of (x, y) positions  #
# of your feature in each frame successfully tracked.                        #
##############################################################################
