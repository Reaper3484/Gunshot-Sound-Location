import pygame
from pygame.locals import *
import math


pygame.init()

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
bgColor = 'white'

noOfMics = 4
micRadius = 7
micIdleColor = 'grey'
micDetectedColor = 'green'

micArrayRadius = 50
micArrayWidth = 3
micArrayCenter = (width // 2, height // 2)
arrayColor = 'light grey'

sourcePos = (250, 0)
sourceColor = 'red'
sourceSize = (10, 10)

soundWaveColor = (100, 0, 0)
soundWaveWidth = 10
soundWaveSpeed = 5
updateRate = 10

soundSpeed = 343


class DetectionSystem():
    def __init__(self) -> None:
        self.mics = []
        self.source = Source(sourcePos)
        self.detected = False
        self.sourceAngle = 0
        self.inititalizeMics()

    def inititalizeMics(self):
        angleOffset = 2 * math.pi / noOfMics
        angle = 0
        for _ in range(noOfMics):
            x = micArrayRadius * math.cos(angle)
            y = micArrayRadius * math.sin(angle)
            self.mics.append(Mic((x,y)))
            angle += angleOffset
        self.mics[0].color = "red"
        self.mics[1].color = "blue"
        self.mics[2].color = "yellow"
        self.mics[3].color = "pink"
    
    def detectSoundWave(self):
        if Mic.allMicsDetected == noOfMics:
            self.calculateAngle()
            self.detected = True
    
    def calculateAngle(self):
        timeDiff = self.mics[1].timeStamp - self.mics[3].timeStamp
        value = (timeDiff * soundSpeed) / (2*micArrayRadius)
        if(value > 1 or value < -1):
            value = 1
        try:
            angle = math.degrees(math.acos(value))
            angle = 90 - angle
        except:
            print("Math Value Error", value)

        print("Angle: ", angle)
        self.sourceAngle = angle
        self.sourceAngleProvider()
    
    def resetMics(self):
        for mic in self.mics:
            mic.timeStamp = 0
            mic.color = micIdleColor
        
        Mic.allMicsDetected = 0
        print("Mic Ready for next Wave")
    
    def update(self):
        self.detectSoundWave()
        if self.detected:
            self.resetMics()
            self.detected = False

    def drawMics(self):
        pygame.draw.circle(screen, arrayColor, micArrayCenter, micArrayRadius + micArrayWidth //2, micArrayWidth)
        for mic in self.mics:
            mic.draw()


    def draw(self):
        self.drawMics()
        self.source.draw()
    
    def handleEvent(self, event):
        if event.type == KEYDOWN and event.key == K_SPACE:
            # if self.readyForNextWave:
            self.source.fireShot()
            
        if event.type == MOUSEBUTTONDOWN:
            self.source.rect.center = event.pos
    
    def updateMics(self):
        for mic in self.mics:
            mic.update(self.source)
    
    def updateSource(self):
        self.source.update()
    
    def sourceAngleProvider(self):
        sortedMics = sorted(self.mics, key=lambda mic: mic.timeStamp if mic.timeStamp != 0 else float('inf'))
        if(self.mics[0] == sortedMics[0] and self.mics[1] == sortedMics[1]) or (self.mics[0] == sortedMics[1] and self.mics[1] == sortedMics[0]):
            self.sourceAngle = abs(self.sourceAngle)
        if (sortedMics[0] == self.mics[1] and sortedMics[1] == self.mics[2]) or (sortedMics[0] == self.mics[2] and sortedMics[1] == self.mics[1]):
            self.sourceAngle = (90 - abs(self.sourceAngle)) + 90
        if (sortedMics[0] == self.mics[2] and sortedMics[1] == self.mics[3]) or (sortedMics[0] == self.mics[3] and sortedMics[1] == self.mics[2]):
            self.sourceAngle = (abs(self.sourceAngle)) + 180
        if (sortedMics[0] == self.mics[3] and sortedMics[1] == self.mics[0]) or (sortedMics[0] == self.mics[0] and sortedMics[1] == self.mics[3]):
            self.sourceAngle = (90 - abs(self.sourceAngle)) + 270
        if (self.sourceAngle == -90 ):
            self.sourceAngle = 90
        if (self.sourceAngle == 0 and sortedMics[0] == self.mics[0]):
            self.sourceAngle = 0
        if (self.sourceAngle == 0 and sortedMics[0] == self.mics[2]):
            self.sourceAngle = 180
        if (self.sourceAngle == 90 ):
            self.sourceAngle = 270
        
        print("Final Angle: ", self.sourceAngle)
            


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
            if self in wave['detected']:
                continue

            center = wave['center']
            distance = math.sqrt((self.rect.centerx - center[0]) ** 2 + (self.rect.centery - center[1]) ** 2)
            if distance <= wave['radius']:
                if self.timeStamp == 0:
                    self.timeStamp = distance / soundSpeed
                    self.color = micDetectedColor
                    print(f"Mic at {self.position} detected collision at {self.timeStamp} ms")
                    Mic.allMicsDetected += 1
                    wave['detected'].append(self)

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
            'radius': 0,
            'detected': []
        })

    def update(self):
        self.sendSoundWave()
        if Mic.allMicsDetected:
            pass



detectionSystem = DetectionSystem()

clock = pygame.time.Clock()
running = True
while (running):

    for ev in pygame.event.get():
        if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
            running = False
        
        detectionSystem.handleEvent(ev)
        
    screen.fill(bgColor)

    detectionSystem.draw()
    detectionSystem.updateMics()
    detectionSystem.updateSource()
    detectionSystem.update()

    clock.tick(60)
    pygame.display.flip()

pygame.quit()