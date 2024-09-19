import math
import pygame
from pygame.locals import *
import os


base_dir = os.path.dirname(os.path.abspath(__file__))

width = 800    
height = width
screen = pygame.display.set_mode((width, height))
pygame.font.init()
bgColor = 'black'
frameRate = 60

radarWidth = width
radarEdgeDist = 40
radarRadius = radarWidth // 2 - radarEdgeDist

lineLen = radarRadius
lineColor = 'red'
lineRotationSpeed = 120 # Degree per second
lineWidth = 3
lineTrailAlpha = 100

noOfCircles = 1
distBwCircles = radarRadius / noOfCircles
circleWidth = 5
circleColor = 'green'

blipDistanceCenter = radarRadius * (2 / 3)
fade_duration = 2000  # milliseconds
blink_speed = 1.6
redDotImagePath = os.path.join(base_dir, "assets/images/reddot1.png")

# Sound
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
BulletSoundPath = os.path.join(base_dir, "assets/sounds/shot1.mp3")
BulletSound = pygame.mixer.Sound(BulletSoundPath)
micDetectPingPath = os.path.join(base_dir, "assets/sounds/ping2.mp3")
micDetectPing = pygame.mixer.Sound(micDetectPingPath)
BlipSoundPath = os.path.join(base_dir, "assets/sounds/ping3loud.mp3") 
BlipSound = pygame.mixer.Sound(BlipSoundPath)
BlipSound.set_volume(1)