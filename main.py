#!/usr/bin/python
import os, os.path
import time

import math
import cv2
import numpy as np

import drone_ctrl
from drone_ctrl import drone as drn

import cv_fns
from cv_fns import cvfunc as CV

import a_logger
from a_logger import alogger as alog

import stereo
from stereo import stereofunc as stereofn

import vision_module
from vision_module import vm as VM

import droneapi.lib
from droneapi.lib import VehicleMode, Location, Attitude


###################################################################

###########################  STOBA  ###############################

###################################################################


if __name__ == "__builtin__":
	drn.connect(local_connect())
	#load the stereo module from path
	stereofn.run("/home/ardupilot/droneapi-python/example/my_app/stereo/")
	drn.run()
	#assign the target positions and run the avoidance mechanism
	VM.check_target1()
	VM.check_target2()
	VM.check_target3()