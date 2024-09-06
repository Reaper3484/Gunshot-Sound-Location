from radar import Radar
from config import *


class DetectionSystem():
    def __init__(self, radar) -> None:
        self.surf = pygame.Surface((simWidth, height))
        self.mics = []
        self.source = Source(sourcePos, self.surf)
        self.detected = False
        self.radar = radar
        self.inititalizeMics()

    def inititalizeMics(self):
        angleOffset = 2 * math.pi / noOfMics
        angle = 0
        for _ in range(noOfMics):
            x = micArrayRadius * math.cos(angle)
            y = micArrayRadius * math.sin(angle)
            self.mics.append(Mic((x, y), self.surf))
            angle += angleOffset

    def detectSoundWave(self):
        if Mic.allMicsDetected == noOfMics:
            self.calculateAngle()
            self.detected = True

    def calculateAngle(self):
        timeDiff = self.mics[1].timeStamp - self.mics[3].timeStamp
        value = (timeDiff * soundSpeed) / (2*micArrayRadius)
        if(value > 1):
            value = 1
        elif(value <-1):
            value = -1
        try:
            angle = math.degrees(math.acos(value))
            angle = 90 - angle
        except:
            print("Math Value Error", value)

        print("Angle: ", angle)
        self.sourceAngleProvider(angle)

    def sourceAngleProvider(self, angle):
        sortedMics = sorted(self.mics, key=lambda mic: mic.timeStamp if mic.timeStamp != 0 else float('inf'))
        if(self.mics[0] == sortedMics[0] and self.mics[1] == sortedMics[1]) or (self.mics[0] == sortedMics[1] and self.mics[1] == sortedMics[0]):
            angle = abs(angle)
        if (sortedMics[0] == self.mics[1] and sortedMics[1] == self.mics[2]) or (sortedMics[0] == self.mics[2] and sortedMics[1] == self.mics[1]):
            angle = (90 - abs(angle)) + 90
        if (sortedMics[0] == self.mics[2] and sortedMics[1] == self.mics[3]) or (sortedMics[0] == self.mics[3] and sortedMics[1] == self.mics[2]):
            angle = (abs(angle)) + 180
        if (sortedMics[0] == self.mics[3] and sortedMics[1] == self.mics[0]) or (sortedMics[0] == self.mics[0] and sortedMics[1] == self.mics[3]):
            angle = (90 - abs(angle)) + 270
        if (angle == -90 ):
            angle = 90
        if (angle == 0 and sortedMics[0] == self.mics[0]):
            angle = 0
        if (angle == 0 and sortedMics[0] == self.mics[2]):
            angle = 180
        if (angle == 90 ):
            angle = 270
        
        self.radar.addBlip(angle)
        BlipSound.play()
        
    def resetMics(self):
        for mic in self.mics:
            mic.timeStamp = 0
            mic.color = micIdleColor

        Mic.allMicsDetected = 0

    def update(self):
        for mic in self.mics:
            mic.update(self.source)

        self.source.update()

        self.detectSoundWave()
        if self.detected:
            self.resetMics()
            self.detected = False

    def drawMics(self):
        pygame.draw.circle(self.surf, arrayColor, micArrayCenter,
                           micArrayRadius + micArrayWidth // 2, micArrayWidth)
        for mic in self.mics:
            mic.draw()

    def draw(self):
        self.drawMics()
        self.source.draw()
        screen.blit(self.surf, (0, 0))
        self.surf.fill(bgColor)

    def handleEvent(self, event):
        if event.type == KEYDOWN and event.key == K_SPACE:
            BulletSound.play()
            self.source.fireShot()

        if event.type == MOUSEBUTTONDOWN:
            if (event.pos[0] <= simWidth):
                self.source.rect.center = event.pos


class Mic():
    allMicsDetected = 0
    angleCalculated = False

    def __init__(self, position, screen) -> None:
        self.screen = screen
        self.surf = pygame.Surface((micRadius * 2, micRadius * 2))
        self.rect = self.surf.get_rect(
            center=(micArrayCenter[0] + position[0], micArrayCenter[1] + position[1]))
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
            distance = math.sqrt(
                (self.rect.centerx - center[0]) ** 2 + (self.rect.centery - center[1]) ** 2)
            if distance <= wave['radius']:
                if self.timeStamp == 0:
                    self.timeStamp = distance / soundSpeed
                    self.color = micDetectedColor
                    Mic.allMicsDetected += 1
                    wave['detected'].append(self)
                    micDetectPing.play()


    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           self.rect.center, micRadius)

    def update(self, source):
        self.checkCollision(source)


class Source():
    def __init__(self, position, screen) -> None:
        self.screen = screen
        self.surf = pygame.Surface(sourceSize)
        self.rect = self.surf.get_rect(center=position)
        self.color = sourceColor
        self.soundWaveColor = soundWaveColor
        self.radius = 10
        self.last_update_time = pygame.time.get_ticks()
        self.soundWaves = []

    def draw(self):
        pygame.draw.circle(self.screen, self.color,
                           self.rect.center, self.radius)

        for wave in self.soundWaves:
            pygame.draw.circle(wave['surf'], self.soundWaveColor,
                               wave['center'], wave['radius'], soundWaveWidth)
            self.screen.blit(wave['surf'], (0, 0))

    def sendSoundWave(self):
        curr_time = pygame.time.get_ticks()
        if curr_time - self.last_update_time >= updateRate:
            for wave in self.soundWaves.copy():
                wave['radius'] += soundWaveSpeed
                if wave['radius'] > max(simWidth, height):
                    self.soundWaves.remove(wave)
                    continue

                opacity = (wave['radius'] / wave['edgeDistance']) * 255
                wave['surf'].set_alpha(255 - opacity)

            self.last_update_time = curr_time

    def fireShot(self):
        surf = pygame.Surface((simWidth, height), SRCALPHA)
        x, y = self.rect.center
        bottom = height - y
        top = y
        left = x
        right = simWidth - x
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


radar = Radar(screen, simWidth, radarWidth, height)
detectionSystem = DetectionSystem(radar)

clock = pygame.time.Clock()
running = True
while (running):

    for ev in pygame.event.get():
        if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
            running = False

        detectionSystem.handleEvent(ev)

    radar.draw()
    radar.update()
    detectionSystem.draw()
    detectionSystem.update()

    clock.tick(frameRate)
    pygame.display.flip()

pygame.quit()
