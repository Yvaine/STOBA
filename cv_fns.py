#!/usr/bin/python

import numpy as np

import math
import time
import cv2

import drone_ctrl
from drone_ctrl import drone as drn

import droneapi.lib
from droneapi.lib import VehicleMode, Location, Attitude

import position_vector
from position_vector import PositionVector

import os, os.path

from pymavlink import mavutil


class CVfns(object):

	def __init__(self):

		#define camera
		self.camera_width 		= 640
		self.camera_height 		= 480
		
		# calculating the field of vision of the camera (the higher the field of vision, more of the image fits in the HUD)
		self.camera_vfov 		= 12.42 
		self.camera_hfov 		= 12.42
		self.camera_fov 		= math.sqrt(self.camera_vfov**2 + self.camera_hfov**2)

		# background
		self.backgroundColor = (114,78,109)

	def rotate_target(self,sim,angle):
		#apply rotation matrix here
		(h, w) = (sim.shape[1],sim.shape[0])
		center = (h/2,w/2)
		rotM   = cv2.getRotationMatrix2D(center, angle, 1.0)
		rotimg = cv2.warpAffine(sim, rotM, (self.camera_width,self.camera_height),borderValue=self.backgroundColor)

		return rotimg


	#shift the point to the center of the image
	def shift_to_image(self,pt):
		return ((pt[0] + self.camera_width/2),(pt[1] + self.camera_height/2))

	#visualize_target - simulate the target image given the camera position[cX,cY,cZ](pixels) and camera orientation
	
	def visualize_target(self,target,cX, cY, img_width, img_height,relative_dist):

		#point maps
		corners = np.float32([[-img_width/2,img_height/2],[img_width/2 ,img_height/2],[-img_width/2,-img_height/2],[img_width/2, -img_height/2]])
		newCorners = np.float32([[0,0],[0,0],[0,0],[0,0]])


		#calculate projection for four corners of image
		for i in range(0,len(corners)):

			#shift to world
			x = corners[i][0] + cX - img_width/2.0
			y = corners[i][1] + cY - img_height/2.0


			#calculate perspective
			x , y  = (x/relative_dist, y/relative_dist)

			#shift to camera
			x , y = self.shift_to_image((x,y))
			newCorners[i] = x,y  
		
		#project image
		M 		= cv2.getPerspectiveTransform(corners,newCorners)
		sim 	= cv2.warpPerspective(target,M,(self.camera_width,self.camera_height),borderValue=self.backgroundColor)
		# get the roll angle from the drone in order to rotate the image
		roll	= drn.get_attitude().roll
		# caluclating the roll angle, convert it from radians to degrees
		rotimg 	= self.rotate_target(sim,-roll*(180/3.14))

		return rotimg


	def get_frame(self,target,cX,cY,aZ):
		
		# get image diemensions
		self.target = target
		img_width =   self.target.shape[1]
		img_height =  self.target.shape[0]

		# calc pixels per meter
		pixels_per_meterX 	= img_width
		pixels_per_meterY 	= img_height
		
		# scales up camera center
		cX = cX * pixels_per_meterX
		cY = cY * pixels_per_meterY
		cZ = 1
		
		#ensure that the relative distance between the camera and the target is legal
		T = (aZ-cZ)
		if(T<=0): 
			T = 1.0 
		relative_dist = T 

		# calculate field of view and relative distance
		eZ = 1.0/math.tan(math.radians(self.camera_fov)/2.0)
		relative_dist = relative_dist/eZ

		frame = self.visualize_target(target,cX, cY, img_width, img_height, relative_dist)

		return frame


cvfunc = CVfns()

if __name__ == "__builtin__":

###################################################################
###########################MODULE TESTING##########################

	drn.connect(local_connect())	
	# THE VIDEO MODULE
	drn.run()
	camera_constX=0.02
	camera_constY=0.39
	zoom = 4.0
	target = cv2.imread('/home/ardupilot/droneapi-python/example/my_app/stereo/1left.png')
	frame = cvfunc.get_frame(target,camera_constX,camera_constY,zoom)
	cv2.imshow('frame',frame)
	cv2.waitKey(1)

	while 1:
		frame = cvfunc.get_frame(target,camera_constX,camera_constY,zoom)
		cv2.imshow('frame',frame)
		zoom = zoom-0.1
		cv2.waitKey(1)
		time.sleep(0.5)

###################################################################
###################################################################