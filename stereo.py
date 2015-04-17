#!/usr/bin/python

import os, os.path
import cv2

import numpy as np
import time
from matplotlib import pyplot as plt


class stereoCl(object):		


	def reSizeL (self,imgL):
		r =  1024.0 / imgL.shape[1]
		dim = (1024, int(imgL.shape[0] * r))
		 
		# perform the actual resizing of the imgR and show it
		reszdL = cv2.resize(imgL, dim, interpolation = cv2.INTER_AREA)
		return reszdL

	def reSizeR (self,imgR):
		r = 1024.0 / imgR.shape[1]
		dim = (1024, int(imgR.shape[0] * r))
		 
		# perform the actual resizing of the imgRgR and show it
		reszdR = cv2.resize(imgR, dim, interpolation = cv2.INTER_AREA)
		return reszdR


	def createDisparity(self,no,path):
		fl1 = path + str(no) + "left.png"
		fl2 = path + str(no) + "right.png"

		#opencv switches left and right images for some reason
		imgR = cv2.imread(fl1,0)
		imgL = cv2.imread(fl2,0)

		resizedR = self.reSizeR(imgR)
		resizedL = self.reSizeL(imgL)

		blurR = cv2.GaussianBlur(resizedR,(5,5),0)
		blurL = cv2.GaussianBlur(resizedL,(5,5),0)

		stereo = cv2.StereoSGBM(0,48,9,0,8*9*9,32*9*9,63,7,0,8,False)

		disparity = stereo.compute(blurR, blurL)

		im = np.array(disparity, dtype = np.uint8)
		name = path + "disp" + str(no) + ".png"
		cv2.imwrite(name,im)


	def colorFinder(self,no,path):

		name = path + "disp" + str(no) + ".png"
		im = cv2.imread(name)

		lower = np.array([0, 0, 0], dtype = "uint8")
		upper = np.array([100, 100, 100], dtype = "uint8")

		# find the colors within the specified boundaries and apply
		# the mask
		mask = cv2.inRange(im, lower, upper)
		output = cv2.bitwise_and(im, im, mask = mask)


		r = 512.0 / im.shape[1]
		dim = (512, int(im.shape[0] * r))
		 
		# perform the actual resizing of the imgR and show it
		resizedL = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)

		r = 512.0 / output.shape[1]
		dim = (512, int(output.shape[0] * r))
		 
		# perform the actual resizing of the imgR and show it
		resizedop = cv2.resize(output, dim, interpolation = cv2.INTER_AREA)

		name = path + "thresh" + str(no) + ".png"
		cv2.imwrite(name,resizedop)


	def compHist(self,no,path):

		name = path + "thresh" + str(no) + ".png"
		img = cv2.imread(name)
		im = np.array(img, dtype = np.uint8)

		#to move a mask all over the image

		#store distance values obtained by the image
		store     = []

		for i in range(0,3):
			for j in range(0,3):
				
				im_slice=im[i*51:(i+1)*51,j*171:(j+1)*171]

				mask = np.zeros((51, 171, 1),np.uint8)
				
				mask[:] = (0) 

				mask_path = path + "mask.png"

				cv2.imwrite(mask_path, mask)

				rmask = cv2.imread(mask_path)
				rmaski = np.array(rmask, dtype = np.uint8)

				#calucalte the histogram of the thresholded disparity map and compare it with the mask
				hist1 = cv2.calcHist([im_slice],[0],None,[256],[0,256])
				hist1 = cv2.normalize(hist1).flatten()

				hist2 = cv2.calcHist([rmaski],[0],None,[256],[0,256])
				hist2 = cv2.normalize(hist2).flatten()

				d=cv2.compareHist(hist1, hist2, cv2.cv.CV_COMP_BHATTACHARYYA)
				store.append(d)

		#pick the farthest bhattacharyya distance from black (i.e all the grey areas)
		store = [x*10 for x in store]

		max_d 		= max(store)
		max_d_index = store.index(max(store))

		#an array with all the circle centers of the nine segments
		circle_centers = [(86,25),(256,25),(342,25),(86,76),(256,76),(342,76),(86,128),(256,128),(342,128)]

		#draw a circle on the image for the selected segment to fly through
		cv2.circle(img,circle_centers[max_d_index],23,(0,0,255),2)
		name = path + "circled" + str(no) + ".png"
		cv2.imwrite(name,img)

	def run(self,path):
		for i in range(1,8):
			self.createDisparity(i,path)
			self.colorFinder(i,path)
			self.compHist(i,path)



stereofunc = stereoCl()

if __name__ == "__builtin__":
	stereofunc.run("/home/ardupilot/droneapi-python/example/my_app/stereo/")
