#!/usr/bin/python

import os, os.path
import time

import a_logger
from a_logger import alogger as alog

from pymavlink import mavutil
import droneapi.lib
from droneapi.lib import VehicleMode, Location


class Drone(object):
    def __init__(self):
        self.api = None
        self.gps_lock = False
        self.altitude = 30.0
        self.vehicle = None
        self.locationB = None

    def connect(self, api, home_coords=[0.0,0.0]):
        
        self.api = api

        # if we succesfully connect
        if not self.api is None:
            # get our vehicle (we assume the user is trying to control the first vehicle attached to the GCS)
            self.vehicle = self.api.get_vehicles()[0]
            self.commands = self.vehicle.commands
            self.current_coords = []
            self.home_coords = home_coords

            self.vehicle.add_attribute_observer('location', self.location_callback)    

            alog.log.debug("Waiting for GPS Lock")            
            self.gps_lock = True        

            return

    def takeoff(self):
        alog.log.debug("Taking off")
        self.commands.takeoff(30.0)
        self.vehicle.flush()

    def arm(self, toggle=True):
        if toggle:
            alog.log.debug("Arming")
        else:
            alog.log.debug("Disarming")
        self.vehicle.armed = True
        self.vehicle.flush()

    def change_mode(self, mode):
        alog.log.info("Mode: {0}".format(mode))

        self.vehicle.mode = VehicleMode(mode)
        self.vehicle.flush()

    def goto(self, location, alti, relative=None):
        alog.log.info("Goto: {0}, {1}".format(location, alti))
        #save heading location.
        self.locationB = Location(
                float(location[0]), float(location[1]),
                float(alti),
                is_relative=relative
            )

        self.commands.goto(
            Location(
                float(location[0]), float(location[1]),
                float(alti),
                is_relative=relative
            )
        )
        self.vehicle.flush()

    def get_location(self):
        return self.vehicle.location

    def get_attitude(self):
        return self.vehicle.attitude

    def location_callback(self, location):
        location = self.vehicle.location

        if location.alt is not None:
            self.altitude = location.alt

        self.current_location = location
    

    def mode_callback(self, mode):
        alog.log.info("Mode: {0}".format(self.vehicle.mode))


    # controlling_vehicle - return true if we have control of the vehicle
    def controlling_vehicle(self):
            if self.api is None:
                return False                     
            else:
                return True

    #get_mode - get current mode of vehicle
    def get_mode(self):
        return self.vehicle.mode.name

    #obstacle avoidance function
    def left_drift(self,mag):
        alog.log.debug("Obstacle avoidance activated.")
        alog.log.debug("Going left.")
        self.change_mode('STABILIZE')
        self.vehicle.channel_override = {2: 1900}
        self.vehicle.channel_override = {3: 1700}
        time.sleep(1)
        self.vehicle.channel_override = {2: 1500}
        time.sleep(0.1)
        self.vehicle.channel_override = {3: 1700}
        time.sleep(2)
        self.vehicle.channel_override = {1: 1200}
        time.sleep(mag)
        self.vehicle.channel_override = {1: 1500}
        self.vehicle.channel_override = {3: 1500}
        time.sleep(1)
        return

    #obstacle avoidance function
    def right_drift(self,mag):
        alog.log.debug("Obstacle avoidance activated.") 
        alog.log.debug("Going right.")
        self.change_mode('STABILIZE')
        self.vehicle.channel_override = {2: 1900}
        self.vehicle.channel_override = {3: 1700}
        time.sleep(1)
        self.vehicle.channel_override = {2: 1500}
        time.sleep(0.1)
        self.vehicle.channel_override = {3: 1700}
        time.sleep(2)
        self.vehicle.channel_override = {1: 1800}
        time.sleep(mag)
        self.vehicle.channel_override = {1: 1500}
        self.vehicle.channel_override = {3: 1500}
        time.sleep(1)
        return

    #obstacle avoidance function
    def top_drift(self,mag):
        alog.log.debug("Obstacle avoidance activated.") 
        alog.log.debug("Going up.")
        self.change_mode('STABILIZE')
        self.vehicle.channel_override = {2: 1900}
        self.vehicle.channel_override = {3: 1700}
        time.sleep(1)
        self.vehicle.channel_override = {2: 1500}
        time.sleep(0.1)
        self.vehicle.channel_override = {3: 1700}
        time.sleep(4)
        self.vehicle.channel_override = {3: 1500}
        time.sleep(0.3)
        return
    

    def run(self):

        if (self.vehicle.mode.name == 'GUIDED'):
            return        

        #if the vehicle veers off course, land and get back on track
        if(self.vehicle.mode.name != 'STABILIZE'):
            self.change_mode('LAND')
            while (self.altitude != float(0.0)):
                pass

       
        self.change_mode('STABILIZE')
        self.arm()
        alog.log.info("ARMED!!!")
        self.vehicle.channel_override = {3: 1500}
        time.sleep(15)
        self.change_mode('GUIDED')
        alog.log.info("Initial run sequence started, rising to target altitude")
        time.sleep(3)
        self.takeoff()
        time.sleep(5)
        alog.log.info("Takeoff complete")
        msg = "Current Altitude: " + format(self.altitude)
        alog.log.info(msg)
        self.goto([33.778679, -84.3960606],30)
        time.sleep(10)
        alog.log.info("Mode: {0}".format(drone.get_mode()))
        time.sleep(1)
        
    def resume(self):
        self.change_mode('GUIDED')
        self.goto([33.778679, -84.3960606],30)
        alog.log.info("Resuming flight to reach target")

drone = Drone()

if __name__ == "__builtin__":

###################################################################
##########################MODULE TESTING###########################

    drone.connect(local_connect())
    drone.run()
    alog.log.debug("Obstacle detected.")   
    drone.left_drift(2)
    drone.resume()
    alog.log.debug("Obstacle detected.")
    drone.right_drift(2)
    drone.resume()

###################################################################
###################################################################