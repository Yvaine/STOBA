#!/usr/bin/python
import sys
import os, os.path
import time
from datetime import datetime


import logging
import logging.config



class aLog(object):

	def __init__(self):
		# log to the console
		self.log = logging.getLogger('quad')
		self.log.propagate = False
		self.log.setLevel(logging.DEBUG)
		formatter = logging.Formatter('[%(levelname)s]: %(message)s')
		handler_stream = logging.StreamHandler()
		handler_stream.setFormatter(formatter)
		handler_stream.setLevel(logging.DEBUG)
		self.log.addHandler(handler_stream)

		# log to a file
		log_path = "/home/ardupilot/droneapi-python/example/my_app/logs/"
		flname = log_path + "quad-%s.log"%datetime.now().strftime('%Y-%m-%d-%I:%M:%S')
		formatter = logging.Formatter('[LOG]: %(message)s')
		handler_file = logging.FileHandler(flname)
		handler_file.setFormatter(formatter)
		handler_file.setLevel(logging.INFO)
		self.log.addHandler(handler_file)

###################################################################
##########################MODULE TESTING###########################

	def fly(self):
		self.log.debug('Alltems operational')
		self.log.info('Airspeed knots')
		self.log.warn('Lowfuel')
		self.log.error('Nol. Trying to glide.')
		self.log.critical('Glide attempt failed. About to crash.')

###################################################################
###################################################################

alogger = aLog()


if __name__ == "__main__":

###################################################################
##########################MODULE TESTING###########################
	alogger.fly()
###################################################################
###################################################################