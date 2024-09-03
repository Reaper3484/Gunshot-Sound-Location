import pygame
from pygame.locals import *
import math


pygame.init()

width = 1000
height = 1000
screen = pygame.display.set_mode((width, height), SRCALPHA)
bgColor = 'white'

noOfMics = 4
micRadius = 5
micIdleColor = 'grey'
micDetectedColor = 'green'

micArrayRadius = 10
micArrayWidth = 10
micArrayCenter = (width // 2, height // 2)
arrayColor = 'light grey'

sourcePos = (500, 0)
sourceColor = 'red'
sourceSize = (10, 10)

soundWaveColor = (100, 0, 0)
soundWaveWidth = 10
soundWaveSpeed = 5
updateRate = 10

soundSpeed = 343


class DetectionSystem():
    def __init__(self) -> None:
        pass


class Mic():
    allMicsDetected = 0
    angleCalculated = False
    def __init__(self, position) -> None:
        self.surf = pygame.Surface((micRadius * 2, micRadius * 2))
        self.rect = self.surf.get_rect(center=(micArrayCenter[0] + position[0], micArrayCenter[1]  + position[1]))
        self.color = micIdleColor
        self.timeStamp = 0        
        self.intensity = 0
        self.frequency = 0
        self.position = position

    def checkCollision(self, source):
        for wave in source.soundWaves:
            center = wave['center']
            distance = math.sqrt((self.rect.centerx - center[0]) ** 2 + (self.rect.centery - center[1]) ** 2)
            if distance <= wave['radius']:
                if self.timeStamp == 0:
                    self.timeStamp = distance / soundSpeed
                    self.color = micDetectedColor
                    print(f"Mic at {self.position} detected collision at {self.timeStamp} ms")
                    Mic.allMicsDetected += 1

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, micRadius)

    def update(self, source):
        self.checkCollision(source)


class Source():
    def __init__(self, position) -> None:
        self.surf = pygame.Surface(sourceSize)
        self.rect = self.surf.get_rect(center=position)
        self.color = sourceColor
        self.soundWaveColor = soundWaveColor    
        self.radius = 10
        self.last_update_time = pygame.time.get_ticks()
        self.soundWaves = []
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

        for wave in self.soundWaves:
            pygame.draw.circle(wave['surf'], self.soundWaveColor, wave['center'], wave['radius'], soundWaveWidth)
            screen.blit(wave['surf'], (0, 0))

    def sendSoundWave(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_update_time >= updateRate:
            for wave in self.soundWaves.copy():    
                wave['radius'] += soundWaveSpeed
                if wave['radius'] > max(width, height):
                    self.soundWaves.remove(wave)
                    continue

                opacity = (wave['radius'] / wave['edgeDistance']) * 255 
                wave['surf'].set_alpha(255 - opacity)
                
            self.last_update_time = curr_time

    def fireShot(self):
        surf = pygame.Surface((width, height), SRCALPHA)
        x, y = self.rect.center
        bottom = height - y
        top = y
        left = x
        right = width - x
        edgeDistance = max(bottom, top, left, right)
        self.soundWaves.append({
            'surf': surf,
            'edgeDistance': edgeDistance,
            'center': self.rect.center,
            'radius': 0
        })

    def update(self):
        self.sendSoundWave()
        if Mic.allMicsDetected:
            pass


micsList = []

angleOffset = 2 * math.pi / noOfMics
angle = 0

for _ in range(noOfMics):
    x = micArrayRadius * math.cos(angle)        
    y = micArrayRadius * math.sin(angle)        
    micsList.append(Mic((x, y)))
    angle += angleOffset

source = Source(sourcePos)

        
def drawMics():
    pygame.draw.circle(screen, arrayColor, micArrayCenter, micArrayRadius + micArrayWidth // 2, micArrayWidth)
    for mic in micsList:
        mic.draw()


def updateMics(source):
    for mic in micsList:
        mic.update(source)


def calculateAngle():
    if(Mic.angleCalculated == False):
        timeDiff = micsList[1].timeStamp - micsList[3].timeStamp
        value = (timeDiff * soundSpeed) / (2*micArrayRadius)
        angle = math.degrees(math.asin(value))
        print("Angle: ", angle)
        Mic.angleCalculated =True


clock = pygame.time.Clock()
running = True
while (running):
    for ev in pygame.event.get():
        if ev.type == QUIT or ev.type == KEYDOWN and ev.key == K_ESCAPE:
            running = False

        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                Mic.allMicsDetected = 0
                source.fireShot()
        
        if ev.type == MOUSEBUTTONDOWN:
            source.rect.center = ev.pos

    screen.fill(bgColor)

    drawMics()
    updateMics(source)

    source.draw()
    source.update()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()