import pygame
from pygame.locals import *
import math


pygame.init()

width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))
bgColor = 'black'
frameRate = 60

radarRadius = 400
radarCenter = (width // 2, height // 2)

lineLen = radarRadius
lineColor = 'red'
lineRotationSpeed = 180 # Degree per second

signalLineWidth = 30 # Degrees
noOfLines = 30
lineWidth = int(signalLineWidth / noOfLines) 

noOfCircles = 4
distBwCircles = radarRadius / noOfCircles
circleWidth = 5
circleColor = 'green'


class Radar:
    def __init__(self) -> None:
        self.surf = pygame.Surface((radarRadius * 2, radarRadius * 2))
        self.rect = self.surf.get_rect(center=radarCenter)
        self.lineLen = lineLen
        self.lineAngle = 0
        self.linesList = []
        self.detectedPoints = []
        self.initializeLines()

    def initializeLines(self):
        for i in range(int(noOfLines)):
            surf = pygame.Surface((radarRadius * 4, radarRadius * 4), SRCALPHA)
            surf.set_alpha(255 * (i / noOfLines))
            self.linesList.append(surf)

    def draw(self):
        for radar in [circle * distBwCircles for circle in range(1, noOfCircles + 1)]:
            pygame.draw.aacircle(screen, circleColor, radarCenter, radar, circleWidth)

        pygame.draw.line(screen, circleColor, (radarCenter[-1], radarCenter[1] + radarRadius), (radarCenter[0], radarCenter[1] - radarRadius))
        pygame.draw.line(screen, circleColor, (radarCenter[0] + radarRadius, radarCenter[1]), (radarCenter[0] - radarRadius, radarCenter[1]))
         
        for i, line in enumerate(self.linesList):
            lineX = radarCenter[0] + lineLen * math.cos(math.radians(self.lineAngle + i * lineWidth))
            lineY = radarCenter[1] + lineLen * math.sin(math.radians(self.lineAngle + i * lineWidth))

            pygame.draw.line(line, lineColor, radarCenter, (lineX, lineY), lineWidth)

            screen.blit(line, line.get_rect())
            line.fill((0, 0, 0, 0))
        

    def update(self):
        self.lineAngle += lineRotationSpeed / frameRate
        pass


radar = Radar()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bgColor)
    radar.draw()
    radar.update()

    clock.tick(frameRate)
    pygame.display.flip()

pygame.quit()