import math
import pygame
from pygame.locals import *


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

# Sound
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
BulletSound = pygame.mixer.Sound("./assets/sounds/shot1.mp3")
micDetectPing = pygame.mixer.Sound("./assets/sounds/ping2.mp3")
BlipSound = pygame.mixer.Sound("./assets/sounds/ping3loud.mp3")
BlipSound.set_volume(1)