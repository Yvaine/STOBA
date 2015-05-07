# STOBA 
A stereo based obstacle avoidance system for drones using the ArduPilot SITL.

## Installation
First, install ArduPilot SITL on linux.
Follow these steps: http://dev.ardupilot.com/wiki/simulation-2/sitl-simulator-software-in-the-loop/setting-up-sitl-on-linux/

Next, install dronekit-python from source.
Follow the instructions mentioned on their website: http://python.dronekit.io/getting_started.html

Next, download this entire repository and paste it in ../path-to-dronekit/examples/my_app/

Before starting the simulator to run the api make sure you load the params from the copter params by running this script, 
in the ArduCopter directory inside ardupilot:

/path-to-ardupilot/ardupilot/Tools/autotest/./sim_vehicle.sh -w

Next, create a start script for ardupilot, "start.sh" in the ArduCopter folder, with the following:

--------------------------------script---------------------------------------------

export PATH=$PATH:/home/ardupilot/droneapi-python/example/my_app

export PYTHONPATH=$PYTHONPATH:/home/ardupilot/droneapi-python/example/my_app

/path-to-ardupilot/ardupilot/Tools/autotest/./sim_vehicle.sh -L Gatech --console --map --aircraft test

-------------------------------eoscript---------------------------------------------

You can set a location for simulation using locations.txt in the autotest folder in ArduPilot. 
You can see that the -L option is used to do this, as shown above.

Start the Ardupilot SITL simulator and run the api using the command given in apistart.txt.

Make sure you change the location of the ardupilot folder in the logger module and stereo module.
