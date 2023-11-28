#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import time

class ALCalin(object):
    def __init__(self, session):
        self.session = session

    def withconsent(self):
        audio_player_service = self.session.service("ALAudioPlayer")
        fileId = audio_player_service.loadFile("/data/home/nao/.local/share/PackageManager/apps/ROBOWSE/sounds/love.wav")
        audio_player_service.play(fileId, _async=True)

    def running(self):
        self.calin()

    def jul(self):
        audio_player_service = self.session.service("ALAudioPlayer")
        fileId = audio_player_service.loadFile("/data/home/nao/.local/share/PackageManager/apps/ROBOWSE/sounds/tchikita.wav")
        audio_player_service.play(fileId, _async=True)

    def TTS(self, text):
        tts = self.session.service("ALTextToSpeech")
        tts.setLanguage("French")
        tts.setParameter("doubleVoice", 1)
        tts.setParameter("doubleVoiceLevel", 0.5)
        tts.setParameter("doubleVoiceTimeShift", 0.1)
        tts.setParameter("pitchShift", 1.1)
        phrase = text
        tts.say(phrase)

    def calin(self):
        self.TTS("Viens me faire un calin \\pau=500\\\\vct=50\\\\rspd=50\\bébou")

        motion_service = self.session.service("ALMotion")

        # Bras gauche
        left_shoulder_pitch = 0.5
        left_shoulder_roll = 0.0
        left_elbow_yaw = -1.5
        left_elbow_roll = -1.0
        left_wrist_yaw = 0.0

        # Bras droit
        right_shoulder_pitch = 0.5
        right_shoulder_roll = 0.0
        right_elbow_yaw = 1.5
        right_elbow_roll = 1.0
        right_wrist_yaw = 0.0

        # Appliquer les angles
        motion_service.setAngles(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"], 
                                [left_shoulder_pitch, left_shoulder_roll, left_elbow_yaw, left_elbow_roll, left_wrist_yaw], 
                                0.2)
        motion_service.setAngles(["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"], 
                                [right_shoulder_pitch, right_shoulder_roll, right_elbow_yaw, right_elbow_roll, right_wrist_yaw], 
                                0.2)

    def braquage(self):

        # Définir les angles de cible pour les articulations
        # Les angles sont en radians

        motion_service = self.session.service("ALMotion")

        # Définir les angles pour le bras droit
        # Bras tendu, paume vers la gauche
        right_shoulder_pitch = 0.0  # Épaule verticale
        right_shoulder_roll = 0.0   # Épaule horizontale
        right_elbow_yaw = -1.57     # Rotation du coude pour tourner la paume
        right_elbow_roll = 0.0      # Coude
        right_wrist_yaw = -1.57     # Poignet, pour tourner la paume vers la gauche

        # Définir les angles pour le bras gauche
        # Bras plié avec le poing fermé sous le coude droit
        left_shoulder_pitch = 0.0
        left_shoulder_roll = 0.0
        left_elbow_yaw = 0          # Rotation du coude
        left_elbow_roll = 0    # -1.57 Coude plié à 90 degrés
        left_wrist_yaw = -1.57      # Poignet

        # Appliquer les angles
        motion_service.setAngles(["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"], 
                                [right_shoulder_pitch, right_shoulder_roll, right_elbow_yaw, right_elbow_roll, right_wrist_yaw], 
                                0.2)
        motion_service.setAngles(["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"], 
                                [left_shoulder_pitch, left_shoulder_roll, left_elbow_yaw, left_elbow_roll, left_wrist_yaw], 
                                0.2)
        
        
        time.sleep(5)

        # Serrer la main droite
        motion_service.closeHand('LHand')

        # Temps pendant lequel la main doit rester serrée (en secondes)
        duration = 10
        start_time = time.time()

        # Boucle pour maintenir la main fermée
        while time.time() - start_time < duration:
            motion_service.closeHand('RHand')
            time.sleep(0.2)  # Petite pause pour éviter une utilisation excessive du processeur

        time.sleep(1)

        # Déplacer le robot de 1 mètre vers l'avant
        x = 0.0  # distance en mètres dans la direction avant (x)
        y = 0.0  # distance en mètres dans la direction latérale (y)
        theta = 0.0  # rotation en radians

        motion_service.moveTo(x, y, theta)

        audio_player_service = self.session.service("ALAudioPlayer")
        fileId = audio_player_service.loadFile("/data/home/nao/.local/share/PackageManager/apps/ROBOWSE/sounds/gun.wav")
        audio_player_service.play(fileId, _async=True)

        time.sleep(10)