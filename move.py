#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

__author__      = "Raphael Leber"
__license__     = """
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
<raphael.leber@cpe.fr> wrote this file.  As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return.   Raphael Leber
----------------------------------------------------------------------------
"""


"""Example: A Simple class to test body and base movements"""

import qi
import time
import sys
import argparse
from math import pi
import audio

class SimpleMove(object):
    """
    A Simple class to test body and base movements.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(SimpleMove, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMotion.
        self._motion = session.service("ALMotion")
        self.life_service = session.service("ALAutonomousLife")
        self.life_service.setAutonomousAbilityEnabled("BackgroundMovement",True)

    # def turn(self, angle):
    #     """
    #     Robot turn with an angle in degrees

    #     /!\ THE CHARGING FLAP MUST BE CLOSED to allow the robot base to move /!\ 

    #     """        
    #     self._motion.moveTo(0, 0, angle*pi/180 )



    def hand_hello(self):
        """
        Waves right hand to say hello
        """  

        names = ["RShoulderPitch","RShoulderRoll","RElbowRoll","RElbowYaw","RWristYaw"]
        name_stiffness = ["RArm"]
        angles0 = [88 *pi/180, 0 *pi/180, 0 *pi/180, 20 *pi/180, 0]
        angles = [-15 *pi/180, 0 *pi/180, 0 *pi/180, 0 *pi/180, 90*pi/180]
     

        times = [2.0,1.0,2.0,2.0,2.0,2.0]
 
        isAbsolute = True

        # Motors ready to be moved
        self._motion.wakeUp()

        # Raise arm
        self._motion.angleInterpolation(names, angles, times, isAbsolute)
        audio.main(session)

        # Lower arm
        #self._motion.angleInterpolation(names, angles0, times, isAbsolute)

        # self._motion.stiffnessInterpolation(name_stiffness, 0.8, 0.2)


    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting SimpleMove"

        # self.turn(30)
        # self.turn(-60)
        # self.turn(30)
        self.hand_hello()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user"
            #stop
            sys.exit(0)        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["MoveDemo", "--qi-url=" + connection_url])
        session = qi.Session()
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    
