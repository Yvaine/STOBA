#!/usr/bin/python
import os, os.path
import time

import math
import cv2
import numpy as np

import drone_ctrl
from drone_ctrl import drone as drn

import position_vector
from position_vector import PositionVector

import cv_fns
from cv_fns import cvfunc as CV

import a_logger
from a_logger import alogger as alog

import droneapi.lib
from droneapi.lib import VehicleMode, Location, Attitude


class VModule(object):		

	def __init__(self):
		# the framerate  
		self.steps 		= 10
		self.triggered 	= False
		self.targetno	=1

	def show_frame(self,no):
		threshfile = "/home/ardupilot/droneapi-python/example/my_app/stereo/thresh" + str(no) + ".png"
		circfile = "/home/ardupilot/droneapi-python/example/my_app/stereo/circled" + str(no) + ".png"
		thresh = cv2.imread(threshfile)
		circ = cv2.imread(circfile)
		cv2.namedWindow('stereo')
		cv2.startWindowThread()	
		cv2.imshow('stereo', np.hstack((thresh,circ)))
		cv2.waitKey(1)
		return


	def location_report(self, tarloc, taralti):
		#get target and vehicle locations
		self.targetLoc = PositionVector()
		self.vehicleLoc = PositionVector()
		self.vehicleLoc.set_from_location(drn.get_location())
		
		full_loc = Location(
                float(tarloc[0]), float(tarloc[1]),
                float(taralti),
                is_relative=True
            )
		self.targetLoc.set_from_location(full_loc)
		loc = "Vehicle location: " + "X: " + format(self.vehicleLoc.x) + "Y: " + format(self.vehicleLoc.y) + "Z: " + format(self.vehicleLoc.z)
		alog.log.info(loc)

		target_loc = "Target location: " + "X: " + format(self.targetLoc.x) + "Y: " + format(self.targetLoc.y) + "Z: " + format(self.targetLoc.z)
		alog.log.info(target_loc)

		dist = self.vehicleLoc.get_distance_xyz(self.vehicleLoc,self.targetLoc)
		reld = "Relative distance: " + format(dist)
		alog.log.info(reld)
		return dist


	#load_target- load an image to simulate the target.
	def check_target1(self):	
		tarloc = [33.775497,-84.396860] #33.775497 -84.396860   33.775632 -84.396806
		taralti = 30

		#wait for trigger over here
		reld = self.location_report(tarloc,taralti)
		if not(self.triggered):
			while (int(reld)>10):
				time.sleep(2)
				reld = self.location_report(tarloc,taralti)

		target = cv2.imread('/home/ardupilot/droneapi-python/example/my_app/stereo/1left.png')
		self.load_target(target,11,0.0,0.0)

		#load_target- load an image to simulate the target.
	def check_target2(self):	
		tarloc = [33.776888,-84.396367] #33.775497 -84.396860   33.776888 -84.396367
		taralti 	  = 50
		self.targetno = 2
		#wait for trigger over here
		reld = self.location_report(tarloc,taralti)
		if not(self.triggered):
			while (int(reld)>10):
				time.sleep(2)
				reld = self.location_report(tarloc,taralti)

		target = cv2.imread('/home/ardupilot/droneapi-python/example/my_app/stereo/2left.png')
		self.load_target(target,11,0.0,0.0)

	def check_target3(self):	
		tarloc = [33.777845, -84.396523] #33.775497 -84.396860   33.776888 -84.396367	33.777845 -84.396523
		taralti 	  = 70
		self.targetno = 3
		#wait for trigger over here
		reld = self.location_report(tarloc,taralti)
		if not(self.triggered):
			while (int(reld)>10):
				time.sleep(2)
				reld = self.location_report(tarloc,taralti)

		target = cv2.imread('/home/ardupilot/droneapi-python/example/my_app/stereo/3left.png')
		self.load_target(target,11,0.0,0.0)

		


	def load_target(self,target,zoom,camera_constX,camera_constY):
		frame = CV.get_frame(target,camera_constX,camera_constY,zoom)
		self.load_window(target,frame,zoom,camera_constX,camera_constY)

		

	def load_window(self,target,frame,zoom,camera_constX,camera_constY):
		self.steps = zoom
		cv2.namedWindow('HUD')
		cv2.startWindowThread()	
		while self.steps>1.0:
			if (int(self.steps*10) == 91) and (self.targetno == 1):			#ANALYZE THE VIDEO MODULE AND GET RESULTS
				alog.log.debug("Obstacle detected.")
				drn.right_drift(2)
				drn.resume()
				self.show_frame(self.targetno)
				camera_constX=0.02
				camera_constY=0.39
			if (int(self.steps*10) == 91) and (self.targetno == 2):			#ANALYZE THE VIDEO MODULE AND GET RESULTS
				alog.log.debug("Obstacle detected.")
				drn.left_drift(6)
				drn.resume()
				self.show_frame(self.targetno)
				camera_constX=0.47
				camera_constY=0.4
			if (int(self.steps*10) == 91) and (self.targetno == 3):			#ANALYZE THE VIDEO MODULE AND GET RESULTS
				alog.log.debug("Obstacle detected.")
				drn.left_drift(2)
				drn.resume()
				self.show_frame(self.targetno)
				camera_constX=0.05
				camera_constY=0.2
			st = "Steps: " + format(self.steps)
			alog.log.debug(st)
			cv2.imshow('HUD',frame)
			cv2.waitKey(1)
			time.sleep(0.1)
			camera_constX = camera_constX
			camera_constY = camera_constY
			self.steps = self.steps - 0.1
			self.load_target(target,self.steps,camera_constX,camera_constY)

		cv2.waitKey(3)
		cv2.destroyAllWindows()
		cv2.waitKey(1)
		alog.log.info("Exiting vision threads")


vm = VModule()
	
if __name__ == "__builtin__":

###################################################################
##########################MODULE TESTING###########################

	drn.connect(local_connect())	
	# THE VIDEO MODULE
	drn.run()
	vm.check_target1()
	vm.check_target2()
	vm.check_target3()
	# time.sleep(3)
	# vm.load_target('/home/ardupilot/droneapi-python/example/my_app/target.jpg',15,0.0)

###################################################################
###################################################################