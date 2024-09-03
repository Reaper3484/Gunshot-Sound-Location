import pygame
from pygame.locals import *
import math

pygame.init()


radar_width = 500
radar_height = 500
radar_screen = pygame.display.set_mode((radar_width, radar_height))
radar_bgColor = 'black'
radar_center = (radar_width // 2, radar_height // 2)
radar_radius = [10, 50, 100, 150]

arrow_length =  30
arrow_color = 'red'

clock = pygame.time.Clock()
running = True
angle = 135

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    radar_screen.fill(radar_bgColor)
    for radar in radar_radius:
        pygame.draw.circle(radar_screen, 'green', radar_center, radar, 2)



    arrow_x = radar_center[0] + arrow_length * math.cos(math.radians(angle))
    arrow_y = radar_center[1] - arrow_length * math.sin(math.radians(angle))

    pygame.draw.line(radar_screen, arrow_color, radar_center, (arrow_x, arrow_y), 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()