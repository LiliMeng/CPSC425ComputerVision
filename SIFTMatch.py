from PIL import Image, ImageDraw
import numpy as np
import csv
import math
import random

def ReadKeys(image):
    """Input an image and its associated SIFT keypoints.

    The argument image is the image file name (without an extension).
    The image is read from the PGM format file image.pgm and the
    keypoints are read from the file image.key.

    ReadKeys returns the following 3 arguments:

    image: the image (in PIL 'RGB' format)

    keypoints: K-by-4 array, in which each row has the 4 values specifying
    a keypoint (row, column, scale, orientation).  The orientation
    is in the range [-PI, PI] radians.

    descriptors: a K-by-128 array, where each row gives a descriptor
    for one of the K keypoints.  The descriptor is a 1D array of 128
    values with unit length.
    """
    im = Image.open(image+'.pgm').convert('RGB')
    keypoints = []
    descriptors = []
    first = True
    with open(image+'.key','rb') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC,skipinitialspace = True)
        descriptor = []
 	for row in reader:
            if len(row) == 2:
                assert first, "Invalid keypoint file header."
                assert row[1] == 128, "Invalid keypoint descriptor length in header (should be 128)."
                count = row[0]
                first = False
            if len(row) == 4:
                keypoints.append(np.array(row))
            if len(row) == 20:
                descriptor += row
            if len(row) == 8:
                descriptor += row
                assert len(descriptor) == 128, "Keypoint descriptor length invalid (should be 128)."
                #normalize the key to unit length
                descriptor = np.array(descriptor)
                descriptor = descriptor / math.sqrt(np.sum(np.power(descriptor,2)))
                descriptors.append(descriptor)
                descriptor = []
    assert len(keypoints) == count, "Incorrect total number of keypoints read."
    print "Number of keypoints read:", int(count)
    return [im,keypoints,descriptors]

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

def DisplayMatches(im1, im2, matched_pairs):
    """Display matches on a new image with the two input images placed side by side.

    Arguments:
     im1           1st image (in PIL 'RGB' format)
     im2           2nd image (in PIL 'RGB' format)
     matched_pairs list of matching keypoints, im1 to im2
ath
    Displays and returns a newly created image (in PIL 'RGB' format)
    """
    im3 = AppendImages(im1,im2)
    offset = im1.size[0]
    draw = ImageDraw.Draw(im3)
    for match in matched_pairs:
        draw.line((match[0][1], match[0][0], offset+match[1][1], match[1][0]),fill="red",width=2)
    im3.show()
    return im3

def match(image1,image2):
    """Input two images and their associated SIFT keypoints.
    Display lines connecting the first 5 keypoints from each image.
    Note: These 5 are not correct matches, just randomly chosen points.
ath
    The arguments image1 and image2 are file names without file extensions.

    Returns the number of matches displayed.

    Example: match('scene','book')
    """
    im1, keypoints1, descriptors1 = ReadKeys(image1)
    im2, keypoints2, descriptors2 = ReadKeys(image2)
    #print(descriptors1)
    #print(descriptors2)
    #
    # REPLACE THIS CODE WITH YOUR SOLUTION (ASSIGNMENT 5, QUESTION 3)
    
    distRatio = 0.75
    matched_pairs = []
    # For each descriptor in the first image, select its match to the second image
    descriptors2t = np.transpose(descriptors2)   # Precompute the matrix transpose of descriptors2
    for i in range(len(keypoints1)):
	dotproducts=np.dot(descriptors1[i],descriptors2t)      #Compute vector of dot products
	aCos=np.arccos(dotproducts)
 	
	results3=sorted(aCos)    # Take inverse cosine and sort results
        results3Index=np.argsort(aCos) #the sorted index
 
   
    # Check if nearest neighbor has angle less than distRatio times the 2nd nearest neighbor
       	if(results3[0]<distRatio*results3[1]):
                matched_pairs.append((keypoints1[i],keypoints2[results3Index[0]]))
                print "index in image1: ",i, " the location, scale and orientation of keypoints1:", keypoints1[i]
                print "index in image2: ",results3Index[0], " the location, scale and orientation of keypoints2:", keypoints2[results3Index[0]]
                print '*****************************'
    print "Number of matched keypoints:", len(matched_pairs)   
    
   
    #Perform RANSAC 
    iterationNum =10
    inlierNumList=[]  #store the inlier number of the 10 iterations
    inlierMatchIterationList=[] #store the inlier match for all the 10 iterations
    #Repeat random selection 10 times
    for i in range(iterationNum): 
       inlierMatchList=[]
       #Select one random match index and the random match
       randomIndex = random.randrange(len(matched_pairs)) 
       oneRandomMatch=matched_pairs[randomIndex]
     
       #calculate the orientation difference and scale difference of one random match
       orientationDiff=abs(oneRandomMatch[0][3]-oneRandomMatch[1][3]) # the orientation difference of two keypoints in one match
       scaleDiff=(oneRandomMatch[0][2]-oneRandomMatch[1][2])/oneRandomMatch[0][2] #the scale difference for two keypoints in one match
       #print "the orientation diff of one random match: ", orientationDiff
       #print "the scale diff of one random match: ", scaleDiff       
       scale_tolerence=0.5    #the scale tolerance
       orientation_tolerence=20*math.pi/180 #the orientation tolerance
       #campare orientation and scale difference of the the random selected match with the rest of the matches  
       for j in range(len(matched_pairs)):
           orientationDiff1=abs(matched_pairs[j][0][3]-matched_pairs[j][1][3])
           #print "orientationDiff1: ", orientationDiff1
           scaleDiff1=(matched_pairs[j][0][2]-matched_pairs[j][1][2])/matched_pairs[j][0][2]
          # print "scaleDiff1: ", scaleDiff1
           if abs(orientationDiff1-orientationDiff)<orientation_tolerence and scaleDiff1/scaleDiff<(1+scale_tolerence) and scaleDiff1/scaleDiff>(1-scale_tolerence):
               inlierMatch=matched_pairs[j]
               #print "inlierMatch: ", inlierMatch
               inlierMatchList.append(inlierMatch)
               
       inlierMatchIterationList.append(inlierMatchList)  
       inlierNumList.append(len(inlierMatchList))
    print  "inlierNum: ", len(inlierMatchList)
    print inlierNumList
    
    #find the maximum inlier of the 10 iterations
    maxInlierNum=max(inlierNumList)
    inlierIndex=inlierNumList.index(maxInlierNum)
    print "the maximum inlier number in the 10 iterations: ", maxInlierNum
    
    #find the matching result after performing RANSAC
    resultMatch=inlierMatchIterationList[inlierIndex]
    
    #calculate the inlier ratio
    inlierRatio=maxInlierNum/(len(matched_pairs)*1.0)
    print "matched keypoints number before RANSAC: ", len(matched_pairs)
    print "inlier ratio: ", inlierRatio
    
    im3 = DisplayMatches(im1, im2, matched_pairs)
    #im3 = DisplayMatches(im1, im2, resultMatch)
    return im3

#Test run...
#match('scene','basmati')
#match('library2','library')
match('scene', 'book')

