#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc


def MakePyramid(image,minsize):
    pyramid = []
    #im=Image.open(image)
    while(image.size[0]>=minsize and image.size[1]>=minsize):
        pyramid.append(image)
    	image=image.resize((int(image.size[0]*0.75),int(image.size[1]*0.75)), Image.BICUBIC)
    return pyramid

def ShowPyramid(pyramid1):
    width =0
    height = 0
    for img in pyramid1:
	width = width +img.size[0]
        height = max(height, img.size[1])
  
    image = Image.new("L", (width,height), 256)

    offset_x = 0
    offset_y = 0
   
    for img in pyramid1:
	image.paste(img, (offset_x, offset_y))
        offset_x = offset_x +img.size[0]
        offset_y = 0
    image.save('imagePyramid.png','PNG')
    image.show()
    return 

def FindTemplate(pyramid, template, threshold):

    finalWidth= 15
    downsampleScale=template.size[0]/finalWidth 
    finalHeight=template.size[1]/downsampleScale
    template = template.resize((finalWidth, finalHeight), Image.BICUBIC)
    #print template.size 
    
    img = pyramid[0].convert('RGB')
    
    print 'the length of the pyramid'
    print len(pyramid) 
    for image in pyramid:
	NCC=ncc.normxcorr2D(image, template)
	print 'NCC value'
	print NCC
        aboveThresh=np.where(NCC > threshold)
        print 'the points above threshold'
        print aboveThresh
        xlist=aboveThresh[1]
        ylist=aboveThresh[0]
        print xlist
        print ylist
        ptx1=template.size[0]/2
        pty1=template.size[1]/2
        print len(xlist)
        for i in range(len(xlist)):
			x1=xlist[i]-ptx1
			y1=ylist[i]-pty1
			x2=xlist[i]+ptx1
			y2=ylist[i]+pty1
			print x1,x2,y1,y2
			draw=ImageDraw.Draw(img)
			draw.rectangle((x1,y1,x2,y2),outline="red")
			#del draw
	img.save('result.png','PNG')
	
	return img


def run():
    
	#images=['faces/judybats.jpg','faces/students.jpg','faces/tree.jpg']
	#images=['faces/judybats.jpg']
	images=['faces/students.jpg']
	#images=['faces/tree.jpg']
	for image in images:
		img = Image.open(image)
        	img = img.convert('L')
    

        	pyramid = MakePyramid(img,20)
        	ShowPyramid(pyramid)

                templateName = 'faces/template.jpg'
        	template = Image.open(templateName)
                template = template.convert('L')

      

       	 	threshold =0.51
        	result =FindTemplate(pyramid,template, threshold)
        	result.show()
    	return


run()

   
