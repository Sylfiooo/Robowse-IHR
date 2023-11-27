#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
from math import pi
import signal

class SimpleMove(object):
    """
    A Simple class to test body and base movements.
    """

    def turn(self, angle):
        """
        Robot turn with an angle in degrees

        /!\ THE CHARGING FLAP MUST BE CLOSED to allow the robot base to move /!\ 

        """        
        self._motion.moveTo(0, 0, angle*pi/180 )
        

def hand_hello(motion_service):
    """
    Waves right hand to say hello
    """  

    names = ["RShoulderPitch","RShoulderRoll","RElbowRoll","RElbowYaw","RWristYaw"]
    name_hand="RHand"
    name_stiffness = ["RArm"]
    angles0 = [88 *pi/180, 0 *pi/180, 0 *pi/180, 20 *pi/180, 0]
    angles = [-68.6 *pi/180, -35.6 *pi/180, 11.1 *pi/180, 20.7 *pi/180, 0]
    angles2 = [-68.6 *pi/180, -35.6 *pi/180, 71.1 *pi/180, 20.7 *pi/180, 0]

    times = [2.0,1.0,2.0,2.0,2.0,2.0]
    times2 = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    isAbsolute = True

    # Raise arm
    motion_service.angleInterpolation(names, angles, times, isAbsolute)

    # Wave hand
    motion_service.angleInterpolation(names, angles2, times2, isAbsolute)
    motion_service.angleInterpolation(names, angles, times2, isAbsolute)
    motion_service.angleInterpolation(names, angles2, times2, isAbsolute)
  
    # Lower arm
    motion_service.angleInterpolation(names, angles0, times, isAbsolute)

    motion_service.stiffnessInterpolation(name_stiffness, 0.8, 0.2)

def main(session):
    # Get the service ALTabletService.
    try:
        tabletService = session.service("ALTabletService")
        tabletService.loadApplication("ROBOWSE")
        tabletService.showWebview()
    except Exception, e:
        print "Error was: ", e

    # Get the service ALMotionService.
    try:
        motionService = session.service("ALMotion")
        motionService.wakeUp()
    except Exception, e:
        print "Error was: ", e
    
    # Getting the service ALDialog
    try:
    	ALDialog = session.service("ALDialog")
        ALDialog.resetAll()
    	ALDialog.setLanguage("French")

    	# Loading the topics directly as text strings
    	topic_name = ALDialog.loadTopic("/home/nao/.local/share/PackageManager/apps/ROBOWSE/dialogs/robowse_simple_fr.top")

    	# Activating the loaded topics
    	ALDialog.activateTopic(topic_name)

    	# Starting the dialog engine - we need to type an arbitrary string as the identifier
    	# We subscribe only ONCE, regardless of the number of topics we have activated
    	ALDialog.subscribe('robowsedialog')
    except Exception, e:
        print "Error was: ", e

    # Get the service ALAudioPlayer.
    try:
        audio_player_service = session.service("ALAudioPlayer")
        
        #plays a file and get the current position 5 seconds later
        fileId = audio_player_service.loadFile("/data/home/nao/.local/share/PackageManager/apps/ROBOWSE/sounds/gun.wav")
        audio_player_service.play(fileId, _async=True)

        time.sleep(3)

        #currentPos should be near 3 secs
        currentPos = audio_player_service.getCurrentPosition(fileId)
        print "The current position in file is: ", currentPos
    except Exception, e:
        print "Error was: ", e
    
    #sm = SimpleMove(session)
    hand_hello(motionService)

    try:
        raw_input("\n Press Enter when finished:")
    finally:
        # stopping the dialog engine
        ALDialog.unsubscribe('robowsedialog')

        # Deactivating the topic
        ALDialog.deactivateTopic(topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        ALDialog.unloadTopic(topic_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)