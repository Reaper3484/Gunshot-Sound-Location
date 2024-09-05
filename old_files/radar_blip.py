import pygame
from pygame.locals import *
import math

# Load and scale the red dot image
redDot = pygame.image.load("./assets/images/reddot1.png")
redDot = pygame.transform.scale(redDot, (50, 50))

pygame.init()

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
bgColor = 'black'
frameRate = 60

radarCenter = (width // 2, height // 2)

angle = math.radians(280)
radius = 50

# Calculate the position of the red dot relative to the radar center
dotX = radarCenter[0] + radius * math.cos(angle)
dotY = radarCenter[1] + radius * math.sin(angle)

redDot_rect = redDot.get_rect(center=(dotX, dotY))

radarRadius = 400
radarCenter = (width // 2, height // 2)

lineLen = radarRadius
lineColor = 'red'
lineRotationSpeed = 180  # Degree per second

signalLineWidth = 20  # Degrees
noOfLines = 10
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
            pygame.draw.circle(screen, circleColor, radarCenter, radar, circleWidth)

        pygame.draw.line(screen, circleColor, (radarCenter[0], radarCenter[1] + radarRadius), (radarCenter[0], radarCenter[1] - radarRadius))
        pygame.draw.line(screen, circleColor, (radarCenter[0] + radarRadius, radarCenter[1]), (radarCenter[0] - radarRadius, radarCenter[1]))

        for i, line in enumerate(self.linesList):
            lineX = radarCenter[0] + lineLen * math.cos(math.radians(self.lineAngle + i * lineWidth))
            lineY = radarCenter[1] + lineLen * math.sin(math.radians(self.lineAngle + i * lineWidth))

            pygame.draw.line(line, lineColor, radarCenter, (lineX, lineY), lineWidth)

            screen.blit(line, line.get_rect())
            line.fill((0, 0, 0, 0))

    def update(self):
        self.lineAngle += lineRotationSpeed / frameRate


radar = Radar()

# Blinking settings
fade_duration = 5000  # 3 seconds in milliseconds
blink_timer = pygame.time.get_ticks()  # Initialize the blink timer
blink_speed = 7

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(bgColor)
    radar.draw()

    # Calculate the elapsed time since the blinking started
    elapsed_time = current_time - blink_timer

    if elapsed_time < fade_duration:
        # Calculate the alpha value based on elapsed time (fade in and fade out)
        alpha = abs(math.sin(math.pi * blink_speed*(elapsed_time / fade_duration))) * 255
        redDot.set_alpha(alpha)

        # Draw the red dot with the current alpha value
        screen.blit(redDot, redDot_rect)

    radar.update()

    clock.tick(frameRate)
    pygame.display.flip()

pygame.quit()
