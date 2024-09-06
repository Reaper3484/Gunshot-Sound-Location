import math
import pygame
from pygame.locals import *


width = 1900    
height = width // 2
screen = pygame.display.set_mode((width, height))
bgColor = 'black'
frameRate = 60

simWidth = width * (2 / 3)
radarWidth = width / 3

# Detection System
noOfMics = 4
micRadius = 7
micIdleColor = 'grey'
micDetectedColor = 'green'

micArrayRadius = 50
micArrayWidth = 3
micArrayCenter = (simWidth // 2, height // 2)
arrayColor = 'light grey'

sourcePos = (500, 0)
sourceColor = 'red'
sourceSize = (10, 10)

soundWaveColor = ('white')
soundWaveWidth = 10
soundWaveSpeed = 5
updateRate = 10

soundSpeed = 343

# Radar 
radarRadius = radarWidth // 2 - 20

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
fade_duration = 8000  # milliseconds
blink_speed = 1.6

# Sound
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
BulletSound = pygame.mixer.Sound("./assets/sounds/shot1.mp3")
micDetectPing = pygame.mixer.Sound("./assets/sounds/ping2.mp3")
BlipSound = pygame.mixer.Sound("./assets/sounds/ping3loud.mp3")
BlipSound.set_volume(1)