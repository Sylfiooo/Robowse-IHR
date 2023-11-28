#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import math
import time
from math import pi
import signal
from services.alcalin import ALCalin
from services.alfood import ALFood

pi = math.pi

def wake_up(motion_service):
    # Activer les moteurs
    motion_service.wakeUp()

    # Désactiver le mode de repos automatique
    motion_service.setBreathEnabled('Body', False)
    motion_service.setIdlePostureEnabled('Body', False)

def go_sleep(motion_service):
    # Réactiver le mode de repos automatique
    motion_service.setBreathEnabled('Body', True)
    motion_service.setIdlePostureEnabled('Body', True)

    # Mettre le robot en mode repos
    motion_service.rest()        

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
     # Création et enregistrement des services
    calin_serv = ALCalin(session)
    calin_serv_id = session.registerService("ALCalin", calin_serv)
    food_serv = ALFood(session)
    food_serv_id = session.registerService("ALFood", food_serv)
    
    # Get the service ALTabletService.
    try:
        tabletService = session.service("ALTabletService")
        tabletService.loadApplication("ROBOWSE")
        tabletService.showWebview()
    except Exception as e:
        print "Error was: ", e

    # Get the service ALMotionService.
    try:
        motionService = session.service("ALMotion")
        motionService.wakeUp()
    except Exception as e:
        print 'Error was: ', e
    
    # Getting the service ALDialog
    try:
    	ALDialog = session.service("ALDialog")
        ALDialog.resetAll()
        ALDialog.setLanguage("French")

    	# Loading the topics directly as text strings
    	topic_name_start = ALDialog.loadTopic("/home/nao/.local/share/PackageManager/apps/ROBOWSE/dialogs/robowse_start_fr.top")
        ALDialog.activateTopic(topic_name_start)
        ALDialog.subscribe('robowsedialog')
    except Exception as e:
        print "Error was: ", e

    # Get the service ALAudioPlayer.
    try:
        audio_player_service = session.service("ALAudioPlayer")
        
        #plays a file and get the current position 5 seconds later
        #fileId = audio_player_service.loadFile("/data/home/nao/.local/share/PackageManager/apps/ROBOWSE/sounds/gun.wav")
        #audio_player_service.play(fileId, _async=True)

        #time.sleep(3)

        #currentPos should be near 3 secs
        #currentPos = audio_player_service.getCurrentPosition(fileId)
        #print "The current position in file is: ", currentPos
    except Exception as e:
        print "Error was: ", e

    # Get the service ALCalin.
    try:
        calin_serv = session.service("ALCalin")
    except Exception as e:
        print "Error was: ", e

    # Get the service ALCalin.
    try:
        food_serv = session.service("ALFood")
    except Exception as e:
        print "Error was: ", e

    calin_serv.TTS("Clique pour commencer, ou dis 'C\'est parti !'")
    hand_hello(motionService)

    try:
        raw_input("\n Press Enter when finished:")
    finally:
        # stopping the dialog engine
        ALDialog.unsubscribe('robowsedialog')

        # Deactivating the topic
        ALDialog.deactivateTopic(topic_name_start)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        ALDialog.unloadTopic(topic_name_start)

        session.unregisterService(calin_serv_id)
        session.unregisterService(food_serv_id)

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